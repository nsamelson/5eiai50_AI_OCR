import os
import shutil
import preprocessing.textbounding.textBounding as tb

def prepareCharacters(imagePath):
    # delete output folder
    try:
        shutil.rmtree('./preprocessing/textbounding/outputchars')
    except Exception as e:
        do = "nothing"

    # create empty output folder
    uncreated = 1
    while (uncreated):
        try:
            os.mkdir('./preprocessing/textbounding/outputchars')
            uncreated = 0
        except Exception as e:
            do = "nothing"
    
    tb.cropWords(imagePath)

    for word in os.listdir('./preprocessing/textbounding/outputwords'):
        if word != 'Text Detection.jpg':
            tb.cropCharacters('./preprocessing/textbounding/outputwords/'+word)

    return

