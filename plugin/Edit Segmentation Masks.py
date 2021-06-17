from gimpfu import *
import glob
import os
import gtk,gobject

class PyApp(gtk.Window):
    cur_img_num = 0 # the currnet displayed image
    img = None
    first_build = True # used to know if we need to set up a canvas

    def __init__(self):
        super(PyApp, self).__init__()

        # build gtk interface
        self.set_title("Edit Masks")
        self.set_size_request(200, 100)
        self.set_position(gtk.WIN_POS_CENTER)

        # build buttons
        btn_next = gtk.Button("Next")
        btn_prev = gtk.Button("Previous")

        btn_next.connect("clicked", self.load_next_image)
        btn_prev.connect("clicked", self.load_prev_image)
        # grey out buttons
        btn_next.set_sensitive(False)
        btn_prev.set_sensitive(False)

        btn_next.set_size_request(80, 40)
        btn_prev.set_size_request(80, 40)

        fixed = gtk.Fixed()
        # building progress bar
        self.pb = gtk.ProgressBar()
        self.pb.set_size_request(180, 30)
        self.pb.set_text("Progress")
        self.pb.set_fraction(0.0)
        # possition things
        fixed.put(self.pb,10,60)
        fixed.put(btn_next, 110, 10)
        fixed.put(btn_prev, 10, 10)

        # self.connect("destroy", gtk.main_quit)
        self.connect('destroy', self.finsh)

        self.add(fixed)
        self.show_all()
        self.set_keep_above(True)
        # force two popups on start to select images and mask folder
        PyApp.image_dir = self.open_file(open_title='Select image folder')
        # get image list from selected folder
        self.get_img_list()
        PyApp.mask_dir = self.open_file(open_title='Select coloured mask folder')
        # activate buttons
        btn_next.set_sensitive(True)
        btn_prev.set_sensitive(True)
        # build and load palette
        self.laod_palette()
        # load first image
        self.load_image()
        # update progress bar
        self.progress_timeout()

    def laod_palette(self):
        # find the folder with the palette file, this was made by the Jyputer script
        folder = os.path.dirname(PyApp.image_dir)
        # build fullpath
        palette_path = os.path.join(folder,'Palette.txt')
        # read in file
        with open(palette_path) as f:
            palette_lines = f.readlines()
        # place empty pallete into the GIMP interface
        PyApp.actual_name = pdb.gimp_palette_new('Image Segmentation')
        # place each colour into the pallete
        for colour in palette_lines:
            # convert string array into tuple
            rgb_colour = (tuple([int(x.strip()) for x in colour.split(' ')]))
            pdb.gimp_palette_add_entry(PyApp.actual_name,"Color x",rgb_colour)

    def progress_timeout(self):
        new_val = float(PyApp.cur_img_num+1)/float(PyApp.image_count)
        self.pb.set_fraction(new_val)
        self.pb.set_text(str(PyApp.cur_img_num+1)+' out of ' + str(PyApp.image_count))
        return True

# func to open folder selection dialog box
    def open_file(self,open_title):
        dlg = gtk.FileChooserDialog(open_title,
        None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dlg.show_all()
        dlg.set_keep_above(True)
        response = dlg.run()
        dir = dlg.get_filename()
        dlg.destroy()
        return dir

# funs to load both image and mask
    def load_image(self):

        one_image = PyApp.image_list[PyApp.cur_img_num]
        file_name = os.path.basename(one_image)

        PyApp.mask_path = os.path.join(PyApp.mask_dir,file_name)

        # on first run setup Image
        if PyApp.img == None:
            PyApp.img = gimp.Image(1000, 1000)

        # laod both images
        for f, name, pos in ((one_image, "Image", 1), (PyApp.mask_path, "Mask", 0)):
            PyApp.layer = pdb.gimp_file_load_layer(PyApp.img, f)
            pdb.gimp_layer_set_name(PyApp.layer, name)
            pdb.gimp_image_insert_layer(PyApp.img, PyApp.layer, None, pos)

        # set opacity of mask
        PyApp.image = gimp.image_list()[0]
        active_layer = pdb.gimp_image_get_active_layer(PyApp.image)
        pdb.gimp_layer_set_opacity(active_layer, 60)

        # resize canvas if image is not 1000x1000
        pdb.gimp_image_resize_to_layers(PyApp.image)
        # make display on first run
        if PyApp.first_build == True:
            PyApp.display_name = pdb.gimp_display_new(PyApp.img)
            PyApp.first_build = False
        # refresh image
        pdb.gimp_displays_flush()

# this func sets file list and file count
    def get_img_list(self):
        # pdb.gimp_message('start')
        PyApp.image_list = glob.glob(PyApp.image_dir+'/*')
        # pdb.gimp_message('got list')
        PyApp.image_count = len(PyApp.image_list)
        # pdb.gimp_message('image count '+str(PyApp.image_count))

# this func will save the mask file, then remove all the layers,
# we force index mode to
    def save_mask_then_remove_all(self):
        if PyApp.img != None:
            # pdb.gimp_message(PyApp.image.layers)
            # remove background image from image
            pdb.gimp_image_remove_layer(PyApp.img,PyApp.image.layers[1])
            # foceing into indexed colour mode to limit colours
            pdb.gimp_image_convert_indexed(PyApp.img, NO_DITHER, 4, 20, FALSE, FALSE, PyApp.actual_name)
            # convert back into RGB to save it out
            pdb.gimp_image_convert_rgb(PyApp.image)
            # save mask
            pdb.gimp_file_save(PyApp.img, PyApp.layer, PyApp.mask_path, '?')
            # pdb.gimp_message('saved')
            # remove mask from image
            pdb.gimp_image_remove_layer(PyApp.img,PyApp.image.layers[0])
            # pdb.gimp_message('removed')

    def load_next_image(self,button):
        # the next button has been clicked so inciment cur_img_num by one
        self.save_mask_then_remove_all()
        if PyApp.cur_img_num < PyApp.image_count-1:
            PyApp.cur_img_num+=1
            # pdb.gimp_message('next image')
            self.load_image()
            self.progress_timeout()
        else:
            # wrap arround to start
            PyApp.cur_img_num = 0
            self.load_image()
            self.progress_timeout()

    def load_prev_image(self,button):
        self.save_mask_then_remove_all()
        if PyApp.cur_img_num > 0:
            PyApp.cur_img_num-=1
            # pdb.gimp_message('prev image')
            self.load_image()
            self.progress_timeout()
        else:
            # wrap arround to the end
            PyApp.cur_img_num = PyApp.image_count-1
            self.load_image()
            self.progress_timeout()
            # pdb.gimp_message('no more images')
    def finsh(self,button):
        self.save_mask_then_remove_all()
        pdb.gimp_palette_delete(PyApp.actual_name)
        pdb.gimp_displays_flush()
        pdb.gimp_display_delete(PyApp.display_name)
        self.destroy()

def ESM():
    PyApp()
    gtk.main()

# GIMP rego info
register(
         "ESM",
         "Open images and mask files for rapid edits",
         "Open images and mask files for rapid edits",
         "Nick Wright", "Nick Wright",
         "2021",
         "<Toolbox>/Tools/Edit Segmentation Masks",
         "",
         [],
         [],
         ESM)
main()
