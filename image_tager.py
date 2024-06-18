import os
from tkinter import *
# from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import shutil

img_x_size = 1270
img_y_size = 920

def get_current_tags(img_path=''):
    global current_img_tags

    img_path = img_path.split('.')
    if len(img_path) != 2:
        print(' !!! TOO MANY DOTS IN FILENAME !!! ', img_path )
        lbl_notif.config(text = '!!! TOO MANY DOTS IN FILENAME !!!')
        return
