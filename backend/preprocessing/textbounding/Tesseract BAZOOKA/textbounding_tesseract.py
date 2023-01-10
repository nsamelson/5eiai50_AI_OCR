import cv2 
import pytesseract
from pytesseract import Output
import numpy as np

img = cv2.imread("backend/preprocessing/textbounding/PRINTECAM_canon3320_v1self_ecam_be_0751_001_page-0001.jpg")

# Adding custom options
custom_config = r'--oem 3 --psm 6'
d = pytesseract.image_to_data(img, output_type=Output.DICT)

h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img) 
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.namedWindow('output', cv2.WINDOW_NORMAL)
cv2.resizeWindow('output', 800,800)
cv2.imshow('output', img)
cv2.waitKey(0)
print(d['text'])

