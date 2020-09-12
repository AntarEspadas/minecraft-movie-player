import numpy
import cv2
import structure_block
import os
import csv
import kdtree

def video_to_structure(path_to_video: str, destination_folder: str, name_prefix: str, path_to_palette: str = None, starting_number: int = None, width: int = None, height: int = None, adjust_mode: str = "fit"):
    video = cv2.VideoCapture(path_to_video)
    palette = __get_palette(path_to_palette or os.path.join(os.path.dirname(__name__),"palette.txt"))

def __get_palette(path_to_palette):
    palette_file = open(path_to_palette,newline="")
    palette_reader = csv.reader(palette_file,delimiter=",",quotechar="|")
    blocks = [_Block(tuple(block[1:4]),block[0], block[4] or None) for block in palette_reader]
    palette = kdtree.create(blocks)

class _Block:
    def __init__(self, color: tuple, block_id: str, block_state: str):
        self._color = color
        self._block_id = block_id
        self._block_state = block_state
    
    def __len__(self):
        return len(self._color)

    def __getitem__(self, i):
        return self._color[i]


if __name__ == "__main__":
    __get_palette("D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\palette.txt")