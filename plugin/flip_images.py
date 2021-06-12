# helpfull links
# https://stackoverflow.com/questions/58343148/gimp-python-plugin-to-load-2-images-as-layers


from gimpfu import *
import glob
import os
import gtk
# import Gtk




class PyApp(gtk.Window):
    cur_img_num = 0
    image_count = 0
    image_list = []
    image_count = 0
    image_dir = ''
    mask_dir = ''
    mask_path = ''
    img = None
    layer = None


    def __init__(self):
        super(PyApp, self).__init__()
        self.set_title("Buttons")
        self.set_size_request(250, 200)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_keep_above(True)

        # image_btn = gtk.FileChooserButton('open image folder')

        image_btn = gtk.FileChooserButton(title="open image file") # should be able to use Gtk.FileChooserAction.SELECT_FOLDER to open folder instead
        mask_btn = gtk.FileChooserButton(title='open mask file')

        image_btn.connect("file-set", self.get_image_path_n_list)
        mask_btn.connect("file-set", self.get_mask_dir)

        image_btn.set_size_request(180, 40)
        mask_btn.set_size_request(180, 40)

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





    def load_image(self):

        one_image = PyApp.image_list[PyApp.cur_img_num]

        pdb.gimp_message('one'+one_image)

        file_name = os.path.basename(one_image)

        pdb.gimp_message(PyApp.mask_dir)

        PyApp.mask_path = os.path.join(PyApp.mask_dir,file_name)
        pdb.gimp_message(PyApp.mask_path)


        PyApp.img = gimp.Image(1000, 1000)
        # pdb.gimp_display_new(img)

        for f, name, pos in ((one_image, "Image", 1), (PyApp.mask_path, "Mask", 0)):
            PyApp.layer = pdb.gimp_file_load_layer(PyApp.img, f)
            pdb.gimp_layer_set_name(PyApp.layer, name)
            pdb.gimp_image_insert_layer(PyApp.img, PyApp.layer, None, pos)
            # pdb.gimp_message(img.layers)



        image = gimp.image_list()[0]
        active_layer = pdb.gimp_image_get_active_layer(image)
        pdb.gimp_layer_set_opacity(active_layer, 60)

        width = active_layer.width
        height = active_layer.height



        pdb.gimp_image_resize_to_layers(image)
        pdb.gimp_display_new(PyApp.img)

            # delete image display and image


        # pdb.gimp_display_delete(img)
        # pdb.gimp_message('made it')
        # pdb.gimp_image_resize(width,height)
        # pdb.gimp_image_resize(width,height)

        # this will save a layer


    def get_mask_dir(self,button):
        path = os.path.dirname(button.get_filename())
        pdb.gimp_message(path)
        PyApp.mask_dir = path
        # return path

    def get_image_path_n_list(self,button):
        # this func turns file path into folder path
        # then calls calls get image list
        # convert selected image in to dir path
        image_path = os.path.dirname(button.get_filename())
        pdb.gimp_message(image_path)
        # pdb.gimp_message('got image path')
        self.get_img_list(image_path)
        PyApp.image_dir
        # return image_path

    def get_img_list(self,image_path):
        # this func sets file list and file count
        PyApp.image_list = glob.glob(image_path+'/*')
        pdb.gimp_message('got list')
        PyApp.image_count = len(PyApp.image_list)
        pdb.gimp_message('image count '+str(PyApp.image_count))


    def load_next_image(self,button):
        # the next button has been clicked so inciment cur_img_num by one
        pdb.gimp_message('next clicked')
        # save mask
        if PyApp.img != None:
            pdb.gimp_message(PyApp.layer)
            pdb.gimp_file_save(PyApp.img, PyApp.layer, PyApp.mask_path, '?')

        pdb.gimp_message(PyApp.cur_img_num)
        if PyApp.cur_img_num < PyApp.image_count-1:
            # self.remove_image()
            PyApp.cur_img_num+=1
            pdb.gimp_message('next image')
            self.load_image()
        else:
            pdb.gimp_message('no more images')
        pdb.gimp_message(PyApp.cur_img_num)




    def load_prev_image(self,button):
        pdb.gimp_message('prev clicked')
        if PyApp.cur_img_num != 0:
            PyApp.cur_img_num-=1
            pdb.gimp_message('prev image')
            self.load_image()
        else:
            pdb.gimp_message('no more images')
        pdb.gimp_message(PyApp.cur_img_num)

# crazy hack to remove images
    def remove_image():
        pdb.gimp_message('remove')
        # delete image display and image
        for displayID in range(1,image.ID+50):
            display=gimp._id2display(displayID)
            if isinstance(display,gimp.Display):
                #print 'Image: %d; display %d' % (image.ID,displayID)
                break
        if not display:
            pdb.gimp_message('nothing to remove')
        gimp.delete(display)





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
