from gimpfu import *
import glob
import os
import gtk




class PyApp(gtk.Window):


    def __init__(self):
        super(PyApp, self).__init__()
        self.set_title("Buttons")
        self.set_size_request(250, 200)
        self.set_position(gtk.WIN_POS_CENTER)

        image_btn = gtk.FileChooserButton('open image folder')
        mask_btn = gtk.FileChooserButton('open mask folder')
        pdb.gimp_message('got_path')
        image_dir = image_btn.connect("file-set", self.get_path)
        mask_dir = mask_btn.connect("file-set", self.get_path)

        btn_next = gtk.Button("Next")
        btn_prev = gtk.Button("Previous")

        btn_next.connect("clicked", self.load_next_image)
        btn_prev.connect("clicked", self.load_prev_image)
        # btn_close = gtk.Button("Close")
        btn_next.set_size_request(80, 40)
        btn_prev.set_size_request(80, 40)
        # btn_close.set_size_request(20, 20)
        fixed = gtk.Fixed()
        fixed.put(btn_next, 20, 20)
        fixed.put(btn_prev, 130, 20)
        fixed.put(image_btn,20,80)
        fixed.put(mask_btn,20,120)
        # fixed.put(btn_close, 20, 80)
        self.connect("destroy", gtk.main_quit)
        self.add(fixed)
        self.show_all()




    def load_image(image_path, mask_path, image_number = 0 ):

        image_list = glob.glob(image_path+'/*')

        one_image = image_list[image_number]

        file_name = os.path.basename(one_image)
        mask_path = os.path.join(mask_dir,file_name)


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

        # this will save a layer
        # pdb.gimp_file_save(img, layer, '/Users/nicholaswright/Documents/gimp_segmentation_plugin/sample data/colour mask resave/tq84_write_text.png', '?')


    def get_path(self,button):
        path = os.path.dirname(button.get_filename())
        pdb.gimp_message(path)
        return path

    def load_next_image(self,button):
        pdb.gimp_message('next')
        load_image(image_dir,mask_dir)
        get_image_list(image_dir)

    def load_prev_image(self,button):
        pdb.gimp_message('prev')



def flip_images():

    PyApp()
    gtk.main()





register(
         "flip_images",
         "flip through a folder of images",
         "flip through a folder of images",
         "Nick Wright", "Nick Wright",
         "2021",
         "<Toolbox>/File/Flip through images",
         "",
         [
           # (PF_DIRNAME, "image_dir", "Image folder:", None),
           # (PF_DIRNAME, "colour_mask_dir", "Colour mask folder:", None),

         ],
         [],
         flip_images)

main()
