import warnings
import os
import json


def split_and_convert(input_file: str, output_folder: str, name_prefix: str, segment_duration: float) -> int:
    warnings.filterwarnings("error")
    try:
        import pydub
    except RuntimeWarning:
        print("Could not find ffmpeg or avconv installation, either of them is required for this part of the script to work")
        return None
    finally:
        warnings.filterwarnings("default")


    audio = pydub.AudioSegment.from_file(input_file)
    i = 0
    while i * segment_duration < audio.duration_seconds:
        segment = audio[i * segment_duration * 1000: (i + 1) * segment_duration * 1000]
        segment.export(os.path.join(output_folder, name_prefix + str(i)), "ogg", "vorbis")
        i += 1
    return i

def create_sounds_json(out_file: str, subfolder_name: str, sound_files_amount: int, name_prefix: str, merge_contents = True):
    if merge_contents:
        sounds_file = open(out_file, "r")
        sounds_json = json.load(sounds_file)
        sounds_file.close()
    else:
        sounds_json = {}
    
    for i in range(sound_files_amount):
        name = f"{subfolder_name}%s{name_prefix}{i}"
        sounds_json[name % "."] = {"sounds":[{"name": name % "/", "stream": True}]}

    sounds_file = open(out_file, "w+")
    json.dump(sounds_json, sounds_file, indent = 2)
    sounds_file.close()