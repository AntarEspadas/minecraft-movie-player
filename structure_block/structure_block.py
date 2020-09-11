import python_nbt.nbt as nbt

class StructureBlock():
    data_version = nbt.NBTTagInt(value=2578)

    def __init__(self, dimentions: tuple):

        self._size = nbt.NBTTagList(tag_type=nbt.NBTTagInt, value=[nbt.NBTTagInt(i) for i in dimentions])

        x, y, z = dimentions
        self._blocks = [[[None for k in range(z)] for j in range(y)] for i in range(x)]

        self._entities = nbt.TAG_List(tag_type=nbt.NBTTagCompound)

        self._palette = {}

    def setblock(self, coordinates: tuple, block_id: str, block_state: str = None, tile_entity_nbt: str = None):
        if block_id not in self._palette:
            self._palette[block_id] = len(self._palette)
        x, y, z = coordinates
        self._blocks[x][y][z] = self._palette[block_id]

    def save(self, file_path: str, empty_block: str = None):
        root = nbt.NBTTagCompound()
        root["blocks"]          = self.__get_blocks(empty_block)
        root["entities"]        = self._entities
        root["palette"]         = self.__get_palette()
        root["size"]            = self._size
        root["data_version"]    = self.data_version
        nbt.write_to_nbt_file(file_path,root)
    
    def __get_palette(self):
        values = [None] * len(self._palette)
        for block_id, index in self._palette.items():
            compound = nbt.NBTTagCompound()
            compound["name"] = nbt.NBTTagString(value=block_id)
            values[index] = compound
        palette = nbt.NBTTagList(tag_type=nbt.NBTTagCompound,value=values)
        return palette

    def __get_blocks(self, empty_block):
        generate_block = self.__get_block_generator(empty_block)
        blocks = nbt.NBTTagList(tag_type=nbt.NBTTagCompound)
        for x, slice2d in enumerate(self._blocks):
            for y, slice1d in enumerate(slice2d):
                for z, state in enumerate(slice1d):
                    generate_block((x,y,z), state, blocks)
        return blocks

    def __get_block_generator(self, empty_block):

        def append_block(coordinates: tuple, state: int, block_list: list):
            pos = nbt.TagList(tag_type=nbt.NBTTagInt, value=[nbt.NBTTagInt(i) for i in coordinates])
            compound = nbt.NBTTagCompound()
            compound["pos"]     = pos
            compound["state"]   = nbt.NBTTagInt(value=int(state))
            block_list.append(compound)
        
        def  no_empty_block_generator(coordinates: tuple, state: int, block_list: list):
            if state == None:
                return
            append_block(coordinates, state, block_list)
        
        if empty_block is None:
            return no_empty_block_generator
        if empty_block not in self._palette:
            self._palette[empty_block] = len(self._palette)
        empty_block_index = self._palette[empty_block]
        
        def empty_block_generator(coordinates: tuple, state: int, block_list: list):
            if state == None:
                state = empty_block_index
            append_block(coordinates, state, block_list)

        return empty_block_generator

if __name__ == "__main__":
    structure = StructureBlock((5,5,5))