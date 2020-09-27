
def video(path_to_video: str, path_to_output_folder: str, path_to_palette: str, name_prefix: str, ticks_per_frame: str, width: int, height: int, unoptimized: bool):
    print(path_to_video, path_to_output_folder, path_to_palette, name_prefix, ticks_per_frame, width, height, unoptimized, sep=", ")

def resourcepack_audio(path_to_audio: str, path_to_output_folder: str, split_size: float, name_prefix: str):
    print(path_to_audio, path_to_output_folder, split_size, name_prefix, sep=", ")

def resourcepack_json(output_folder: str, amount_of_sound_files: int, name_prefix: str, subfolder_name: str):
    print(output_folder, amount_of_sound_files, name_prefix, subfolder_name, sep=", ")

def functions_video(output_folder: str, amount_of_frames: int, datapack_name: str, name_prefix: str, max_commands: int, ticks_per_frame: int):
    print(output_folder, amount_of_frames, datapack_name, name_prefix, max_commands, ticks_per_frame, sep=", ")

def functions_audio(output_folder: str, amount_of_sound_files: int, datapack_name: str, name_prefix: str, sound_duration: float, max_commands: int):
    print(output_folder, amount_of_sound_files, datapack_name, name_prefix, sound_duration, max_commands, sep=", ")

def functions_playback_control(output_folder: str, datapack_name: str, control_audio: bool):
    print(output_folder, datapack_name, control_audio, sep=", ")