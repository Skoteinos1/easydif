import pickle
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS, IFD
from pillow_heif import register_heif_opener    # HEIF support
# import pillow_avif                              # AVIF support
from string import printable
import json
import pyperclip
import pyautogui
import time
from pynput.keyboard import Key, Controller


pth = '/PATH/TO/FILES/'  # Has to be defined because of debug bug
def save_pickle(file, data1):
    if '.pkl' not in file:
        file += '.pkl'
    pkl_file = open(pth + file, 'wb')
    pickle.dump(data1, pkl_file)
    pkl_file.close()

def load_pickle(fl_nm):
    if '.pkl' not in fl_nm:
        fl_nm += '.pkl'
    try:
        pkl_file = open(pth + fl_nm, 'rb')
        data1 = pickle.load(pkl_file)
        pkl_file.close()
    except:
        print('Missing pickle table:', fl_nm)
        # pkl_file = open(file, 'wb')
        data1 = ''
    return data1

def metadata_for_jpg(pth):
    image = Image.open(pth)
    exif = image.getexif()
    info_dict = {
    "Filename": image.filename,
    "Image Size": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1)
    }

    # register_heif_opener()   # HEIF support
 
    for k, v in exif.items():
        tag = TAGS.get(k, k)
        info_dict[tag] = v

    for ifd_id in IFD:
        try:
            ifd = exif.get_ifd(ifd_id)

            if ifd_id == IFD.GPSInfo:
                resolve = GPSTAGS
            else:
                resolve = TAGS

            for k, v in ifd.items():
                tag = resolve.get(k, k)
                if ifd_id.name == 'Exif':
                    json_string = v.decode('utf-8')
                    json_string = ''.join(char for char in json_string if char in printable)
                    json_string = json_string[len('UNICODE'):]
                    # json_string = json_string.replace('null', '0')
                    user_comment_data = json.loads(json_string)
                    # print(json.dumps(user_comment_data, indent=2))
                    for key in user_comment_data:
                        info_dict[key] = user_comment_data[key]
                        # print(key, user_comment_data[key])
                else:
                    print(tag, v)
        except KeyError:
            pass

    # for label,value in info_dict.items():
    #     print(f"{label:26}: {value}")

    return info_dict
    

option = 4

'''
Option 1: Takes bunch of prompts from foo and sorts them out. There is an option to generate bunch of prompts with different LoRA's in them
Option 2: If you coose to store data about jour pictures in .json files. This code will run through all folder and put all data into Dictionary
Option 3: Now when you have your Dictionary, you can pull data about all pictures you need
Option 4: After you generated bunch of pictures with different checkpoints and LoRA's run this code once. Now delete all pictures you don't like from folder. 
          Run this code again and it will tell you that you kept 30% of pictures from checkpint1, 70% of pictures from checkpoint2, 50% of pictures from LoRA1.
          Now you know that you should not use checkpoint1 ever again.
Option 5: It enters all combinations of prompts and LoRA's into textfield in quick succesion. Make sure you have right coordinates for mouse pointer
Option 6: It cleans up .json and .txt files which don't have picture with same name
Option 7: Goes through all pictures and collects all negative prompts which were used.

'''
if option == 1:
    # Prompt sorter
    foo = """
deformed, blurry, username, watermark, signature, poorly drawn face, mutated hands, poorly drawn hands, mutation, blurry 
deformed, blurry, username, watermark, signature, poorly drawn face, mutated hands, poorly drawn hands, mutation, blurry 
"""

    foo = foo.split('\n')
    foo2 = []
    for f in foo:
        if f.strip() not in foo2:
            foo2.append(f.strip())

    for i in range(1, 10):
        for f in foo2:
            # print(f + ', <lora:LoRA-0' + str(i) + ':0.8>'  '\n')
            pass

    for f in foo2:
        print(f, '\n')
        # print(f + ', <lora:LoRA2-10:0.8>'  '\n')

    foo3 = []
    for entry in foo2:
        entry = entry.split(', ')
        for pr in entry:
            if pr not in foo3:
                foo3.append(pr)
                print(pr, end=', ')
    print()
    

elif option == 2:
    # make File info DB
    dic = load_pickle('img_dic')
    if not dic:
        dic = {}
    counter = 0
    for path, subdirs, files in os.walk("/home/skoty/Stable Diffusion UI"):
        for fl in files:
            key = ''
            info = ''
            foo = path + '/' + fl
            if '.txt' in fl or '.xml' in fl or '.json' in fl:
                key = fl
                # key = fl.replace('.txt', '')
                # key = key.replace('.xml', '')
                # key = key.replace('.json', '')
                if key in dic:
                    continue
                counter += 1
                file1 = open(foo, "r")
                info = file1.read()
                file1.close()
            dic[key] = info
    save_pickle('img_dic', dic)
    print('Added: ', counter)
                
elif option == 3:
    # Get Prompt for image
    dic = load_pickle('img_dic')
    while True:
        name = input("Enter image name:  ")
        for key in dic:
            name = name.replace('.jpg', '')
            name = name.replace('.jpeg', '')
            name = name.replace('.png', '')
            if name in key:
                print(key, '\n', dic[key], '\n\n')

