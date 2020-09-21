
import math
import os

def generate_structure_functions(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands: int = 25, ticks_per_frame: int = 2):
    command_amount = final_index - first_index + 1

    layers = [math.ceil(command_amount / max_commands ** (i+1)) for i in range(math.ceil(math.log(command_amount, max_commands)))]

    #layers.reverse()

    for file_number in range(layers[0]):
        first_index = file_number * max_commands
        last_index = (file_number + 1) * max_commands - 1
        _write_primary_function(output_folder, datapack_name, filename_prefix, first_index, min(last_index, final_index), layers[0] == 1)
    
    for power, file_amount in enumerate(layers[1:]):
        power += 1
        step = max_commands ** power#math.ceil(math.ceil(command_amount / file_amount) / max_commands)
        for file_number in range(file_amount):
            first_index = file_number * step * max_commands
            last_index = (file_number + 1) * step *max_commands - 1
            _write_secondary_function(output_folder, datapack_name, first_index, min(last_index, final_index), step, file_amount == 1)

    _write_setup_function(output_folder, datapack_name)
    _write_main_function(output_folder, datapack_name, ticks_per_frame)

def _write_setup_function(output_folder: str, datapack_name: str):
    function = open(os.path.join(output_folder, "setup.mcfunction"), "w+")
    
    commands = []

    commands += f"scoreboard objectives add {datapack_name}_master dummy",
    commands += f"scoreboard objectives add {datapack_name}_ticks dummy",
    commands += 'setblock ~ ~ ~ minecraft:structure_block{mode: "LOAD", showboundingbox: 0b, posX: 1, posY: 0}',
    commands += 'summon minecraft:armor_stand ~ ~1 ~ {CustomName:\'{"text":"%s_screen"}\'}' % datapack_name,

    function.write("\n".join(commands))
    function.close()

def _write_main_function(output_folder: str, datapack_name: str, ticks_per_frame: int):
    function = open(os.path.join(output_folder, "main.mcfunction"), "w+")

    commands = []

    commands += f'scoreboard players add @e[type=armor_stand, name={datapack_name}_screen] {datapack_name}_master 1',
    commands += 'scoreboard players set @e[type=armor_stand, name=%s_screen, scores={%s_master=%d..}] %s_master 0' % (datapack_name, datapack_name, ticks_per_frame, datapack_name),
    commands += 'scoreboard players add @e[type=armor_stand, name=%s_screen, scores={%s_master=0}] %s_ticks 1' % ((datapack_name,) * 3),
    commands += f'function {datapack_name}:root',
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_ticks=0..}] run setblock ~ ~ ~ stone' % ((datapack_name,) * 2),
    commands += 'execute at @e[type=armor_stand, name=%s_screen, scores={%s_ticks=0..}] run setblock ~ ~ ~ redstone_block' % ((datapack_name,) * 2),

    function.writelines("\n".join(commands))
    function.close()

def _write_primary_function(folder: str, datapack_name: str, filename_prefix: str, first_index: int, last_index: int, is_root = False):
    filename = "root.mcfunction" if is_root else f"animation_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1):
        function.write(_get_structure_command(datapack_name, filename_prefix, i))
    function.close()

def _write_secondary_function(folder: str, datapack_name: str, first_index: int, last_index: int, step: int, is_root = False):
    filename = "root.mcfunction" if is_root else f"animation_{first_index}-{last_index}.mcfunction"
    function = open(os.path.join(folder, filename), "w+")
    for i in range(first_index, last_index + 1, step):
        function.write(_get_secondary_command(datapack_name, i, min(i + step -1, last_index)))
    function.close()


def _get_structure_command(datapack_name: str, filename_prefix: str, index: int):
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_ticks matches {index}'
    command = 'run data merge block ~ ~-1 ~ {name:"%s:%s%s"}' % (datapack_name, filename_prefix, index)
    return f"{execute} {condition} {command}\n"

def _get_secondary_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute as @e[type=armor_stand, name="{datapack_name}_screen"]'
    condition = f'if score @s {datapack_name}_ticks matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:animation_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"

if __name__ == "__main__":
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\function_testing"
    generate_structure_functions(output_folder,"testpack","rickroll_", 0, 847, 10, 5)