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
        block_id = "minecraft:air"
        coordinates = (10,10,10)
        self._structure.setblock(coordinates,block_id)
        self.assertTrue(block_id in self._structure._palette)
        self.assertEqual(self._structure._blocks[(10,10,10)], self._structure._palette[block_id])

if __name__ == "__main__":
    unittest.main()
