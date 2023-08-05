# -*- coding: utf-8 -*-

"""Unit test for the 'text' module."""

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from pixel_panel import color
from pixel_panel import font
from pixel_panel import text


BLACK = ImageColor.getrgb(color.default_black)
WHITE = ImageColor.getrgb(color.default_white)
YELLOW = ImageColor.getrgb(color.default_yellow)


def test_character():
    image = Image.new(color.default_mode, (5, 7))

    imagedraw = ImageDraw.Draw(image)
    imagedraw = text.character(
        'A', imagedraw, font.default_small, color.default_white)
    assert BLACK == image.getpixel((0, 0))
    assert WHITE == image.getpixel((0, 1))
    assert WHITE == image.getpixel((0, 6))
    assert WHITE == image.getpixel((4, 4))

    imagedraw = ImageDraw.Draw(image)
    imagedraw = text.character(
        'A', imagedraw, font.default_small, color.default_yellow)
    assert YELLOW == image.getpixel((0, 1))


def test_dictionary():
    for char in font.default_small.iterkeys():
        image = Image.new(color.default_mode, (5, 7))
        imagedraw = ImageDraw.Draw(image)
        imagedraw = text.character(
            char, imagedraw, font.default_small, color.default_white)
        # testing that we don't fail while tryig to draw every character
        # assert that each character has at least one drawn pixel
        assert any((WHITE == image.getpixel((x, y))
                    for x in xrange(5) for y in xrange(7)))

if __name__ == "__main__":
    test_character()
