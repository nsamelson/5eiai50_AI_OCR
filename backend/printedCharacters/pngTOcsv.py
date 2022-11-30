from PIL import Image
import numpy as np



# 1. Read image
img = Image.open("backend/training/printed/image_0_12456.png")
 
# 2. Convert image to NumPy array
arr = np.asarray(img)
print(arr.shape)
# (771, 771, 3)
# 3. Convert 3D array to 2D list of lists
lst = []
for row in arr:
    tmp = []
    for col in row:
        tmp.append(str(col))
    lst.append(tmp)

    
# 4. Save list of lists to CSV
with open('my_file.csv', 'w') as f:
    for row in lst:
        f.write(','.join(row) + '\n')