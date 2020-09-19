
import math
import os

def generate_structure_functions(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands):
    command_amount = final_index - first_index + 1

    layers = [max_commands ** i for i in range(math.ceil(math.log(command_amount, max_commands)))]

    #Divide loop into two
    for depth, files in enumerate(layers):
        interval = max_commands * layers[-depth -1]
        for file in range(files):
            first = file * interval
            last = min((file +  1) * interval - 1, final_index)
            _write_function(output_folder, first, last, datapack_name, filename_prefix, layers, depth, interval)

def _write_function(folder: str, start_index: int, end_index: int, datapack_name: str, filename_prefix, layers: list, depth: int, interval: int):
    filename = f"animation_{start_index}-{end_index}.mcfunction"
    filename = "root.mcfunction" if depth == 0 else filename
    function = open(os.path.join(output_folder, filename), "w+")
    if depth + 1 == len(layers):
        for i in range(start_index, end_index + 1):
            function.write(_get_command(datapack_name, filename_prefix, i))
    function.close()

def _get_command(datapack_name: str, filename_prefix: str, index: int):
    execute = f'execute as @e[type = armor_stand, name="{datapack_name}_screen"] at @s'
    condition = f'if score @s {datapack_name}_ticks matches {index}'
    command = 'run data merge block ~ ~-1 ~ {name:"%s:%s_%s"}' % (datapack_name, filename_prefix, index)
    return f"{execute} {condition} {command}\n"

def _get_function_caller(datapack_name: str, minimum, maximum):
    execute = f'execute as @e[type=armor_stand], name="{datapack_name}_screen"'
    condition = f'if score @s {datapack_name}_ticks matches {minimum}..{maximum}'
    command = f'run function {datapack_name}:animations/animation_{minimum}-{maximum}'
    return f"{execute} {condition} {command}"

if __name__ == "__main__":
    output_folder = "D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\function_testing"
    generate_structure_functions(output_folder,"test","test", 0, 999, 10)