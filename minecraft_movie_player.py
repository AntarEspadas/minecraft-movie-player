def main():
    import argparse

    parser = argparse.ArgumentParser()
    parsers = parser.add_subparsers(help="commands", dest="command")

    video_parser = parsers.add_parser("video", help="convert video to structure files")
    video_parser.add_argument("path_to_video", type=str, help="The path to the video file that will be converted to structure files")
    video_parser.add_argument("path_to_output_folder", type=str, help="The path to the folder in which the frames will be written")
    video_parser.add_argument("-p", "--palette", default="palette.txt", type=str, dest="path_to_palette",help="The path to the block palette file to be used when convertnig")
    video_parser.add_argument("-t", "--ticks-per-frame", default="2", type=int, dest="ticks_per_frame",help="How many game ticks between every frame. Can be any integer from 1 to 20. Default is 2. 20 = 1 fps, 2 = 10 fps, 1 = 20 fps, etc...")
    video_parser.add_argument("-x", "--width", default=-1, type=int, dest="width", help="The width of the output frames, measured in blocks")
    video_parser.add_argument("-y", "--height",default=-1, type=int, dest="height", help="The height of the output frames, measured in blocks")
    video_parser.add_argument("-n", "--name-prefix", default="video", type=str, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    video_parser.add_argument("-u","--unoptimized", action="store_true", dest="unoptimized", help="By default, every frame contains only the blocks that differ from the previous frame in an attempt to save resources. Using this option will disable this feature")


    resourcepak_parser = parsers.add_parser("resourcepack", help="Generates two key components for the resourcepack that will be used to play the audio: The sound files and the sounds.json file")
    resourcepack_parsers = resourcepak_parser.add_subparsers("subcommands", dest="subcommand")

    resourcepack_audio_parser = resourcepack_parsers.add_parser("audio", help="Splits the audio track from a video or audio file into several vorbis encoded audio files so that it can be used by the player")
    resourcepack_audio_parser.add_argument("path_to_audio", type=str, help="The path to the audio file that will be split and converted")
    resourcepack_audio_parser.add_argument("path_to_output_folder", type=str, help="The path to the folder in which the audio files will be written")
    resourcepack_audio_parser.add_argument("-s", "--split-size", default="60", type=int, dest="split_size", help="The duration in seconds of every generated audio file")
    resourcepack_audio_parser.add_argument("-n", "--name-prefix", default="audio", type=str, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    
    resourcepack_json_parser = resourcepack_parsers.add_parser("json", help="Generates the sounds.json file required to create thr resourcepack")
    resourcepack_json_parser.add_argument("output_folder", type=str, help="The path to the folder in which the sounds.json file will be written")
    resourcepack_json_parser.add_argument("amount_of_sound_files", type=int, help="The amount of sound files that should be added to sonds.json")
    resourcepack_json_parser.add_argument("-n", "--name-prefix", type=str, default="audio", dest="name_prefix", help="The name that was prefixed to every sound file")
    resourcepack_json_parser.add_argument("-s","--subfolder-name", default="player", dest="subfolder_name", type=str, help="The name of the resourcepack subfolder where the audio files should be moved to")

    functions_parser = parsers.add_parser("functions", help="generates movie player functions")
    functions_parsers = functions_parser.add_subparsers(help="subcommands", dest="subcommand")

    video_functions_parser = functions_parsers.add_parser("video", help="Generate the functions required for video playbak")

    audio_functions_parser = functions_parsers.add_parser("audio", help="Generate the functions required for audio playbak")
    
    playback_control_functions_parser = functions_parsers.add_parser("playback-control", help="Generate the functions required for controlling the video and audio playback")

    #parser.add_argument("-nv", "--no-video", help="doesn't convert the video to any format", action="store_true")
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "video":
        pass
    elif args.command == "audio":
        pass
    elif args.command == "functions":
        if args.subcommand is None:
            functions_parser.print_help()
        elif args.subcommand == "video":
            pass
        elif args.subcommand == "audio":
            pass
        elif args.subcommand == "playback-control":
            pass

if __name__ == "__main__":
    main()