elif option == 4:
    # make File info DB
    fldr = []
    fldr.append("1704851761307")  # 0 
    fldr.append('1705889825765')  # 1
    # fldr.append('')  # 2

    i = -1
    dic = load_pickle(fldr[i])
    dic_exists = True
    if not dic:
        dic = {}
        dic_exists = False
    counter = 0
    new_dic = {}
    for path, subdirs, files in os.walk("/PATH/TO/Stable Diffusion UI/"+fldr[i]):
        for fl in files:
            key = ''
            info = ''
            foo = path + '/' + fl
            if fl.endswith(".jpeg") or fl.endswith(".jpg"):
                key = fl
                # key = fl.replace('.txt', '')
                # key = key.replace('.xml', '')
                # key = key.replace('.json', '')                
                mdt = metadata_for_jpg(foo)
                new_dic[key] = mdt
                if key in dic:
                    continue
                dic[key] = mdt
                counter += 1
    if not dic_exists:
        save_pickle(fldr[i], dic)
        print('Added: ', counter)

    dic_counter = {}
    for key in dic:
        lora = dic[key]['use_lora_model']
        model = dic[key]['use_stable_diffusion_model']
        if not lora in dic_counter:
            dic_counter[lora] = [0, 0]
        if not model in dic_counter:
            dic_counter[model] = [0, 0]
        dic_counter[lora][0] += 1
        dic_counter[model][0] += 1

    for key in new_dic:
        lora = new_dic[key]['use_lora_model']
        model = new_dic[key]['use_stable_diffusion_model']
        if not lora in dic_counter:
            dic_counter[lora] = [0, 0]
        if not model in dic_counter:
            dic_counter[model] = [0, 0]
        dic_counter[lora][1] += 1
        dic_counter[model][1] += 1

    trash_lst = []
    for key in dic_counter:
        # print(f"{key:35} {dic_counter[key]} {dic_counter[key][1]/dic_counter[key][0]}")
        # print(key, dic_counter[key], dic_counter[key][1]/dic_counter[key][0])
        try:
            trash_lst.append([key, dic_counter[key], dic_counter[key][1]/dic_counter[key][0]])
        except:
            print(key, dic_counter[key])
    
    trash_lst.sort(key = lambda x: x[2])
    for ln in trash_lst:
        print(ln)

elif option == 5:
    # Create prompt lora combinations
    prompts = '''Astronaut on Horse
Astronaut on Tree
'''
    loras = ['LoRA-10', 'LoRA21-04', 'LoRA21-05', 'LoRA21-07', 'LoRA1', 'MyLoRAV1']
    
    print(loras)
    # loras = 'a'
    prompts = prompts.split('\n')
    keyboard = Controller()
    for lora in loras:
        lora = '<lora:'+ lora +':0.5>'
        for prompt in prompts:
            if not prompt.strip():
                continue
            s = prompt.strip() + ' ' + lora
            # pyautogui.click(100, 300)
            pyautogui.moveTo(100, 300)
            pyautogui.leftClick()
            with keyboard.pressed(Key.ctrl):
                keyboard.press('a')
                keyboard.release('a')

            time.sleep(0.1)
            pyperclip.copy(s)
            with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
            time.sleep(0.2)

            # pyautogui.click(100, 100)
            # spam = pyperclip.paste()
            # pyperclip.paste()
            pyautogui.moveTo(100, 530)
            pyautogui.leftClick()
            time.sleep(0.1)
            print(s)
            # break
        # break

elif option == 6:
    # Clean up of json files.
    c = 0
    for path, subdirs, files in os.walk("/PATH/TO/Stable Diffusion UI"):
        for fl in files:
            key = ''
            if '.txt' in fl or '.xml' in fl or '.json' in fl:
                key = fl.replace('.txt', '')
                key = key.replace('.xml', '')
                key = key.replace('.json', '')
                foo = path + '/' + key
                if not os.path.isfile(foo + '.jpg') and not os.path.isfile(foo + '.jpeg') and not os.path.isfile(foo + '.png'):
                    if '.comments' not in foo:
                        print(foo)
                        os. remove(path + '/' + fl)
                        c+=1
                    else:
                        if not os.path.isfile(foo.replace('.comments/', '')):
                            os. remove(path + '/' + fl)
                            print(foo)
                            c+=1
    print('Deleted files:', c)
elif option == 7:
    # Negative prompt collector
    dic = load_pickle('img_dic')
    neg_lst = []
    for key in dic:
        if dic[key]:
            if isinstance(dic[key], str):
                try:
                    s = dic[key].split("Negative Prompt: ")[1]
                    s = s.split("Seed: ")[0]
                except:
                    s = dic[key]
                    if '&quot;' in s:
                        s = dic[key].split('&quot;')
                        for i in range(len(s)):
                            if s[i] == 'Negative Prompt' or s[i] == 'negative_prompt':
                                s = s[i+2]
                                break
                    elif '{' in s:
                        s = json.loads(s)
                        # print(s)
                        s = s['negative_prompt']
                    else:
                        # print(s)
                        pass
       
            try:
                s = s.strip()
            except:
                # print(dic[key])
                # foo = input('Press Enter')
                pass
            if s not in neg_lst:
                neg_lst.append(s)
    for ent in neg_lst:
        print(ent, '\n')


                


