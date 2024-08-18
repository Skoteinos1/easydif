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
    # adds all tags together into one file
    f = open((img_path[0] + '.txt').replace(img_group_path, pth2+'all_tags/'), "w")
    f.write(current_img_tags)
    f.close()
    for word in special_tags:
        new_tags = new_tags.replace(word, '')
    new_tags = new_tags.replace('\n', ',')
    tg_lst = new_tags.split(',')
    tg_lst = [x.strip() for x in tg_lst if x.strip()]
    tg_lst = list(dict.fromkeys(tg_lst))
    new_tags = ', '.join(tg_lst) # list to string

    if new_tags:
        f = open((img_path[0] + '.txt').replace(img_group_path, pth2), "w")
        f.write(new_tags)
        f.close()
        # print(new_tags)
        shutil.copyfile(images_list[image_index], images_list[image_index].replace(img_group_path, pth2))
        last_pic_tags.append(new_tags)
        next_img()
    while len(last_pic_tags) > number_of_sets_as_suggestions:
        last_pic_tags.pop(0)


def show_image(x):
    for widget in img_frame.winfo_children():
        widget.destroy()
    img = Image.open(x)

    base_width = img_x_size
    base_height = img_y_size
    wpercent = (base_width / float(img.size[0]))
    hpercent = (base_height / float(img.size[1]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    wsize = int((float(img.size[0]) * float(hpercent)))
    if hsize <= img_y_size:
        img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    else:
        img = img.resize((wsize, base_height), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel = Label(img_frame, image=img, height=img_y_size, width=img_x_size)
    panel.image = img
    panel.pack()
    file_note.delete(0.0, END)
    file_note.insert(END, x.replace(pth, ''))
    get_current_tags(x)


def next_img(which_folder=''):
    global image_index
    if which_folder:
        shutil.copyfile(images_list[image_index], images_list[image_index].replace(img_group_path, pth2+which_folder))
    if image_index +1 in images_list:
        image_index +=1
    show_image(images_list[image_index])
    # print(image_index, len(images_list)-image_index)
    lbl_notif.config(text = str(image_index) +  ' ' + str(len(images_list)-image_index))


def prev_img():
    global image_index
    image_index -=1 if image_index > 0 else 0
    show_image(images_list[image_index])
    lbl_notif.config(text = str(image_index) +  ' ' + str(len(images_list)-image_index))


def moat_mess():
    # If Moat tagger did lousy job, this will mark tags for second tagging
    next_img('moat/')


def conv_mess():
    # If Convnext tagger did lousy job, this will mark tags for second tagging
    next_img('conv/')


def cln_tags():
    # Cleans suggested tags list
    new_tags = curent_tag_list.get(0.0, END).strip()
    old_tags = generated_tags.get(0.0, END).strip()
    new_tags = new_tags.split(',')
    old_tags = old_tags.split(',')
    new_tags = [x.strip() for x in new_tags if x.strip()]

    old_tags = [x.strip() for x in old_tags if x.strip() and x.strip() not in new_tags]
    old_tags = list(dict.fromkeys(old_tags))

    # marks checkbuttons
    global checkbutton_tags
    for key in checkbutton_tags:
        if key in new_tags:
            checkbutton_tags[key][0].set(True)
        else:
            checkbutton_tags[key][0].set(False)

    # Check for over tagging
    word_counter = ' '.join(new_tags)
    word_counter = word_counter.split(' ')
    word_counter = [x for x in word_counter if word_counter.count(x) > 1]
    word_counter = list(dict.fromkeys(word_counter))

    tag_suggest = ''
    for tg in recomended_tags:
        if tg not in new_tags:
            tag_suggest += tg + ', '
    for words in pair_tags:
        if words in new_tags and pair_tags[words] not in new_tags:
            tag_suggest += pair_tags[words]+ ', '
    suggestions_note.delete(0.0, END)
    suggestions_note.insert(END, tag_suggest)
    for tg in word_counter:
        suggestions_note.insert(END, tg + ', ', 'alert')
    suggestions_note.insert(END, len(new_tags), 'alert')

    # Removes unwanteg tags
    unwanted_list = unwantd_list.split(',')
    old_tags = [ele for ele in old_tags if ele not in unwanted_list]
   
    # Removes tag from generated_tags if other is present in curent_tag_list 
    for key in remove_if:
        if isinstance(remove_if[key], str):
            if key in new_tags and remove_if[key] in old_tags:
                old_tags.remove(remove_if[key])
        elif isinstance(remove_if[key], list):
            for t in remove_if[key]:
                if key in new_tags and t in old_tags:
                    old_tags.remove(t)
    
    old_tags = ', '.join(old_tags) # list to string
    for word in special_tags:
        old_tags = old_tags.replace(word, '\n'+word)
    generated_tags.delete(0.0, END)
    generated_tags.insert(END, old_tags.strip()+', ')


def on_closing():
    global current_img_tags
    global last_pic_tags
    save_pickle('image_tagger_tags', {'current_img_tags': current_img_tags, 'last_pic_tags': last_pic_tags})
    root.destroy()


def apply_checked_tags():
    # Manipulate tag list with checkbuttons
    new_tags = curent_tag_list.get(0.0, END).strip()
    new_tags = new_tags.replace('\n', ',')
    new_tags = new_tags.split(',')
    new_tags = [x.strip() for x in new_tags if x.strip()]
    new_tags = list(dict.fromkeys(new_tags))

    for key in checkbutton_tags:
        # if checkbutton_tags[key][0].get() and :
        #     print(key)
        if not checkbutton_tags[key][0].get() and key in new_tags:
            new_tags.remove(key)
        elif checkbutton_tags[key][0].get() and key not in new_tags:
            new_tags.append(key)
