import unittest
import numpy
import cv2
import os
import minecraft_movie_player.image_converter as image_converter

class ImageConverterTests(unittest.TestCase):

    def test_get_tree(self):
        image_converter._get_palette(os.path.join("tests", "data", "palette.txt"))
    
    def test_resize(self):
        image = numpy.zeros((90,160))
        size = image_converter._get_image_size(image, width = 80)
        self.assertTupleEqual(size, (80,45))

        size = image_converter._get_image_size(image, height = 45)
        self.assertTupleEqual(size, (80,45))

        size = image_converter._get_image_size(image)
        self.assertTupleEqual(size, (160, 90))

        size = image_converter._get_image_size(image, width = 80, height= 45, adjust_mode = "fit")
        self.assertTupleEqual(size,(80,45))

        size = image_converter._get_image_size(image, width = 80, height= 45, adjust_mode = "fill")
        self.assertTupleEqual(size,(80,45))

        size = image_converter._get_image_size(image, width = 80, height= 100, adjust_mode = "fit")
        self.assertTupleEqual(size,(80,45))

        size = image_converter._get_image_size(image, width = 80, height= 100, adjust_mode = "fill")
        self.assertTupleEqual(size,(177,100))

    def test_get_adjuster(self):
        image = numpy.zeros((90,160))

        adjuster = image_converter._get_adjuster(image)
        self.assertEqual(adjuster.__name__, "nop")

        adjuster = image_converter._get_adjuster(image, 160, 90)
        self.assertEqual(adjuster.__name__, "nop")

        adjuster = image_converter._get_adjuster(image, 80, 45)
        self.assertEqual(adjuster.__name__, "resize_only")

        adjuster = image_converter._get_adjuster(image, 80, 100, adjust_mode = "fit")
        self.assertEqual(adjuster.__name__, "resize_and_pad")

        adjuster = image_converter._get_adjuster(image, 80, 100, adjust_mode = "fill")
        self.assertEqual(adjuster.__name__, "resize_and_crop")

    def test_adjust(self):
        output_folder = os.path.join("tests","output")
        image_path = os.path.join("tests", "data", "test_0.png")
        print(image_path)
        image = cv2.imread(image_path)

        self.assertIsNotNone(image)

        size = image_converter._get_image_size(image, width = 100)
        adjust = image_converter._get_adjuster(image, width = 100)
        self.assertEqual(adjust.__name__, "resize_only")
        cv2.imwrite(os.path.join(output_folder, "test_adjust_1.png"), adjust(image, size))

        size = image_converter._get_image_size(image, height = 100)
        adjust = image_converter._get_adjuster(image, height = 100)
        self.assertEqual(adjust.__name__, "resize_only")
        cv2.imwrite(os.path.join(output_folder, "test_adjust_2.png"), adjust(image, size))

        size = image_converter._get_image_size(image, 100, 100, "fit")
        adjust = image_converter._get_adjuster(image, 100, 100, "fit")
        self.assertEqual(adjust.__name__, "resize_and_pad")
        cv2.imwrite(os.path.join(output_folder, "test_adjust_3.png"), adjust(image, size))

        size = image_converter._get_image_size(image, 100, 100, "fill")
        adjust = image_converter._get_adjuster(image, 100, 100, "fill")
        self.assertEqual(adjust.__name__, "resize_and_crop")
        cv2.imwrite(os.path.join(output_folder, "test_adjust_4.png"), adjust(image, size))

def main():
    import pathlib
    pathlib.Path(os.path.join("tests", "output")).mkdir(exist_ok=True)
    unittest.main()

if __name__ == "__main__":
    main()