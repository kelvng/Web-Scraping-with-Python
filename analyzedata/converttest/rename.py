from PIL import Image
import os
# open image in png format
path = r'C:\Users\Administrator\Desktop\Image'
for root, dirs, files in os.walk(path):
    #print(root)
    if 'images' in root or 'Source' in root:
        #print(root)
        dir_list = os.listdir(root)
        #print(dir_list)
        #print('---------------')
        print(len(dir_list))
        for value in dir_list:
            imagepath = root + '\\' +value
            print(imagepath)
            img_png = Image.open(imagepath)
            if img_png.mode in ("RGBA", "P"):
                img_png = img_png.convert("RGB")
            # The image object is used to save the image in jpg format
            img_png.save(imagepath.replace('.png','.jpg'))

# path = r'P:\DataCrawler\Thuvienhoclieu.com'
# for root, dirs, files in os.walk(path):
#     #print(root)
#     dir_list = os.listdir(root)
#     for value in dir_list:
#         imagepath = root + '\\' + value
#         print(imagepath)
#         os.rename(imagepath, imagepath.replace('wwww.',''))