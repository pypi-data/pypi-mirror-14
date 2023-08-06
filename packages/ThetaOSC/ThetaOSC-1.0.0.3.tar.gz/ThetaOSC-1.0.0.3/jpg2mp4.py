#!python
#-*- coding:utf-8 -*

import cv2
import os
import glob

def main(rootdir="./Images/",fname="./animation.mp4v"):
    writer = cv2.VideoWriter ()
    if not writer.open(fname,
                       cv2.VideoWriter_fourcc(*"mp4v"),
                       1,#fps
                       (896,448), #frame_size, original image size w:5376xh2688 
                       isColor=True):
        print ("failed to open writer")
        sys.exit()

    files=glob.iglob(os.path.join(rootdir,"*[!-thmb].JPG")
    for imgfile in files:
        img=cv2.imread(imgfile)
        h,w,d=img.shape
        simg=cv2.resize(img,(896,448))
        cv2.imshow("image",simg)
        cv2.waitKey(10)
        writer.write(simg)
        
    writer.release()

    # "Free MP4 Converter" does not recognize ".mp4v" extension.
    newfname=os.path.join(os.path.abspath("."),"converted.mp4")
    os.rename(fname,newfname)n

if __name__ == "__main__":
    import argparse
    main()
