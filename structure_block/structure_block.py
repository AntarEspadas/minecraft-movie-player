from nbt import nbt
import numpy

class StructureBlock():

    data_version = nbt.TAG_Int(2578,"DataVersion")

    def __init__(self, dimentions: tuple):

        self._file = nbt.NBTFile()

        self._size = nbt.TAG_List(type=nbt.TAG_Int, name="size")
        for dimention in dimentions:
            self._size.tags.append(nbt.TAG_Int(dimention))

        self._blocks = numpy.empty(dimentions)
        self._blocks.fill(-1)

        self._entities = nbt.TAG_List(type=nbt.TAG_Compound, name="entities")

        self._palette = {}

    def setblock(self, coordinates: tuple, block_id: str):
        if block_id not in self._palette:
            self._palette[block_id] = len(self._palette)
        self._blocks[coordinates] = self._palette[block_id]

    def save(self, file_path: str, empty_block: str = None):
        self._file.tags = [
            self.__get_blocks(empty_block),
            self._entities,
            self.__get_palette(),
            self._size,
            self.data_version
        ]
        """,
            
            """
        self._file.write_file(file_path)
    
    def __get_palette(self):
        palette = nbt.TAG_List(type=nbt.TAG_Compound, name="palette")
        palette.tags = [None] * len(self._palette)
        for block_id, index in self._palette.items():
            compound = nbt.TAG_Compound()
            compound.tags.append(nbt.TAG_String(value=block_id, name="Name"))
            palette.tags[index] = compound
        return palette

    def __get_blocks(self, empty_block):
        generate_block = self.__get_block_generator(empty_block)
        blocks = nbt.TAG_List(type=nbt.TAG_Compound, name="blocks")
        for x, slice2d in enumerate(self._blocks):
            for y, slice1d in enumerate(slice2d):
                for z, state in enumerate(slice1d):
                    generate_block((x,y,z), state, blocks.tags)
        return blocks

    def __get_block_generator(self, empty_block):

        def append_block(coordinates: tuple, state: int, block_list: list):
            pos = nbt.TAG_List(name="pos", type=nbt.TAG_Int)
            pos.tags = [nbt.TAG_Int(value=i) for i in coordinates]
            compound = nbt.TAG_Compound()
            compound.tags = [
                #nbt.TAG_List(value=[nbt.TAG_Int(20)], type=nbt.TAG_Int, name="pos"),
                pos,
                nbt.TAG_Int(value=int(state), name="state")
            ]
            block_list.append(compound)
        
        def  no_empty_block_generator(coordinates: tuple, state: int, block_list: list):
            if state == -1:
                return
            append_block(coordinates, state, block_list)
        
        if empty_block is None:
            return no_empty_block_generator
        if empty_block not in self._palette:
            self._palette[empty_block] = len(self._palette)
        empty_block_index = self._palette[empty_block]
        
        def empty_block_generator(coordinates: tuple, state: int, block_list: list):
            if state == -1:
                state = empty_block_index
            append_block(coordinates, state, block_list)

        return empty_block_generator

if __name__ == "__main__":
    pass