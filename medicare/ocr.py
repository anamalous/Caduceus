import cv2
import pytesseract
import pandas as pd
# Load image
def readstrip(imgurl):
    img = cv2.imread("./medicare/media/"+str(imgurl))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold_img)
    print(text)
    
    df=pd.read_csv("./medicare/drugs.csv")
    drug=df[df["Drug"]==text.split()[0]]

    return drug.to_dict()
