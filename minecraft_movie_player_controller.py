
def video(path_to_video: str, path_to_output_folder: str, path_to_palette: str, name_prefix: str, ticks_per_frame: str, width: int, height: int, adjust_mode: str, unoptimized: bool, subprocesses: int):
    import image_converter as ic
    ic.video_to_structure(path_to_video, path_to_output_folder, name_prefix, path_to_palette, ticks_per_frame, 0, width, height, adjust_mode, not unoptimized, subprocesses)

def resourcepack_audio(path_to_audio: str, path_to_output_folder: str, split_size: float, name_prefix: str):
    import player_resourcepack as pr
    pr.split_and_convert(path_to_audio, path_to_output_folder, name_prefix, split_size)

def resourcepack_json(output_folder: str, amount_of_sound_files: int, name_prefix: str, subfolder_name: str):
    import player_resourcepack as pr
    pr.create_sounds_json(output_folder, subfolder_name, amount_of_sound_files, name_prefix)

def functions_video(output_folder: str, amount_of_frames: int, datapack_name: str, name_prefix: str, max_commands: int, ticks_per_frame: int):
    import player_functions as pf
    final_index = amount_of_frames - 1
    pf.generate_structure_functions(output_folder, datapack_name, name_prefix, 0, final_index, max_commands, ticks_per_frame)

def functions_audio(output_folder: str, amount_of_sound_files: int, datapack_name: str, name_prefix: str, sound_duration: float, max_commands: int):
    import player_functions as pf
    final_index = amount_of_sound_files - 1
    pf.generate_audio_functions(output_folder, datapack_name, name_prefix, sound_duration, 0, final_index, max_commands)

def functions_playback_control(output_folder: str, datapack_name: str, control_audio: bool):
    import player_functions as pf
    pf.generate_playback_control_functions(output_folder, datapack_name, control_audio)