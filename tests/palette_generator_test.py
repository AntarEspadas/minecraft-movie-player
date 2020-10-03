import unittest
import os
import minecraft_movie_player.palette_generator as palette_generator

class PaletteGeneratorTest(unittest.TestCase):
     
     def test_generate_index_template(self):
         pass

def main():
    import pathlib
    pathlib.Path(os.path.join("tests", "output")).mkdir(exist_ok=True)
    unittest.main()

if __name__ == "__main__":
    main()