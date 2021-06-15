# helpfull links
# https://stackoverflow.com/questions/58343148/gimp-python-plugin-to-load-2-images-as-layers

from gimpfu import *
import glob
import os
import gtk,gobject
#




class PyApp(gtk.Window):
    # set a bunch of globals, this is a bit lazy but it works
    cur_img_num = 0 # the currnet displayed image
    image_count = 0 # the amount of images in images folder
    image_list = [] # the list of images from the images folder
    mask_path = '' # path to current mask file
    image_dir = None # directory of images
    mask_dir = None # directory of mask folder
    img = None
    layer = None
    image = None
    first_build = True # used to know if we need to set up a canvas
    first_img_load = True # used to not try to save on first click

    def __init__(self):
        super(PyApp, self).__init__()
        # build gtk interface
        self.set_title("Image flipper")
        self.set_size_request(240, 110)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_keep_above(True)
        # build buttons
        btn_next = gtk.Button("Next")
        btn_prev = gtk.Button("Previous")

        btn_next.connect("clicked", self.load_next_image)
        btn_prev.connect("clicked", self.load_prev_image)

        btn_next.set_sensitive(False)
        btn_prev.set_sensitive(False)


        btn_next.set_size_request(80, 40)
        btn_prev.set_size_request(80, 40)

        fixed = gtk.Fixed()
        # building progress bar
        self.pb = gtk.ProgressBar()
        self.pb.set_size_request(220, 30)
        self.pb.set_text("Progress")
        self.pb.set_fraction(0.0)

    	fixed.put(self.pb,10,70)



        # self.timer = gobject.timeout_add (100, progress_timeout, self)

        fixed.put(btn_next, 150, 20)
        fixed.put(btn_prev, 10, 20)

        self.connect("destroy", gtk.main_quit)
        self.add(fixed)
        self.show_all()

        # force two popups on start to select images and mask folder
        PyApp.image_dir = self.open_file(open_title='Select image folder')
        # get image list from selected folder
        self.get_img_list()
        PyApp.mask_dir = self.open_file(open_title='Select coloured mask folder')

        btn_next.set_sensitive(True)
        btn_prev.set_sensitive(True)

        self.load_image()
        self.progress_timeout()


    def progress_timeout(self):
        pdb.gimp_message('checked')
        new_val = float(PyApp.cur_img_num+1)/float(PyApp.image_count)
        self.pb.set_fraction(new_val)
        self.pb.set_text(str(PyApp.cur_img_num+1)+' out of ' + str(PyApp.image_count))
        return True

# func to open folder selection dialog box
    def open_file(self,open_title):
        dlg = gtk.FileChooserDialog(open_title,
        None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = dlg.run()
        dir = dlg.get_filename()
        dlg.destroy()
        return dir

# funs to load both image and mask
    def load_image(self):

        one_image = PyApp.image_list[PyApp.cur_img_num]
        file_name = os.path.basename(one_image)

        # pdb.gimp_message(PyApp.mask_dir)

        PyApp.mask_path = os.path.join(PyApp.mask_dir,file_name)
        # pdb.gimp_message(PyApp.mask_path)

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
            pdb.gimp_display_new(PyApp.img)
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
            pdb.gimp_image_convert_indexed(PyApp.img, NO_DITHER, 4, 20, FALSE, FALSE, "Image Segmentation Palette.txt")
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
        # pdb.gimp_message('next clicked')
        # save mask
        self.save_mask_then_remove_all()

        if PyApp.cur_img_num < PyApp.image_count-1:
            # self.remove_image()
            PyApp.cur_img_num+=1
            # pdb.gimp_message('next image')
            self.load_image()
            self.progress_timeout()
        else:
            # PyApp.cur_img_num = PyApp.image_count+1
            self.load_image()
            pdb.gimp_message('no more images')
        # pdb.gimp_message(PyApp.cur_img_num)


    def load_prev_image(self,button):
        # pdb.gimp_message('prev clicked')
        self.save_mask_then_remove_all()
        if PyApp.cur_img_num > 0:
            PyApp.cur_img_num-=1
            # pdb.gimp_message('prev image')
            self.load_image()
            self.progress_timeout()
        else:
            PyApp.cur_img_num = 0
            self.load_image()
            pdb.gimp_message('no more images')
        # pdb.gimp_message(PyApp.cur_img_num)

def flip_images():

    PyApp()
    gtk.main()

# gimp rego info
register(
         "flip_images",
         "flip through a folder of images",
         "flip through a folder of images",
         "Nick Wright", "Nick Wright",
         "2021",
         "<Toolbox>/File/Flip through images",
         "",
         [],
         [],
         flip_images)
main()
