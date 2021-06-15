#!/usr/bin/env python

# palette_from_image.py
# creates palette from image.
# Created by Tin Tran
# Comments directed to http://gimplearn.net
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.


import math
import string
#import Image
from gimpfu import *


def python_palette_from_image_tt(image, layer, palette_name,hor_colors, vert_colors ):
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()
	column_width = layer.width / hor_colors;
	row_height = layer.height / vert_colors;
	mid_offset_x = column_width / 2.0; #offset it so that we generally get the middle pixel.
	mid_offset_y = row_height / 2.0; #offset it so that we generally get the middle pixel.
	actual_name = pdb.gimp_palette_new(palette_name)
	for iy in range(0,int(vert_colors)):
		y = iy * row_height + mid_offset_y;
		for ix in range(0,int(hor_colors)):
			x = ix * column_width + mid_offset_x;
			num_channels,pixel = pdb.gimp_drawable_get_pixel(layer,x,y)
			pdb.gimp_palette_add_entry(actual_name,"Color " + str(iy*16+ix+1),pixel[0:3])
			pdb.gimp_message(type(pixel))
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()
    #return

register(
	"python_fu_palette_from_image_tt",
	"Generates a cross stitch pattern",
	"Generates a cross stitch pattern",
	"Tin Tran",
	"Tin Tran",
	"July 2018",
	"<Image>/Python-Fu/Palette from Image...",             #Menu path
	"RGB*, GRAY*",
	[
	(PF_STRING, "palette_name", "New palette name:", "A New Palette"),
	(PF_SPINNER, "hor_colors","# of horizontal colors (columns):", 16, (1, 256, 1)),
	(PF_SPINNER, "vert_colors","# of vertical colors (rows):", 16, (1, 256, 1)),
	],
	[],
	python_palette_from_image_tt)

main()
