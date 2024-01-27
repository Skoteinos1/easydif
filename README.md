# Assistant for AI image generaion.

![Easy Diffusion Screen](https://github.com/Skoteinos1/easydif/blob/main/easydif.jpg) 

To achieve some sort of similarity in generated images you need LoRA. You can easily train new LoRA's but which version produces best images? There is only one way to find out. You have to generate A LOT of images. But that was just a first step, now you have to find out which LoRA is most successful. My code will help you with that.

My code does 7 things. You can control them by setting: option = x<br>
Option 1: Takes bunch of prompts from foo and sorts them out. There is an option to generate bunch of prompts with different LoRA's in them.<br>
Option 2: If you coose to store data about jour pictures in .json files. This code will run through all folder and put all data into Dictionary.<br>
Option 3: Now when you have your Dictionary, you can pull data about all pictures you need.<br>
Option 4: After you generated bunch of pictures with different checkpoints and LoRA's run this code once. Now delete all pictures you don't like from folder. Run this code again and it will tell you that you kept 30% of pictures from checkpint1, 70% of pictures from checkpoint2, 50% of pictures from LoRA1. Now you know that you should not use checkpoint1 ever again.<br>
Option 5: It enters all combinations of prompts and LoRA's into textfield in quick succesion. Make sure you have right coordinates for mouse pointer.<br>
Option 6: It cleans up .json and .txt files which don't have picture with same name.<br>
Option 7: Goes through all pictures and collects all negative prompts which were used.


Don't forget to set your folders.


