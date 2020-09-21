
import math
import os

def generate_structure_functions(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands: int = 25, ticks_per_frame: int = 2):
    #audio duration * 20 / ticks_per_frame 
    
    layers = _calculate_layers(first_index, final_index, max_commands)

    for power, file_amount in enumerate(layers):
        step = max_commands ** power
        for file_number in range(file_amount):
            first_index = file_number * step * max_commands
            last_index = (file_number + 1) * step * max_commands - 1
            if power == 0:
                _write_primary_function(output_folder, datapack_name, filename_prefix, first_index, min(last_index, final_index), file_amount == 1)
            else:
                _write_secondary_function(output_folder, datapack_name, first_index, min(last_index, final_index), step, file_amount == 1)

    _write_setup_video_function(output_folder, datapack_name)
    _write_main_video_function(output_folder, datapack_name, ticks_per_frame)

def generate_audio_functions(output_folder: str, datapack_name: str, sound_name: str, sound_duration: str, first_index: int, final_index: int, max_commands: int = 25):
    
    layers = _calculate_layers(first_index, final_index, max_commands)

    for power, file_amount in enumerate(layers):
        step = max_commands ** power
        for file_number in range(file_amount):
            first_index = file_number * step * max_commands
            last_index = (file_number + 1) * step * max_commands - 1

def _write_setup_video_function(output_folder: str, datapack_name: str):
    function = open(os.path.join(output_folder, "setup_video.mcfunction"), "w+")
    
    commands = []

    commands += f"scoreboard objectives add {datapack_name}_vm dummy",
    commands += f"scoreboard objectives add {datapack_name}_vt dummy",
    commands += 'setblock ~ ~ ~ minecraft:structure_block{mode: "LOAD", showboundingbox: 0b, posX: 1, posY: 0}',
    commands += 'summon minecraft:armor_stand ~ ~1 ~ {CustomName:\'{"text":"%s_screen"}\'}' % datapack_name,

    function.write("\n".join(commands))
    function.close()

def _write_main_video_function(output_folder: str, datapack_name: str, ticks_per_frame: int, with_audio = False):
    function = open(os.path.join(output_folder, "main_video.mcfunction"), "w+")

    commands = []

    commands += f'scoreboard players add @e[type=armor_stand, name={datapack_name}_screen] {datapack_name}_vm 1',
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_vm=%d..}] %s_vm 0' % (datapack_name, datapack_name, ticks_per_frame, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}] %s_vt 1' % ((datapack_name,) * 3),
    commands += f'function {datapack_name}:video_root',
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vt=0..}] run setblock ~ ~ ~ stone' % ((datapack_name,) * 2),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vt=0..}] run setblock ~ ~ ~ redstone_block' % ((datapack_name,) * 2),

    function.writelines("\n".join(commands))
    function.close()

def _write_primary_function(folder: str, datapack_name: str, filename_prefix: str, first_index: int, last_index: int, is_root = False, score_suffix: str = None, command: str = None):
    filename = "video_root.mcfunction" if is_root else f"video_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1):
        function.write(_get_primary_command(datapack_name, filename_prefix, i, score_suffix, command))
    function.close()

def _write_secondary_function(folder: str, datapack_name: str, first_index: int, last_index: int, step: int, is_root = False):
    filename = "video_root.mcfunction" if is_root else f"video_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1, step):
        function.write(_get_secondary_command(datapack_name, i, min(i + step -1, last_index)))
    function.close()


def _get_primary_command(datapack_name: str, filename_prefix: str, index: int, score_suffix: str = None, command: str = None):
    score_suffix = score_suffix if score_suffix is not None else "vt"
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_{score_suffix} matches {index}'
    command = command if command is not None else 'run data merge block ~ ~-1 ~ {name:"%s:%s%s"}' % (datapack_name, filename_prefix, index)
    command.replace("%d",str(index))
    return f"{execute} {condition} {command}\n"

def _get_secondary_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute as @e[type=armor_stand, name="{datapack_name}_screen"]'
    condition = f'if score @s {datapack_name}_vt matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:video_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"

def _calculate_layers(first_index: int, final_index: int, max_commands: int) -> list:
    command_amount = final_index - first_index + 1
    return [math.ceil(command_amount / max_commands ** (i+1)) for i in range(math.ceil(math.log(command_amount, max_commands)))]

if __name__ == "__main__":
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\function_testing"
    generate_structure_functions(output_folder,"testpack","rickroll_", 0, 847, 10, 5)