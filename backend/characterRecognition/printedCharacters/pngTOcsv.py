import os
from PIL import Image
import numpy as np



labels = ['0','1','2','3','4','5','6','7','8','9',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



directory = "backend/training/printed/"
csv = []
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Create headers of the CSV
headers = []
for i in range(785):
    if(i ==0):
        headers.append("label")
    else:
        headers.append(f"pixel{i}")
# csv.append(headers)

length = len(os.listdir(f"backend/training/printed/"))
# add each image as a row
for i,image in enumerate(os.listdir(f"backend/training/printed/")):
    f = os.path.join(directory, image)

    # 1. Read image
    img = Image.open(f)

    # 2. Convert image to NumPy array
    arr = np.asarray(img)

    # 3. find the label of the character
    name = image.split("_")[-1].split(".")[0]
    label = labels.index(name)


    lst = []
    lst.append(str(label))
    for row in arr:
        for col in row:
            # Grayscale = 255 - (0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2])
            inverted = 255 - col
            lst.append(str(int(inverted)))
 
    csv.append(lst)
    printProgressBar(i + 1, length, prefix = 'Progress:', suffix = 'Complete', length = 50)




# 4. Save list of lists to CSV
with open('backend/training/digitsAndChars.csv', 'w') as f:
    for row in csv:
        f.write(','.join(row) + '\n')