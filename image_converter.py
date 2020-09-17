import numpy
import cv2
import structure_block
import os
import csv
import kdtree

def video_to_structure(path_to_video: str, destination_folder: str, name_prefix: str, path_to_palette: str = None, starting_number: int = None, width: int = None, height: int = None, adjust_mode: str = "fit"):
    video = cv2.VideoCapture(path_to_video)
    palette = __get_palette(path_to_palette or os.path.join(os.path.dirname(__name__),"palette.txt"))
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    success, image = video.read()
    

    array_to_structure(image, palette).save(os.path.join(destination_folder,name_prefix + ".nbt"))

def image_to_structure(path_to_image: str, out_structure: str, path_to_palette: str = "palette.txt"):
    palette = __get_palette(path_to_palette)
    image = cv2.imread(path_to_image)
    structure = array_to_structure(image, palette)
    structure.save(out_structure)

def array_to_structure(image: numpy.ndarray, palette):
    structure = structure_block.StructureBlock((len(image[0]), len(image), 1))

    for y, row in enumerate(numpy.flip(image, 0)):
        for x, pixel in enumerate(row):
            block = palette.search_nn(tuple(numpy.flip(pixel)))[0].data
            structure.setblock((x,y,0), block.block_id, block.block_state)

    return structure

def __get_palette(path_to_palette):
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
    path_to_video = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\rickroll.mp4"#"D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\bbb_sunflower_1080p_30fps_normal.mp4"
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io"
    palette = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\palette.txt"
    path_to_image = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\carved_pumpkin.png"
    path_to_structure = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\carved_pumpkin.nbt"
    name_prefix = "test"
    image_to_structure(path_to_image, path_to_structure, palette)
    #video_to_structure(path_to_video,output_folder,name_prefix,palette)
    #__get_palette(palette)