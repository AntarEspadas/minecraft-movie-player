import numpy
import cv2
import structure_block
import os

def video_to_structure(path_to_video: str, destination_folder: str, name_prefix: str, path_to_palette: str = None, starting_number: int = None, width: int = None, height: int = None, adjust_mode: str = "fit"):
    video = cv2.VideoCapture(path_to_video)
    palette = __get_palette(path_to_palette or os.path.join(os.path.dirname(__name__),"palette.txt"))

def __get_palette(path_to_palette):
    return None

class _Block:
    def __init__(self):
        super().__init__()