import numpy
import cv2
from . import structure_block
import os
import csv
import kdtree
import time
import multiprocessing
import datetime
from math import ceil


def video_to_structure(path_to_video: str, destination_folder: str, name_prefix: str, path_to_palette: str = None, ticks_per_frame:int = 2, starting_frame: int = 0, width: int = None, height: int = None, adjust_mode: str = None, optimize = True, processes: int = None, on_progress = None):
    
    path_to_palette = path_to_palette if path_to_palette is not None else os.path.join(os.path.dirname(__file__), "palette.txt")

    video = cv2.VideoCapture(path_to_video)

    output_fps = 20 / ticks_per_frame
    video_fps = video.get(cv2.CAP_PROP_FPS)
    frame_skip = video_fps / output_fps

    video.set(cv2.CAP_PROP_POS_FRAMES, int(starting_frame * frame_skip) - 1)
    success, image = video.read()
    
    size = _get_image_size(image, width, height, adjust_mode)
    adjust = _get_adjuster(image, width, height, adjust_mode)

    path_to_palette = os.path.abspath(path_to_palette)

    processes = processes if processes is not None else multiprocessing.cpu_count()
    in_q = multiprocessing.Queue()
    out_q = multiprocessing.Queue()
    row_processors = [multiprocessing.Process(target=_row_processor, args=(path_to_palette, in_q, out_q)) for _ in range(processes)]
    [process.start() for process in row_processors]

    if optimize:
        x = image.shape[1]
        y = image.shape[0]
        base = [[None for _ in range(y)] for _ in range(x)]
    else:
        base = None

    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT) / frame_skip
    total_frames = ceil(total_frames)
    count = 0
    total_time = 0
    print("converting video...")
    while success:
        start = time.time()
        image = adjust(image, size)
        structure = _array_to_structure(image, in_q, out_q, base)
        structure.save(os.path.join(destination_folder, f"{name_prefix}{starting_frame + count}.nbt"))
        if on_progress is not None:
            on_progress(starting_frame + count)
        count += 1
        elapsed = time.time() - start
        total_time += elapsed
        average = total_time / (count)
        eta = (total_frames - starting_frame - count) * average
        eta = datetime.timedelta(seconds=round(eta))
        print(f"{starting_frame + count}/{total_frames} (Elapsed: {datetime.timedelta(seconds=round(total_time, 5))}, Average: {round(average, 5)}s, ETA: {eta})" + " "*10, end="\r")
        video.set(cv2.CAP_PROP_POS_FRAMES, int(frame_skip * (starting_frame + count)) - 1)
        success, image = video.read()
    print("")
    print("done!")
    [process.terminate() for process in row_processors]
    return count

def image_to_structure(path_to_image: str, out_structure: str, path_to_palette: str = None, width: int = None, height: int = None, adjust_mode = None):
    
    path_to_palette = path_to_palette if path_to_palette is not None else os.path.join(os.path.dirname(__file__), "palette.txt")
    
    palette = _get_palette(path_to_palette)
    image = cv2.imread(path_to_image)

    size = _get_image_size(image, width, height, adjust_mode)
    image = _get_adjuster(image, width, height, adjust_mode)(image, size)
    structure = array_to_structure(image, palette)

    structure.save(out_structure)

def array_to_structure(image: numpy.ndarray, palette: kdtree.KDNode, base = None):
    structure = structure_block.StructureBlock((len(image[0]), len(image), 1))
    for y, row in enumerate(numpy.flip(image, 0)):
        for x, pixel in enumerate(row):
            block = palette.search_nn(tuple(numpy.flip(pixel)))[0].data
            if base is not None:
                if base[x][y] == (block.block_id, block.block_state):
                    continue
                else:
                    base[x][y] = (block.block_id, block.block_state)
            structure.setblock((x,y,0), block.block_id, block.block_state)

    return structure

