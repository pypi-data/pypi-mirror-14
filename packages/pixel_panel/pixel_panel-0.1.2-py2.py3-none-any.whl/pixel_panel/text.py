# -*- coding: utf-8 -*-
"""Functions for drawing text onto an image.
"""


def character(char, imagedraw, font, fill):
    """Draw the given character onto the given image.

    Args:
       char: the character to draw.

       imagedraw: the ImageDraw to modify.

       font: see the 'font' module - dictionary mapping characters to lines.

       fill: color to use while drawing lines.

    """
    for line in font[char]:
        imagedraw.line(line, fill=fill)
    return imagedraw
