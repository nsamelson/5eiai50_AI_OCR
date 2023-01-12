# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import shutil
import os

def cropWords(imagePath, minConfidence=0.5, width=1280, height=1280):

    # load the input image and grab the image dimensions
    image = cv2.imread(imagePath)
    orig = image.copy()
    (H, W) = image.shape[:2]

    # set the new width and height and then determine the ratio in change for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that we are interested -- the first is the output probabilities and the 
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet("./preprocessing/textbounding/frozen_east_text_detection.pb")

    # construct a blob from the image and then perform a forward pass of the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    # show timing information on text prediction
    print("[INFO] text detection took {:.6f} seconds".format(end - start))

    # grab the number of rows and columns from the scores volume, then initialize our set of bounding box rectangles and corresponding confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for i in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical data used to derive potential bounding box coordinates that surround text
        scoresData = scores[0, 0, i]
        xData0 = geometry[0, 0, i]
        xData1 = geometry[0, 1, i]
        xData2 = geometry[0, 2, i]
        xData3 = geometry[0, 3, i]
        anglesData = geometry[0, 4, i]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < minConfidence:
                continue

            # compute the offset factor as our resulting feature maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, i * 4.0)

            # extract the rotation angle for the prediction and then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    count = 1
    # change box width and height -> positive will add pixels and vice-versa
    box_width_padding = 3
    box_height_padding = 3

    temp_image = orig.copy()

    # delete output folder
    try:
        shutil.rmtree('preprocessing/textbounding/outputwords')
    except Exception as e:
        do = "nothing"

    # create empty output folder
    uncreated = 1
    while (uncreated):
        try:
            os.mkdir('preprocessing/textbounding/outputwords')
            uncreated = 0
        except Exception as e:
            do = "nothing"

    # define crop object
    class Crop(object):
        def __init__(self, startX, startY, endX, endY):
            self.startX = startX
            self.startY = startY
            self.endX = endX
            self.endY = endY

        def __eq__(self, other):
            diff = abs(self.startY - other.startY)
            if (diff <= 10):
                return self.startX == other.startX
            else:
                False

        def __lt__(self, other):
            diff = abs(self.startY - other.startY)
            if (diff <= 10):
                return self.startX < other.startX
            else:
                return self.startY < other.startY

    croppedList = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW) - box_width_padding
        startY = int(startY * rH) - box_height_padding
        endX = int(endX * rW) + box_width_padding
        endY = int(endY * rH) + box_height_padding

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # append to croppedList to sort the images
        croppedList.append(Crop(startX, startY, endX, endY))

    croppedList = sorted(croppedList)

    for img in croppedList:
        roi = temp_image[img.startY:img.endY, img.startX:img.endX]
        cv2.imwrite("preprocessing/textbounding/outputwords/" + str(count) + ".jpg", roi)
        count = count + 1

    # show the output image
    cv2.imwrite("preprocessing/textbounding/outputwords/Text Detection.jpg", orig)
    cv2.waitKey(0)
    
    return

def cropCharacters(imagePath):    
    # Create output directory
    file_name, file_ext = os.path.splitext(os.path.basename(imagePath))
    os.mkdir('preprocessing/textbounding/outputchars/'+file_name)
    
    # Load the image
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to create a binary image
    _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # Use morphological operations to separate the characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    
    i=0
    for contour in contours:
        i+=1
        x, y, w, h = cv2.boundingRect(contour)
        # Crop out the character using the bounding box coordinates
        character_img = img[y:y+h, x:x+w]
        
        # Add white padding around letter as it is cropped with no margin
        character_img = cv2.copyMakeBorder(character_img, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        character_img = cv2.resize(character_img, dsize=(28, 28), interpolation=cv2.INTER_AREA)

        cv2.imwrite('preprocessing/textbounding/outputchars/'+file_name+'/'+str(i)+file_ext, character_img)
        
    return
