from nbt import nbt

class Structure():

    data_version = nbt.TAG_Int(2230,"DataVersion")

    def __init__(self, width: int, height: int, depth: int):
        self._width = width
        self._file = nbt.NBTFile()

if __name__ == "__main__":
    structure = Structure(10,10,10)
    print(structure._width)