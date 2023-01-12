import fitz

def transformIntoPng(pdfsource):
    # Open the pdf document
    doc = fitz.open("temp/"+pdfsource)

    # Select the first page
    page = doc[0]

    # Create a png image of the page
    pix = page.get_pixmap()
    newName = pdfsource.split('.')[0]
    pix.save("temp/{}.png".format(newName))

    return newName

