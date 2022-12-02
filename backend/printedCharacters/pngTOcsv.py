import os
from PIL import Image
import numpy as np



labels = ['0','1','2','3','4','5','6','7','8','9',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



directory = "backend/training/printed/"
csv = []

# Create headers of the CSV
headers = []
for i in range(785):
    if(i ==0):
        headers.append("label")
    else:
        headers.append(f"pixel{i}")
csv.append(headers)

# add each image as a row
for image in os.listdir(f"backend/training/printed/"):
    f = os.path.join(directory, image)

    # 1. Read image
    img = Image.open(f)

    # 2. Convert image to NumPy array
    arr = np.asarray(img)

    # 3. find the label of the character
    name = image.split("_")
    label = labels.index(name[1])

    lst = []
    lst.append(str(label))
    for row in arr:
        for col in row:
            Grayscale = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
            lst.append(str(Grayscale))
 
    csv.append(lst)


# 4. Save list of lists to CSV
with open('backend/training/digitsAndChars.csv', 'w') as f:
    for row in csv:
        f.write(','.join(row) + '\n')