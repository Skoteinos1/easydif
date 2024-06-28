import os
from tkinter import *
# from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import shutil
import pickle

img_x_size = 1270
img_y_size = 920

def save_pickle(file, data1):
    if '.pkl' not in file:
        file += '.pkl'
    pkl_file = open(pth_pickl + file, 'wb')
    pickle.dump(data1, pkl_file)
    pkl_file.close()

def load_pickle(fl_nm):
    if '.pkl' not in fl_nm:
        fl_nm += '.pkl'
    try:
        pkl_file = open(pth_pickl + fl_nm, 'rb')
        data1 = pickle.load(pkl_file)
        pkl_file.close()
    except:
        print('Missing pickle table:', fl_nm)
        # pkl_file = open(file, 'wb')
        data1 = ''
    return data1


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
    probable_tags = last_pic_tags + ', ' + pre_last_pic_tags
    probable_tags = probable_tags.split(',')
    probable_tags = [x.strip() for x in probable_tags if x.strip()]
    probable_tags = [x for x in probable_tags if x in tags or x in tags_m or x in tags_c]
    probable_tags = ', '.join(probable_tags)
    tags = ',PROBABLY,' + probable_tags + ',DONE,' + tags_d + ',MAIN,' + tags + ',MOAT,' + tags_m + ',CONVNEXT,' + tags_c + ',PREVIOUS,' + last_pic_tags + ', ' + pre_last_pic_tags
    current_img_tags = tags
    repl_dic = {'_': ' ', '\n': ',', 'multicolored hair': 'two-tone hair', 'tatoo on foot': 'tattoo on foot', 'tatoo on belly': 'tattoo on stomach', 'large breasts': '', 'medium breasts': '', 'realistic': '', 'photorealistic': ''}    
    for words in repl_dic:
        tags = tags.replace(words, repl_dic[words])

    tg_lst = tags.split(',')
    tg_lst = [x.strip() for x in tg_lst if x.strip()]
    tg_lst = list(dict.fromkeys(tg_lst))
    tags = ', '.join(tg_lst) # list to string

    for word in special_tags:
        tags = tags.replace(word, '\n'+word)  

    tags += ', '
    tag_suggest = ''
    for tg in [ 'solo, ', 'brown eyes, ', 'two-tone hair, ', 'looking at viewer, ', 'watermark, ']:
        if tg not in tags:
            tag_suggest += tg
