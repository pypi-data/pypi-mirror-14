import random

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

from palettable.colorbrewer.diverging import RdBu_11


class Wallpaper():

    def __init__(self, width=1600, height=900, cube_size=50,
                 filename="test.png", filetype="PNG"):
        self.width = width
        self.height = height
        self.cube_size = cube_size
        self.filename = filename
        self.filetype = filetype.upper()

    def next_color(self):
        return ImageColor.getrgb(random.choice(RdBu_11.hex_colors))

    def paint_cube(self, x, y):
        # get the color
        color = self.next_color()
        # calculate the position
        cube_pos = [x, y, x + self.cube_size, y + self.cube_size]
        # draw the cube
        draw = ImageDraw.Draw(im=self.image)
        draw.rectangle(xy=cube_pos, fill=color, outline=None)

    def paint_pattern(self):
        x = 0
        while x < self.width:
            y = 0
            while y < self.height:
                self.paint_cube(x, y)
                y += self.cube_size
            x += self.cube_size

    def paint(self):
        self.image = Image.new(mode="RGB", size=(self.width, self.height))
        self.paint_pattern()
        self.image.save(fp=self.filename, format=self.filetype)
