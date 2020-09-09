import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-nv", "--no-video", help="doesn't convert the video to any format", action="store_true")
args = parser.parse_args()

if args.no_video:
    print("No video will be output")