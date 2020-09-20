
import math
import os

def generate_structure_functions(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands):
    command_amount = final_index - first_index + 1

    layers = [max_commands ** i for i in range(math.ceil(math.log(command_amount, max_commands)))]

    for file_number in range(layers[-1]):
        first_index = file_number * max_commands
        last_index = (file_number + 1) * max_commands - 1
        _write_primary_function(output_folder, datapack_name, filename_prefix, first_index, min(last_index, final_index), layers[-1] == 1)
    
    for file_amount in layers[:-1]:
        step = math.ceil(math.ceil(command_amount / file_amount) / max_commands)
        for file_number in range(file_amount):
            first_index = file_number * step * max_commands
            last_index = (file_number + 1) * step *max_commands - 1
            _write_secondary_function(output_folder, datapack_name, first_index, min(last_index, final_index), step, file_amount == 1)


    """#Divide loop into two
    for depth, files in enumerate(layers):
        interval = max_commands * layers[-depth -1]
        for file in range(files):
            first = file * interval
            last = min((file +  1) * interval - 1, final_index)
            _write_function(output_folder, first, last, datapack_name, filename_prefix, layers, depth, interval)"""

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
        function.write(_get_secondary_command(datapack_name, i, i + step -1))
    function.close()


def _get_structure_command(datapack_name: str, filename_prefix: str, index: int):
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_ticks matches {index}'
    command = 'run data merge block ~ ~-1 ~ {name:"%s:%s_%s"}' % (datapack_name, filename_prefix, index)
    return f"{execute} {condition} {command}\n"

def _get_secondary_command(datapack_name: str, first_index: int, last_index: int):
    execute = f'execute as @e[type=armor_stand, name="{datapack_name}_screen"]'
    condition = f'if score @s {datapack_name}_ticks matches {first_index}..{last_index}'
    command = f'run function {datapack_name}:animations/animation_{first_index}-{last_index}'
    return f"{execute} {condition} {command}\n"

if __name__ == "__main__":
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\function_testing"
    generate_structure_functions(output_folder,"test","test", 0, 999, 10)