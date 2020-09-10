from nbt import nbt
import numpy

class StructureBlock():

    data_version = nbt.TAG_Int(2230,"DataVersion")

    def __init__(self, dimentions: tuple):

        self._file = nbt.NBTFile()

        self._size = nbt.TAG_List(type=nbt.TAG_Int, name="size")
        for dimention in dimentions:
            self._size.tags.append(nbt.TAG_Int(dimention))

        self._blocks = numpy.zeros(dimentions)

        self._entities = nbt.TAG_List(type=nbt.TAG_Compound, name="entities")

        self._palette = {}

    def setblock(self, coordinates: tuple, block_id: str):
        if block_id not in self._palette:
            self._palette[block_id] = len(self._palette)
        self._blocks[coordinates] = self._palette[block_id]

if __name__ == "__main__":
    structure = StructureBlock(10,10,10)
    print(structure._width)