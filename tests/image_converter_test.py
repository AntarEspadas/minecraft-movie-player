import unittest
from context import image_converter

class ImageConverterTests(unittest.TestCase):

    def test_get_tree(self):
        image_converter.__get_palette("D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\palette.txt")

if __name__ == "__main__":
    unittest.main()