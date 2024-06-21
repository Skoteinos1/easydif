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
    file1 = open(img_path[0] + '.txt', "r")
    tags = file1.read()  # reads until EOF
    file1.close()
    try:
        file1 = open(img_path[0].replace(img_group_path, pth+'moat/') + '.txt', "r")
        tags_m = file1.read()  # reads until EOF
        file1.close()
    except:
        tags_m = ''
    try:
        file1 = open(img_path[0].replace(img_group_path, pth+'convnext/') + '.txt', "r")
        tags_c = file1.read()  # reads until EOF
        file1.close()
    except:
        tags_c = ''
    try:
        file1 = open(img_path[0].replace(img_group_path, pth2) + '.txt', "r")
        tags_d = file1.read()  # reads until EOF
        file1.close()
    except:
        tags_d = ''
