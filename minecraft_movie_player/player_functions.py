
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
                _write_primary_audio_function(output_folder, datapack_name, sound_name_prefix, first_index, last_index, file_amount == 1)
            else:
                _write_secondary_audio_function(output_folder, datapack_name, first_index, last_index, step, file_amount == 1)
    
    _write_setup_audio_function(output_folder, datapack_name)
    _write_main_audio_function(output_folder, datapack_name, sound_duration)
    _write_stopsound(output_folder, sound_name_prefix, first_index, final_index)

def generate_playback_control_functions(output_folder: str, datapack_name: str, control_audio: bool = False):
        play = open(os.path.join(output_folder, "play.mcfunction"),"w+")
        play.write(f"tag @e[name={datapack_name}_screen] add play")
        play.close()

        pause = open(os.path.join(output_folder, "pause.mcfunction"),"w+")
        if control_audio:
            pause.write(f"function {datapack_name}:stopsound\n")
        pause.write(f"tag @e[name={datapack_name}_screen] remove play")
        pause.close()

        restart = open(os.path.join(output_folder, "restart.mcfunction"),"w+")
        commands = []
        if control_audio:
            commands += f"function {datapack_name}:stopsound",
            commands += f"scoreboard players set @e[name={datapack_name}_screen] {datapack_name}_am -1",
            commands += f"scoreboard players set @e[name={datapack_name}_screen] {datapack_name}_at -1",
        commands += f"scoreboard players set @e[name={datapack_name}_screen] {datapack_name}_vm -1",
        commands += f"scoreboard players set @e[name={datapack_name}_screen] {datapack_name}_vt -1",
        commands += f"tag @e[name={datapack_name}_screen] add play",
        restart.write("\n".join(commands))
        restart.close()


def _write_stopsound(output_folder: str, sound_name_prefix: str, first_index: int, last_index: int):
    function = open(os.path.join(output_folder, "stopsound.mcfunction"), "w+")

    command = 'stopsound @a * %s'

    for i in range(first_index, last_index + 1):
        function.write(command % f'{sound_name_prefix}{i}\n')

    function.close()

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

    commands += f'#{datapack_name}',
    commands += '#Do not change the first line of this file',
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, tag=play] %s_am 1' % ((datapack_name,) * 2),
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_am=%d..}] %s_am 0' % (datapack_name, datapack_name, ticks, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_am=0}, tag=play] %s_at 1' % ((datapack_name,) * 3),
    commands += 'execute as @e[type=armor_stand, name=%s_screen, scores={%s_am=0}, tag=play] at @s run function %s:audio_root' % ((datapack_name,) * 3),

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

    commands += f'#{datapack_name}',
    commands += '#Do not change the first line of this file',
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, tag=play] %s_vm 1' % ((datapack_name,) * 2),
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_vm=%d..}] %s_vm 0' % (datapack_name, datapack_name, ticks_per_frame, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}, tag=play] %s_vt 1' % ((datapack_name,) * 3),
    commands += 'execute as @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}, tag=play] at @s run function %s:video_root' % ((datapack_name,) * 3),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}, tag=play] run setblock ~ ~ ~ stone' % ((datapack_name,) * 2),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_vm=0}, tag=play] run setblock ~ ~ ~ redstone_block' % ((datapack_name,) * 2),

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
    execute = f'execute'
    condition = f'if score @s {datapack_name}_at matches {index}'
    command = f'run playsound {sound_name_prefix}{index} record @a ~ ~ ~ 10'
    return f"{execute} {condition} {command}\n"

def _get_secondary_audio_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute'
    condition = f'if score @s {datapack_name}_at matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:audio_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"

def _get_primary_video_command(datapack_name: str, filename_prefix: str, index: int):
    execute = f'execute'
    condition = f'if score @s {datapack_name}_vt matches {index}'
    command = 'run data merge block ~ ~-1 ~ {name:"%s:%s%s"}' % (datapack_name, filename_prefix, index)
    return f"{execute} {condition} {command}\n"

def _get_secondary_video_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute'
    condition = f'if score @s {datapack_name}_vt matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:video_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"


def _calculate_layers(first_index: int, final_index: int, max_commands: int) -> list:
    command_amount = final_index - first_index + 1
    if command_amount == 1:
        return [1]
    return [math.ceil(command_amount / max_commands ** (i+1)) for i in range(math.ceil(math.log(command_amount, max_commands)))]

generate_audio_functions("D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\rickroll_cut", "test", "audio_", 60, 0, 0, 50)