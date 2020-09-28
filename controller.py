import os

def fil(value):
    if not os.path.isfile(value):
        raise ValueError(f"the file '{value}' does not exist")
    return value

def fold(value):
    if not os.path.isdir(value):
        raise ValueError(f"the folder '{value}' dose not exist")
    return value

def palette(value):
    pvalue = fil(value)
    from image_converter import _get_palette
    try:
        _get_palette(pvalue)
    except Exception:
        raise ValueError(f"Could not read the file '{pvalue}', make sure it is formatted properly")
    return pvalue

def filename(value):
    path = os.path.join(".", value)
    if not os.path.exists(path):
            try:
                with open(path, "x") as _:
                    pass
                os.remove(path)
            except OSError:
                raise ValueError(f"The name '{value}' contains invalida characters")
    return value

def mfilename(max_chars):
    def validate(value):
        fvalue = filename(value)
        if len(fvalue) > max_chars:
            raise ValueError(f"the name {value} is {len(value)} characters long, should be at most {max_chars}")
        return fvalue
    return validate

def mint(minimum, nullable: bool = False):
    def validate(value):
        if nullable and value is None:
            return value
        try:
            ivalue = int(value)
        except ValueError:
            raise ValueError(f"Should be an integer above {minimum}, not {value}")
        if ivalue <= minimum:
            raise ValueError(f"Should be an integer above {minimum}, not {value}")
        return ivalue
    return validate

def mfloat(minimum, nullable: bool = False):
    def validate(value):
        if nullable and value is None:
            return value
        try:
            fvalue = float(value)
        except ValueError:
            raise ValueError(f"Should be a number above {minimum}, not {value}")
        if fvalue <= minimum:
            raise ValueError(f"Should be a number above {minimum}, not {value}")
        return fvalue
    return validate

def vid(value):
    fvalue = fil(value)
    import cv2
    video = cv2.VideoCapture(fvalue)
    if not video.read()[0]:
        video.release()
        raise ValueError(f"the file '{fvalue}' is of an unknown format")
    video.release()
    return fvalue

def video(path_to_video: str, path_to_output_folder: str, path_to_palette: str, name_prefix: str, ticks_per_frame: str, width: int, height: int, adjust_mode: str, unoptimized: bool, subprocesses: int):
    import image_converter as ic
    if width is None and height is None:
        width = 75
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

def make(containing_folder: str, subflder_name: str):
    import player_maker as pm
    pm.make(containing_folder, subflder_name)