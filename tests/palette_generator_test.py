import unittest
from os.path import join
import minecraft_movie_player.palette_generator as palette_generator

class PaletteGeneratorTest(unittest.TestCase):
     
    out_folder = join("tests", "output")
    data_folder = join("tests", "data")
    block_folder = join(data_folder, "block")

    def test_generate_index_template(self):
        palette_generator.generate_index_template(self.block_folder, join(self.out_folder, "index.txt"))
        palette_generator.generate_index_template(self.block_folder, join(self.out_folder, "index_no_ids.txt"), False)

    def test_generate_palette(self):
        palette_generator.generate_palette(self.block_folder, join(self.out_folder, "palette.txt"))
        palette_generator.generate_palette(self.block_folder, join(self.out_folder, "palette_from_index.txt"), join(self.data_folder, "index.txt"))

def main():
    import pathlib
    pathlib.Path(join("tests", "output")).mkdir(exist_ok=True)
    unittest.main()

if __name__ == "__main__":
    main()