def _array_to_structure(image: numpy.ndarray, in_q, out_q, base = None):
    structure = structure_block.StructureBlock((len(image[0]), len(image), 1))
    for y, row in enumerate(numpy.flip(image, 0)):
        base_row = base[y] if base is not None else None
        in_q.put((y, row, base_row))

    finished_rows = 0
    while True:
        if finished_rows == y + 1:
            break
        result = out_q.get()
        if result == "done":
            finished_rows += 1
            continue
        
        structure.setblock(*result)
        if base is not None:
            base[result[0][1]][result[0][0]] = result[1:]

    return structure

def _row_processor(path_to_palette: str, in_q, out_q):
    palette = _get_palette(path_to_palette)

    while True:
        args = in_q.get()
        y, row, base_row = args

        for x, pixel in enumerate(row):
            block = palette.search_nn(tuple(numpy.flip(pixel)))[0].data
            if base_row is not None and base_row[x] == (block.block_id, block.block_state):
                continue
            out_q.put(((x,y,0), block.block_id, block.block_state))

        out_q.put("done")


def _get_adjuster(image: numpy.ndarray, width: str = None, height: str = None, adjust_mode: str = None):
    
    def nop(image: numpy.ndarray, size: tuple) -> numpy.ndarray:
        return image
    
    def resize_only(image: numpy.ndarray, size: tuple) -> numpy.ndarray:
        return cv2.resize(image, size)

    def resize_and_crop(image: numpy.ndarray, size: tuple) -> numpy.ndarray:
        image = cv2.resize(image, size)
        return _crop(image, width, height)

    def resize_and_pad(image: numpy.ndarray, size: tuple) -> numpy.ndarray:
        image = cv2.resize(image, size)
        return _pad(image, width, height)

    img_width = image.shape[1]
    img_height = image.shape[0]

    if width is None and height is None:
        return nop

    if width is None or height is None:
        if width == img_width or height == img_height:
            return nop
        else:
            return resize_only
    
    if (img_width, img_height) == (width, height):
        return nop

    if abs(img_width/ img_height - width / height) < 0.01:
        return resize_only
    
    if adjust_mode == "fill":
        return resize_and_crop

    return resize_and_pad

def _crop(image: numpy.ndarray, width: int, height: int):
    img_width = image.shape[1]
    img_height = image.shape[0]
    w_offset = (img_width - width) // 2
    h_offset = (img_height - height) // 2
    return image[h_offset:h_offset + height, w_offset:w_offset + width]

def _pad(image: numpy.ndarray, width: int, height: int):
    img_width = image.shape[1]
    img_height = image.shape[0]
    w_offset = (width - img_width) // 2
    h_offset = (height - img_height) // 2
    destination_image = numpy.zeros((height, width, 3))
    destination_image[h_offset:h_offset + img_height, w_offset: w_offset + img_width] = image
    return destination_image

def _get_image_size(image: numpy.ndarray, width: int = None, height: int = None, adjust_mode: str = None):
    img_width = image.shape[1]
    img_height = image.shape[0]
    
    if width is not None and height is not None:
        dif = img_width / img_height > width / height
        if dif and adjust_mode != "fill":
            height = None
        else:
            width = None

    if width is None and height is None:
        return img_width, img_height
    if height is None:
        height = img_height / img_width * width
    elif width is None:
        width = img_width / img_height * height
    return int(width), int(height)

def _get_palette(path_to_palette):
    palette_file = open(path_to_palette, newline="")
    palette_reader = csv.reader(palette_file, dialect="excel", delimiter=";", quotechar='"')
    blocks = [_Block(tuple([int(i) for i in block[1:4]]),block[0], block[4] or None) for block in palette_reader]
    palette = kdtree.create(blocks)
    palette_file.close()
    return palette

class _Block:
    def __init__(self, color: tuple, block_id: str, block_state: str):
        self.color = color
        self.block_id = block_id
        self.block_state = block_state
    
    def __len__(self):
        return len(self.color)

    def __getitem__(self, i):
        return self.color[i]

