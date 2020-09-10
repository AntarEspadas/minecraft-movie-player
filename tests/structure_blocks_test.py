import unittest
from context import structure_block

class StructureBlocksTest(unittest.TestCase):
    
    def setUp(self):
        self._sizes = (25,25,25)
        self._structure = structure_block.StructureBlock(self._sizes)

    def test_size(self):
        
        size = self._structure._size
        self.assertTupleEqual((size[0].value, size[1].value, size[2].value),self._sizes)

    def test_setblock(self):
        inputs = [
            ((10,10,10), "minecraft:redstone_block"),
            ((19,12,13), "minecraft:dirt"),
            ((8,5,7), "minecraft:air"),
            ((10,10,10), "minecraft:stone"),
            ((10,10,11), "minecraft:stone"),
            ((10,11,10), "minecraft:air"),
            ((11,10,10), "minecraft:dirt"),
        ]
        for coordinates, block_id in inputs:
            self._structure.setblock(coordinates,block_id)
            self.assertTrue(block_id in self._structure._palette)
            self.assertEqual(self._structure._blocks[coordinates], self._structure._palette[block_id])
        
        self._structure.save("D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\nbt-test.dat")

if __name__ == "__main__":
    unittest.main()

