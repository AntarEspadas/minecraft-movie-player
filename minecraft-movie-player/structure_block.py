import nbtlib as nbt

class StructureBlock():
    data_version = nbt.Int(2578)

    def __init__(self, dimentions: tuple):

        self._size = nbt.List[nbt.Int](list(dimentions))

        x, y, z = dimentions
        self._blocks = [[[None for k in range(z)] for j in range(y)] for i in range(x)]

        self._entities = nbt.List[nbt.Compound]()

        self._palette = {}

    def setblock(self, coordinates: tuple, block_id: str, block_state: str = None, tile_entity_nbt: str = None):
        block_identifier = block_id , block_state
        if block_identifier not in self._palette:
            self._palette[block_identifier] = len(self._palette)
        x, y, z = coordinates
        block = self._blocks[x][y][z] = nbt.Compound()
        block["state"] = nbt.Int(self._palette[block_identifier])
        if tile_entity_nbt is not None:
            block["nbt"] = nbt.parse_nbt(tile_entity_nbt)

    def summon(self, coordinates: tuple, entity_id: str, entity_nbt: str = None):
        entity = nbt.Compound()
        if entity_nbt is None:
            entity["nbt"] = nbt.Compound()
        else:
            entity["nbt"] = nbt.parse_nbt(entity_nbt)
        entity["nbt"]["id"] = nbt.String(entity_id)
        entity["blockPos"] = nbt.List[nbt.Int]([int(i) for i in coordinates])
        entity["pos"] = nbt.List[nbt.Double](list(coordinates))
        self._entities.append(entity)

    def save(self, file_path: str, empty_block: str = None):
        root = nbt.Compound()
        root["blocks"]          = self.__get_blocks(empty_block)
        root["entities"]        = self._entities
        root["palette"]         = self.__get_palette()
        root["size"]            = self._size
        root["DataVersion"]    = self.data_version
        file = nbt.File({"":root})
        file.save(file_path,gzipped=True)
    
    def __get_palette(self):
        values = [None] * len(self._palette)
        for block_identifier, index in self._palette.items():
            compound = nbt.Compound()
            compound["Name"] = nbt.String(block_identifier[0])
            if block_identifier[1] is not None:
                compound["Properties"] = nbt.parse_nbt(block_identifier[1])
            values[index] = compound
        palette = nbt.List[nbt.Compound](values)
        return palette

    def __get_blocks(self, empty_block):
        generate_block = self.__get_block_generator(empty_block)
        blocks = nbt.List[nbt.Compound]()
        for x, slice2d in enumerate(self._blocks):
            for y, slice1d in enumerate(slice2d):
                for z, block in enumerate(slice1d):
                    generate_block((x,y,z), block, blocks)
        return blocks

    def __get_block_generator(self, empty_block):

        def append_block(coordinates: tuple, block: nbt.Compound, block_list: list):
            pos = nbt.List[nbt.Int](list(coordinates))
            block["pos"] = pos
            block_list.append(block)
        
        def  no_empty_block_generator(coordinates: tuple, block: nbt.Compound, block_list: list):
            if block is None:
                return
            append_block(coordinates, block, block_list)
        
        if empty_block is None:
            return no_empty_block_generator
        empty_block_identifier = empty_block, None
        if empty_block_identifier not in self._palette:
            self._palette[empty_block_identifier] = len(self._palette)
        empty_block_index = self._palette[empty_block_identifier]
        
        def empty_block_generator(coordinates: tuple, block: nbt.Compound, block_list: list):
            if block is None:
                block = nbt.Compound({
                    "state": nbt.Int(empty_block_index)
                })
            append_block(coordinates, block, block_list)

        return empty_block_generator
