# Importing Image class from PIL module
import os
from PIL import Image






directory = "backend/training/printed/"

for image in os.listdir(f"backend/training/printed/"):
    f = os.path.join(directory, image)

    # Opens a image in RGB mode
    im = Image.open(f)

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    # Setting the points for cropped image
    left = 160
    top = 28
    right = 440
    bottom = 308

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    im2 = im1.resize((28,28))

    im2.save(f)