def main():
    import argparse

    parser = argparse.ArgumentParser()
    parsers = parser.add_subparsers(help="commands", dest="command")

    video_parser = parsers.add_parser("video", help="convert video to structure files")
    video_parser.add_argument("path_to_video", type=str, help="The path to the video file that will be converted to structure files")
    video_parser.add_argument("path_to_output_folder", type=str, help="The path to the folder in which the frames will be written")
    video_parser.add_argument("-p", "--palette", default="palette.txt", type=str, dest="path_to_palette",help="The path to the block palette file to be used when convertnig")
    video_parser.add_argument("-n", "--name-prefix", default="video_", type=str, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    video_parser.add_argument("-t", "--ticks-per-frame", default="2", type=int, dest="ticks_per_frame",help="How many game ticks between every frame. Can be any integer from 1 to 20. Default is 2. 20 = 1 fps, 2 = 10 fps, 1 = 20 fps, etc...")
    video_parser.add_argument("-x", "--width", default=-1, type=int, dest="width", help="The width of the output frames, measured in blocks")
    video_parser.add_argument("-y", "--height",default=-1, type=int, dest="height", help="The height of the output frames, measured in blocks")
    video_parser.add_argument("-u","--unoptimized", action="store_true", dest="unoptimized", help="By default, every frame contains only the blocks that differ from the previous frame in an attempt to save resources. Using this option will disable this feature")


    resourcepak_parser = parsers.add_parser("resourcepack", help="Generate sound files and sounds.json")
    resourcepack_parsers = resourcepak_parser.add_subparsers(help="subcommands", dest="subcommand")

    resourcepack_audio_parser = resourcepack_parsers.add_parser("audio", help="Splits the audio track from a video or audio file into several vorbis encoded audio files so that it can be used by the player")
    resourcepack_audio_parser.add_argument("path_to_audio", type=str, help="The path to the audio file that will be split and converted")
    resourcepack_audio_parser.add_argument("path_to_output_folder", type=str, help="The path to the folder in which the audio files will be written")
    resourcepack_audio_parser.add_argument("-s", "--split-size", default="60", type=float, dest="split_size", help="The duration in seconds of every generated audio file")
    resourcepack_audio_parser.add_argument("-p", "--name-prefix", default="audio_", type=str, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    
    resourcepack_json_parser = resourcepack_parsers.add_parser("json", help="Generates the sounds.json file required to create thr resourcepack")
    resourcepack_json_parser.add_argument("output_folder", type=str, help="The path to the folder in which the sounds.json file will be written")
    resourcepack_json_parser.add_argument("amount_of_sound_files", type=int, help="The amount of sound files that should be added to sonds.json")
    resourcepack_json_parser.add_argument("-p", "--name-prefix", type=str, default="audio_", dest="name_prefix", help="The name that was prefixed to every sound file")
    resourcepack_json_parser.add_argument("-s","--subfolder-name", default="player", dest="subfolder_name", type=str, help="The name of the resourcepack subfolder where the audio files should be moved to")

    functions_parser = parsers.add_parser("functions", help="generates movie player functions")
    functions_parsers = functions_parser.add_subparsers(help="subcommands", dest="subcommand")

    #(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands: int = 25, ticks_per_frame: int = 2)
    video_functions_parser = functions_parsers.add_parser("video", help="Generate the functions required for video playbak")
    video_functions_parser.add_argument("output_folder", type=str, help="The path to the folder in which the video functions will be written")
    video_functions_parser.add_argument("amount_of_frames", type=int, help="The amount of frames that were generated previously")
    video_functions_parser.add_argument("-d","--datapack-name", type=str, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    video_functions_parser.add_argument("-p","--name-prefix", type=str, default="video_", dest="name_prefix", help="the name prefix of the frames that should have been generated beforehand")
    video_functions_parser.add_argument("-m","--max-commands", type=int, default=25, dest="max_commands", help="The maximum amount of commands per generated function file, too many commands in a single function may impact performance. The less commands per function file, the more files will be generated")
    video_functions_parser.add_argument("-t", "--ticks-per-frame", type=int, default=2, dest="ticks_per_frame", help="How many game ticks between every frame. If the number is different that the one used to generate the frames, the video will be sped up or slowed down")

    #(output_folder: str, datapack_name: str, sound_name_prefix: str, sound_duration: float, first_index: int, final_index: int, max_commands: int = 25)
    audio_functions_parser = functions_parsers.add_parser("audio", help="Generate the functions required for audio playbak")
    audio_functions_parser.add_argument("output_folder", type=str, help="The path to the folder in which the audio functions will be written")
    audio_functions_parser.add_argument("amount_of_sound_files", type=int, help="The amount of previously generated sound files")
    audio_functions_parser.add_argument("-n","--datapack-name", type=str, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    audio_functions_parser.add_argument("-p","--name-prefix", type=str, default="audio_", dest="name_prefix", help="The name prefix of the audio files that should have been generated beforehand")
    audio_functions_parser.add_argument("-d","--sound-duration", type=float, default=60, dest="sound_duration", help="The duration in seconds of the previously generated sound files")
    audio_functions_parser.add_argument("-m","--max-commands", type=int, default=25, dest="max_commands", help="The maximum amount of commands per generated function file, too many commands in a single function may impact performance. The less commands per function file, the more files will be generated")

    #(output_folder: str, datapack_name: str, control_audio: bool = False)
    playback_control_functions_parser = functions_parsers.add_parser("playback-control", help="Generate the functions required for controlling the video and audio playback")
    playback_control_functions_parser.add_argument("output_folder", type=str, help="The path to the folder in which the playback control functions will be written")
    playback_control_functions_parser.add_argument("-d","--datapack-name", type=str, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    playback_control_functions_parser.add_argument("-a","--control-audio", action="store_true", default=False, dest="control_audio", help="If present, the functions will be able to control the audio playback aswell, if the datapack uses no audio, enabling this option will break the playback control")

    #parser.add_argument("-nv", "--no-video", help="doesn't convert the video to any format", action="store_true")
    args = parser.parse_args()

    if args.command is None:
        parser.print_usage()

    elif args.command == "video":
        pass

    elif args.command == "resourcepack":
        if args.subcommand is None:
            resourcepak_parser.print_usage()
        elif args.subcommand == "audio":
            pass
        elif args.subcommand == "json":
            pass

    elif args.command == "functions":
        if args.subcommand is None:
            functions_parser.print_usage()
        elif args.subcommand == "video":
            pass
        elif args.subcommand == "audio":
            pass
        elif args.subcommand == "playback-control":
            pass

if __name__ == "__main__":
    main()