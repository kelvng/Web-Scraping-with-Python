import cv2
import numpy as np
import pytesseract
import os

imgname = "../../../learn_scrapy/img.png"
imagePath = os.getcwd()+'/captchas/'+ imgname

img = cv2.imread(imagePath,0)

croppedImg = img[11:67,42:178]

blurImg = cv2.medianBlur(croppedImg,3)

def removeLineNoise(inputImg):
    img = inputImg
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            flag = False
            if(img[i,j]!=50 and img[i,j]!=255):
                for k in range(img.shape[0]):
                    if(img[k,j]==50):
                        flag = True

                if(flag):
                    img[i,j]=50
                else:
                    img[i,j]=255
    return img

outputImg = removeLineNoise(blurImg)

blurOutput = cv2.medianBlur(outputImg,3)

textOutput = pytesseract.image_to_string(blurOutput)
print(textOutput)