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
# special_tags are tags which I use as placeholer, they will not removed if I accidentaly copy them to output filed
special_tags = ['MAIN', 'MOAT', 'CONVNEXT', 'PREVIOUS', 'DONE', 'PROBABLY']

# Define next variables for yourself, based on your needs

# repl_dic  tags which will be replaced/removed
repl_dic = {'_': ' ', '\n': ',', 'multicolored hair': 'two-tone hair', 'realistic': '', 'photorealistic': ''}
# pair_tags tags which expect other tag to be included
pair_tags = {' grin,': 'teeth, ', ' watch,': 'wristwatch, ', 'wristwatch,': ' watch, ', }
# unwantd_list which will be removed from suggestions
unwantd_list = 'uncensored,censored,collarbone,traditional media,mixed media,' 
# Tags whihc should be always included
recomended_tags = ['1girl, ', 'solo, ', 'looking at viewer, ', ]
# Has to be defined because of debug bug
pth_pickl = '/PATH/TO/PYTHON/FILE/'  

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
    probable_tags = ''
    for i in range(len(last_pic_tags)-1,-1,-1):
        probable_tags += last_pic_tags[i] + ', '
    just_used_tags = probable_tags
    probable_tags = probable_tags.split(',')
    probable_tags = [x.strip() for x in probable_tags if x.strip()]
    probable_tags = [x for x in probable_tags if x in tags or x in tags_m or x in tags_c]
    probable_tags = ', '.join(probable_tags)
    tags = ',PROBABLY,' + probable_tags + ',DONE,' + tags_d + ',MAIN,' + tags + ',MOAT,' + tags_m + ',CONVNEXT,' + tags_c + ',PREVIOUS,' + last_pic_tags + ', ' + pre_last_pic_tags
    current_img_tags = tags
    
    # Replaces tags with other tags
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
    for tg in recomended_tags:
        if tg not in tags:
            tag_suggest += tg
    # Suggest tag if there is another tag from pair present
    for words in pair_tags:
        if words in tags and pair_tags[words] not in tags:
            tag_suggest += pair_tags[words]

    generated_tags.delete(0.0, END)
    generated_tags.insert(END, tags)
    suggestions_note.delete(0.0, END)
    suggestions_note.insert(END, tag_suggest)

def reorder_tags(s):
    s = s.split(',')
    s = [x.strip() for x in s if x.strip()]
    new_roder = []
    for tag in tag_order_list:
        if tag in s:
            new_roder.append(tag)
        elif re.match(r'([A-Z]+_?)+', tag):
            new_roder.append('\n')
    new_roder.append('\n')
    for tag in s:
        if tag not in new_roder:
            new_roder.append(tag)
    new_roder = ', '.join(new_roder) 
    new_roder = new_roder.replace('\n, ', '\n').replace('\n\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')
    return new_roder.strip() + ' \n'

def save_tags():
    global image_index
    global last_pic_tags
    img_path = images_list[image_index]
    img_path = img_path.split('.')
    new_tags = curent_tag_list.get(0.0, END).strip()
