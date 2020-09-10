import argparse

parser = argparse.ArgumentParser()
parsers = parser.add_subparsers(help="commands",dest="command")

video_parser = parsers.add_parser("video", help="convert video into blocks or maps")
video_parser.add_argument("path_to_input_file", type=str, help="The path to the video file that will be converted to maps or blocks")
video_parser.add_argument("path_to_output_file", type=str, help="The path to which the zip file containing the frames will be written")
video_parser.add_argument("-f", "--ticks-per-frame", default="2", type=int, dest="ticks_per_frame",help="How many game ticks between every frame. Can be any integer from 1 to 20. Default is 2. 20 = 1 fps, 2 = 10 fps, 1 = 20 fps, etc...")
video_parser.add_argument("-x", "--width", default=-1, type=int, dest="width", help="The width of the output video, measured in blocks or maps")
video_parser.add_argument("-y", "--height",default=-1, type=int, dest="height", help="The height of the output video, measured in blocks or maps")
video_parser.add_argument("-u","--unoptimized", action="store_true", dest="unoptimized", help="By default, when converting to blocks, every frame contains only the blocks that differ from the previous frame in an attempt to save resources. Using this option will disable this feature. Will be ignored if converting to maps")
type_group = video_parser.add_mutually_exclusive_group(required = True)
type_group.add_argument("-m","--maps", action="store_const", const="item-frame", dest="type", help="Tells the program to convert the video into maps")
type_group.add_argument("-b","--blocks", action="store_const", const="blocks", dest="type", help="Tells the program to convert the video into blocks")

audio_parser = parsers.add_parser("audio", help="generates resourcepack containint audio files")
audio_parser.add_argument("-s", "--split-size", default="1", type=int, dest="split_size")

datapack_parser = parsers.add_parser("datapack", help="generates movie player datapack")
datapack_parser.add_argument("-m","--merge", action="store_true", dest="merge")

#parser.add_argument("-nv", "--no-video", help="doesn't convert the video to any format", action="store_true")
args = parser.parse_args()
print(args.command)

if args.command == "video":
    pass
elif args.command == "audio":
    pass
elif args.command == "datapack":
    pass

