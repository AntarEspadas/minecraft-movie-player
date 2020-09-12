import numpy
import cv2
import os
import csv

def __get_all_files(directory: str) -> list:
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def __get_average_color(image: numpy.ndarray) -> list:
    avg_color_per_row = numpy.average(image, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return numpy.flip(avg_color)

def __generate_palette_from_index(source_directory: str, destination_file: str, index_file: str):
    palette_file = open(destination_file, "w+")
    if index_file is not None:
        index = open(index_file,newline="")
        i = 0
        for row in csv.reader(index,delimiter=",",quotechar="|"):
            i += 1
            if len(row) < 2:
                print(f"Not enough values in row {i}")
                continue
            if len(row) > 3:
                print(f"Ignoring extra values in row {i}")
            image = cv2.imread(os.path.join(source_directory,row[0]))
            if image is not None:
                color = __get_average_color(image)
                palette_file.write(f"{row[1]},%d,%d,%d,|{row[2]}|\n" % tuple(color))
            else:
                print(f"Unable to read {row[0]}. File may not exist or not be an image")
        index.close()
        palette_file.close()

def generate_palette(source_directory: str, destination_file: str, index_file: str = None):
    if index_file is not None:
        __generate_palette_from_index(source_directory,destination_file,index)
        return

    palette_file = open(destination_file, "w+")
    files = __get_all_files(source_directory)
    for file in files:
        image = cv2.imread(os.path.join(source_directory,file))
        if image is not None:
            try:
                color = __get_average_color(image)
                palette_file.write(f"{file},%d,%d,%d\n" % tuple(color)) 
            except Exception:
                print(f"An unknown error ocurred reading file {file}")
        else:
            print(f"Unable to read {file}. File may not exist or not be an image")
    palette_file.close()

def generate_index_template(source_directory: str, destination_file: str, filename_is_id: bool = True):
    file = open(destination_file,"w+")
    for image in __get_all_files(source_directory):
        filename, extension = os.path.splitext(image)
        if extension[1:].lower() == "png":
            file.write(f"{image},{filename if filename_is_id else ''},\n")
    file.close

if __name__ == "__main__":
    folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\FilteredBlocks"
    index = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\FilteredBlocks\\index.txt"
    generate_palette(folder,"D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\FilteredBlocks\\palette.txt", index)
    #generate_index_template(folder,index)
    