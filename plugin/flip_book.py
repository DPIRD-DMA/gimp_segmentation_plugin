#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Draw arrows in GIMP, using the selection as a guide for where to draw.
#
# Copyright 2010,2011 by Akkana Peck, http://www.shallowsky.com/software/
# plus contributions from Robert Brizard.
# You may use and distribute this plug-in under the terms of the GPL.

from gimpfu import *
# import gtk, pango
# from gobject import timeout_add
import glob
import os
# import numpy as np


def flip_images(image_dir,mask_dir):
    image_list = glob.glob(image_dir+"/*")
    one_image = image_list[0]
    file_name = os.path.basename(one_image)
    mask_path = os.path.join(mask_dir,file_name)
    # pdb.gimp_message(img.layers)

    img = gimp.Image(1000, 1000)
    pdb.gimp_display_new(img)
    for f, name, pos in ((one_image, "Image", 1), (mask_path, "Mask", 0)):
        layer = pdb.gimp_file_load_layer(img, f)
        pdb.gimp_layer_set_name(layer, name)
        pdb.gimp_image_insert_layer(img, layer, None, pos)
        pdb.gimp_message(img.layers)


    image = gimp.image_list()[0]
    active_layer = pdb.gimp_image_get_active_layer(image)
    pdb.gimp_layer_set_opacity(active_layer, 60)




register(
         "flip_images",
         "flip through a folder of images",
         "flip through a folder of images",
         "Nick Wright", "Nick Wright",
         "2021",
         "<Toolbox>/File/Flip through images",
         "",
         [
           (PF_DIRNAME, "image_dir", "Image folder:", None),
           (PF_DIRNAME, "mask_dir", "Maks folder:", None),

         ],
         [],
         flip_images)

main()
