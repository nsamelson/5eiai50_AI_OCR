import os
import shutil
import preprocessing.textbounding.textBounding as tb

def prepareCharacters(imagePath):
    # delete output folder
    try:
        shutil.rmtree('./backend/preprocessing/textbounding/outputchars')
    except Exception as e:
        do = "nothing"

    # create empty output folder
    uncreated = 1
    while (uncreated):
        try:
            os.mkdir('./backend/preprocessing/textbounding/outputchars')
            uncreated = 0
        except Exception as e:
            do = "nothing"
    
    tb.cropWords(imagePath)

    for word in os.listdir('./backend/preprocessing/textbounding/outputwords'):
        tb.cropCharacters('./backend/preprocessing/textbounding/outputwords/'+word)

    return

# prepareCharacters('./backend/preprocessing/textbounding/images/Loremipsum1.png')