import random
from PIL import Image, ImageDraw, ImageFont
import string
import ntpath
import numpy as np
import os
import glob

fontSize = 22
imgSize = (28,28)
position = (0,0)

# https://tanmayshah2015.wordpress.com/2015/12/01/synthetic-font-dataset-generation/
#All images will be stored in 'Synthetic_dataset' directory under current directory
# dataset_path = os.path.join (os.getcwd(), 'Synthetic_dataset')
dataset_path = "backend/training/printed/"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

fhandle = open('backend\printedCharacters\Fonts_list.txt', 'r')
lower_case_list = list(string.ascii_lowercase)
upper_case_list = list(string.ascii_uppercase)
digits = range(0,10)

digits_list=[]
for d in digits:
    digits_list.append(str(d))

all_char_list = lower_case_list + upper_case_list + digits_list

fonts_list = []
for line in fhandle:
    fonts_list.append(line.rstrip('\n'))

total_fonts = len(fonts_list)
#paths = ttfquery.findsystem.findFonts()
all_fonts = glob.glob("C:\\Windows\\Fonts\\*.ttf")
f_flag = np.zeros(total_fonts)

for sys_font in all_fonts:
    #print "Checking "+p
    font_file = ntpath.basename(sys_font)
    font_file = font_file.rsplit('.')
    font_file = font_file[0]
    f_idx = 0
    for font in fonts_list:
        f_lower = font.lower()
        s_lower = sys_font.lower()
        #Check desired font
        if f_lower in s_lower:
            path = sys_font
            # r_size = random.randrange(-2,2) * 2 # gives a fontsize of 18,20,22 or 24
            # font = ImageFont.truetype(path, fontSize + r_size)
            f_flag[f_idx] = 1
            for ch in all_char_list:
                for a in range(10):
                    r_size = random.randrange(-2,2) * 2 # gives a fontsize of 18,20,22 or 24
                    font = ImageFont.truetype(path, fontSize + r_size)
                    image = Image.new("L", imgSize,255)
                    draw = ImageDraw.Draw(image)
                    pos_x = random.randrange(3,8)
                    pos_y = random.randrange(0,3)
                    shift_x = random.randrange(-1,5)
                    shift_y = random.randrange(-2,4)
                    # pos_x = 0
                    # pos_y = 0
                    pos_idx=0
                    for y in range(pos_y,pos_y+2):
                        for x in range(pos_x,pos_x+2):
                            position = (x+shift_x,y+shift_y)
                            draw.text(position, ch, 0, font=font)
                            ##without this flag, it creates 'Calibri_a.jpg' even for 'Calibri_A.jpg'
                            ##which overwrites lowercase images
                            l_u_d_flag = "u"
                            if ch.islower():
                                l_u_d_flag = "l"
                            elif ch.isdigit():
                                l_u_d_flag = "d"
                            file_name = font_file + '_' + l_u_d_flag + '_' + str(a) + '_'+ str(pos_idx) + '_' + ch + '.png'
                            file_name = os.path.join(dataset_path,file_name)
                            image.save(file_name)
                            pos_idx = pos_idx + 1     
    f_idx = f_idx + 1

