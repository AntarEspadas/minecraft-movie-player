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
    with open(destination_file, "w+", newline="") as palette_file:
        writer = csv.writer(palette_file, delimiter=";", quotechar='"')
        index = open(index_file, newline="")
        i = 0
        for row in csv.reader(index, delimiter=";", quotechar='"'):
            i += 1
            if len(row) < 2:
                print(f"Not enough values in row {i}")
                continue
            if len(row) > 3:
                print(f"Ignoring extra values in row {i}")
            image = cv2.imread(os.path.join(source_directory,row[0]))
            if image is not None:
                color = __get_average_color(image)
                writer.writerow(row[1:2] + list(color) + row[2:3])
            else:
                print(f"Unable to read {row[0]}. File may not exist or not be an image")
        index.close()

def generate_palette(source_directory: str, destination_file: str, index_file: str = None):
    if index_file is not None:
        __generate_palette_from_index(source_directory,destination_file,index_file)
        return

    with open(destination_file, "w+", newline="") as palette_file:
        writer = csv.writer(palette_file, delimiter=";", quotechar='"')
        files = __get_all_files(source_directory)
        for file in files:
            image = cv2.imread(os.path.join(source_directory,file))
            if image is not None:
                try:
                    color = __get_average_color(image)
                    writer.writerow([file] + list(color)) 
                except Exception:
                    print(f"An unknown error ocurred reading file {file}")
            else:
                print(f"Unable to read {file}. File may not exist or not be an image")

def generate_index_template(source_directory: str, destination_file: str, filename_is_id: bool = True):
    with open(destination_file,"w+", newline="") as f:
        writer = csv.writer(f, delimiter=";", quotechar='"')
        for image in __get_all_files(source_directory):
            filename, extension = os.path.splitext(image)
            if extension[1:].lower() == "png":
                writer.writerow((image, filename if filename_is_id else "", ""))

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parsers = parser.add_subparsers(help="commands",dest="command")

    parser.add_argument("path_to_images_folder", type=str, help="Path to the folder containing the images that are to be used")
    parser.add_argument("destination_file_path",type=str, help="Path where the generated file will be saved")

    index_parser = parsers.add_parser("generate-index", help="Generate a basic index file. Refer to the script's instructions for more information about this file")
    index_parser.add_argument("--filename-is-id", action="store_true", default=None, dest="filename_is_id", help="In a lot of cases, the filenames of the images correspond to their block IDs. Using this option will fill the column for block IDs with the filenames of the images")

    palette_parser = parsers.add_parser("generate-palette", help="Calculate the average color for the images in the specified folder")
    palette_parser.add_argument("-i","--index", type=str, default=None, dest="path_to_index", help="Path to the index file. If not specified, will process all image files in the folder and use the filenames as block IDs. Refer to the script's instructions for more information about this file")

    args = parser.parse_args()
    
    print("Working...")
    if args.command == "generate-index":
        generate_index_template(args.path_to_images_folder, args.destination_file_path, args.filename_is_id)
        print(f"Index saved to {args.destination_file_path}")
    elif args.command == "generate-palette":
        generate_palette(args.path_to_images_folder, args.destination_file_path, args.path_to_index)
        print(f"Palette saved to {args.destination_file_path}")

if __name__ == "__main__":
    main()