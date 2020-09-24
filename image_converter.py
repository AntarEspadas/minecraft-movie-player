import numpy
import cv2
import structure_block
import os
import csv
import kdtree
import time
import multiprocessing


def video_to_structure(path_to_video: str, destination_folder: str, name_prefix: str, path_to_palette: str = None, ticks_per_frame:int = 2, starting_frame: int = 0,  starting_number: int = None, width: int = None, height: int = None, adjust_mode: str = None, optimize = True):
    video = cv2.VideoCapture(path_to_video)
    palette = _get_palette(path_to_palette or os.path.join(os.path.dirname(__name__),"palette.txt"))
    
    starting_number = starting_number or starting_frame

    output_fps = 20 / ticks_per_frame
    video_fps = video.get(cv2.CAP_PROP_FPS)
    frame_skip = video_fps / output_fps

    video.set(cv2.CAP_PROP_POS_FRAMES, int(starting_frame * frame_skip) - 1)
    success, image = video.read()
    
    size = _get_image_size(image, width, height, adjust_mode)
    adjust = _get_adjuster(image, width, height, adjust_mode)

    if optimize:
        x = image.shape[1]
        y = image.shape[0]
        base = [[None for _ in range(x)] for _ in range(y)]
    else:
        base = None

    process = None
    count = 0
    while success:
        start = time.time()
        image = adjust(image, size)
        structure = array_to_structure(image, palette, base)
        structure.save(os.path.join(destination_folder, f"{name_prefix}{starting_number + count}.nbt"))
        print(f"{count} done in {time.time() - start} seconds")
        count += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, int(frame_skip * (starting_frame + count)) - 1)
        success, image = video.read()

def image_to_structure(path_to_image: str, out_structure: str, path_to_palette: str = "palette.txt", width: int = None, height: int = None, adjust_mode = None):
    start = time.time()
    palette = _get_palette(path_to_palette)
    image = cv2.imread(path_to_image)

    size = _get_image_size(image, width, height, adjust_mode)
    image = _get_adjuster(image, width, height, adjust_mode)(image, size)
    print(time.time() - start)

    start = time.time()
    structure = array_to_structure(image, palette)
    print(time.time() - start)

    start = time.time()
    structure.save(out_structure)
    print(time.time() - start)

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
    palette_file = open(path_to_palette,newline="")
    palette_reader = csv.reader(palette_file,delimiter=",",quotechar="|")
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


if __name__ == "__main__":
    path_to_video = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\rickroll.mp4"
    #path_to_video = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\bbb_sunflower_1080p_30fps_normal.mp4"
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\rickroll"
    #output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\big_buck_bunny"
    palette = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\palette.txt"
    #path_to_image = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\carved_pumpkin.png"
    path_to_image = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\test.jpg"
    #path_to_structure = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\carved_pumpkin.nbt"
    path_to_structure = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\test.nbt"
    name_prefix = "rickroll_"
    #image_to_structure(path_to_image, path_to_structure, palette, 75)
    video_to_structure(path_to_video, output_folder, name_prefix, path_to_palette= palette, width= 50, starting_frame=0)
    #__get_palette(palette)