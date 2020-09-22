
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
                _write_primary_video_function(output_folder, datapack_name, filename_prefix, first_index, min(last_index, final_index), file_amount == 1)
            else:
                _write_secondary_video_function(output_folder, datapack_name, first_index, min(last_index, final_index), step, file_amount == 1)

    _write_setup_video_function(output_folder, datapack_name)
    _write_main_video_function(output_folder, datapack_name, ticks_per_frame)

def generate_audio_functions(output_folder: str, datapack_name: str, sound_name_prefix: str, sound_duration: float, first_index: int, final_index: int, max_commands: int = 25):
    
    layers = _calculate_layers(first_index, final_index, max_commands)

    for power, file_amount in enumerate(layers):
        step = max_commands ** power
        for file_number in range(file_amount):
            first_index = file_number * step * max_commands
            last_index = (file_number + 1) * step * max_commands - 1
            last_index = min(last_index, final_index)
            if power == 0:
                _write_primary_audio_function(output_folder, datapack_name, sound_name_prefix, first_index, last_index)
            else:
                _write_secondary_audio_function(output_folder, datapack_name, first_index, last_index, step, file_amount == 1)
    
    _write_setup_audio_function(output_folder, datapack_name)
    _write_main_audio_function(output_folder, datapack_name, sound_duration)



def _write_setup_audio_function(output_folder: str, datapack_name: str):
    function = open(os.path.join(output_folder, "setup_audio.mcfunction"), "w+")
    
    commands = []

    commands += f"scoreboard objectives add {datapack_name}_am dummy",
    commands += f"scoreboard objectives add {datapack_name}_at dummy",

    function.write("\n".join(commands))
    function.close()

def _write_main_audio_function(output_folder: str, datapack_name: str, sound_duration: int):
    function = open(os.path.join(output_folder, "main_audio.mcfunction"), "w+")

    ticks = sound_duration * 20

    commands = []

    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_am=0..}] %s_am 1' % ((datapack_name,) * 3),
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_am=%d..}] %s_am 0' % (datapack_name, datapack_name, ticks, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_am=0}] %s_at 1' % ((datapack_name,) * 3),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_am=0}] run function %s:audio_root' % ((datapack_name,) * 3),

    function.writelines("\n".join(commands))
    function.close()


def _write_setup_video_function(output_folder: str, datapack_name: str):
    function = open(os.path.join(output_folder, "setup_video.mcfunction"), "w+")
    
    commands = []

    commands += f"scoreboard objectives add {datapack_name}_vm dummy",
    commands += f"scoreboard objectives add {datapack_name}_vt dummy",
    commands += 'setblock ~ ~ ~ minecraft:structure_block{mode: "LOAD", showboundingbox: 0b, posX: 1, posY: 0}',
    commands += 'summon minecraft:armor_stand ~ ~1 ~ {CustomName:\'{"text":"%s_screen"}\'}' % datapack_name,

    function.write("\n".join(commands))
    function.close()

def _write_main_video_function(output_folder: str, datapack_name: str, ticks_per_frame: int):
    function = open(os.path.join(output_folder, "main_video.mcfunction"), "w+")

    commands = []

    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_vm=0..}] %s_vm 1' % ((datapack_name,) * 3),
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_vm=%d..}] %s_vm 0' % (datapack_name, datapack_name, ticks_per_frame, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}] %s_vt 1' % ((datapack_name,) * 3),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}] run function %s:video_root' % ((datapack_name,) * 3),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}] run setblock ~ ~ ~ stone' % ((datapack_name,) * 2),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}] run setblock ~ ~ ~ redstone_block' % ((datapack_name,) * 2),

    function.writelines("\n".join(commands))
    function.close()



def _write_primary_audio_function(folder: str, datapack_name: str, sound_name_prefix: str, first_index: int, last_index: int, is_root = False):
    filename = "audio_root.mcfunction" if is_root else f"audio_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1):
        function.write(_get_primary_audio_command(datapack_name, sound_name_prefix, i))
    function.close()

def _write_secondary_audio_function(folder: str, datapack_name: str, first_index: int, last_index: int, step: int, is_root = False):
    filename = "audio_root.mcfunction" if is_root else f"audio_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1, step):
        function.write(_get_secondary_audio_command(datapack_name, i, min(i + step -1, last_index)))
    function.close()

def _write_primary_video_function(folder: str, datapack_name: str, filename_prefix: str, first_index: int, last_index: int, is_root = False):
    filename = "video_root.mcfunction" if is_root else f"video_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1):
        function.write(_get_primary_video_command(datapack_name, filename_prefix, i))
    function.close()

def _write_secondary_video_function(folder: str, datapack_name: str, first_index: int, last_index: int, step: int, is_root = False):
    filename = "video_root.mcfunction" if is_root else f"video_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1, step):
        function.write(_get_secondary_video_command(datapack_name, i, min(i + step -1, last_index)))
    function.close()



def _get_primary_audio_command(datapack_name: str, sound_name_prefix: str, index: int):
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_at matches {index}'
    command = f'run playsound {sound_name_prefix}{index} record @a ~ ~ ~'
    return f"{execute} {condition} {command}\n"

def _get_secondary_audio_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute as @e[type=armor_stand, name="{datapack_name}_screen"]'
    condition = f'if score @s {datapack_name}_at matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:audio_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"

def _get_primary_video_command(datapack_name: str, filename_prefix: str, index: int):
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_vt matches {index}'
    command = 'run data merge block ~ ~-1 ~ {name:"%s:%s%s"}' % (datapack_name, filename_prefix, index)
    return f"{execute} {condition} {command}\n"

def _get_secondary_video_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute as @e[type=armor_stand, name="{datapack_name}_screen"]'
    condition = f'if score @s {datapack_name}_vt matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:video_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"


def _calculate_layers(first_index: int, final_index: int, max_commands: int) -> list:
    command_amount = final_index - first_index + 1
    return [math.ceil(command_amount / max_commands ** (i+1)) for i in range(math.ceil(math.log(command_amount, max_commands)))]

if __name__ == "__main__":
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\function_testing"
    #generate_structure_functions(output_folder,"testpack","rickroll_", 0, 847, 10, 5)
    generate_audio_functions(output_folder, "testpack", "testpack:rickroll_", 10, 0, 21, 10)