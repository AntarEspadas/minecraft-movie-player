import unittest
import os
import minecraft_movie_player.structure_block as structure_block

class StructureBlocksTest(unittest.TestCase):

    redstone = "minecraft:redstone_block"
    dirt = "minecraft:dirt"
    stone = "minecraft:stone"
    hay = "minecraft:hay_block"
    chest = "minecraft:chest"
    
    def setUp(self):
        self._sizes = (20,20,20)
        self._structure = structure_block.StructureBlock(self._sizes)

    def test_size(self):
        
        size = self._structure._size
        self.assertTupleEqual((size[0], size[1], size[2]),self._sizes)

    def test_setblock(self):
        inputs = [
            ((10,10,10), self.stone),
            ((19,12,13), self.dirt),
            ((8,5,7), "minecraft:air"),
            ((10,10,10), self.stone),
            ((10,10,11), self.stone),
            ((10,11,10), "minecraft:air"),
            ((11,10,10), self.dirt),
        ]
        for coordinates, block_id in inputs:
            x, y, z = coordinates
            block_identifier = block_id, None
            self._structure.setblock(coordinates,block_id)
            self.assertTrue(block_identifier in self._structure._palette)
            self.assertEqual(self._structure._blocks[x][y][z]["state"], self._structure._palette[block_identifier])

    def test_save_file(self):
        blocks = [
            ((0,0,0),self.redstone,None,None),
            ((0,0,1),self.redstone,None,None),
            ((0,0,2),self.redstone,None,None),
            ((0,0,1),self.redstone,None,None),
            ((0,1,0),self.stone,None,None),
            ((0,1,1),self.stone,None,None),
            ((0,1,2),self.stone,None,None),
            ((0,1,3),self.stone,None,None),
            ((0,2,0),self.dirt,None,None),
            ((0,2,1),self.dirt,None,None),
            ((0,2,2),self.dirt,None,None),
            ((0,2,3),self.dirt,None,None),
            ((0,3,0),self.hay,"{axis:'x'}",None),
            ((0,3,1),self.hay,"{axis:'y'}",None),
            ((0,3,2),self.hay,"{axis:'z'}",None),
            ((0,4,0),self.chest,"{facing:'north'}","{Items:[{Count:1b,id:'%s',Slot:0b}]}" % self.redstone),
            ((0,4,1),self.chest,"{facing:'east'}","{Items:[{Count:1b,id:'%s',Slot:1b}]}" % self.stone),
            ((0,4,2),self.chest,"{facing:'south'}","{Items:[{Count:1b,id:'%s',Slot:2b}]}" % self.dirt),
        ]
        for coordinates, block_id, state, nbt in blocks:
            self._structure.setblock(coordinates, block_id, state, nbt)
        self._structure.save(os.path.join("tests","output","nbt-test.nbt"))

    def test_summon(self):
        self._structure = structure_block.StructureBlock((1,1,1))
        self._structure.summon((0.5,0.5,0.5),"minecraft:armor_stand")
        self._structure.save(os.path.join("tests","output","nbt-entity-test.nbt"))


if __name__ == "__main__":
    unittest.main()

