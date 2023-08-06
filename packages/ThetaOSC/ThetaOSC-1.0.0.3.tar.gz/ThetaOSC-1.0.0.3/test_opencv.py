#!/usr/bin/python
#-*- coding:utf-8 -*-
# import pyximport
from __future__ import print_function

import cv2
import numpy
import time

import os,os.path
import sys
sys.path.insert(0,"./build/lib.macosx-10.6-intel-2.7")

from generate_DF_to_ER_map import generate_DFtoER_map

#
cam=cv2.VideoCapture("../Images/R0010080.MP4")
for i in range(405):
    ret,img=cam.read()

h,w,d=img.shape
print (h, w)
simg=cv2.resize(img,(w/2,h/2))
cv2.imshow("shrinked",simg)
cv2.waitKey(1)

print(time.ctime())
map1=generate_DFtoER_map(w, h, 1.0, 1.0, 1.0)

print (time.ctime())
krimg=cv2.remap(img, map1, None,
                cv2.INTER_LANCZOS4,
                dst=None,
                # BORDER_CONSTANT = 0
                # BORDER_DEFAULT = 4
                # BORDER_ISOLATED = 16
                # BORDER_REFLECT = 2
                # BORDER_REFLECT101 = 4
                # BORDER_REFLECT_101 = 4
                # BORDER_REPLICATE = 1
                # BORDER_TRANSPARENT = 5
                # BORDER_WRAP = 3
                borderMode=cv2.BORDER_REFLECT101)

print (time.ctime())
h,w,d=krimg.shape
print (h, w)
skrimg=cv2.resize(krimg,(w,h))
cv2.imshow("mapped",skrimg)
cv2.waitKey(1)
#
cv2.waitKey(0)
sys.exit()
#
cam=cv2.VideoCapture("../Images/R0010079.MP4")
writer = cv2.VideoWriter ()
fcc=cam.get(cv2.CAP_PROP_FOURCC)
fmt=cam.get(cv2.CAP_PROP_FORMAT)
fps = cam.get(cv2.CAP_PROP_FPS)
frame_size=(w/2, h/2)
ext='mp4v'
print ("frame size:(%d x %d)"%(w,h),"fps:",fps,"fourcc:","0x%x"%fcc,fcc,"format:",fmt)
fname=os.path.join(os.path.abspath("."),"converted.%s"%ext.rstrip())
if not writer.open(fname,
                   cv2.VideoWriter_fourcc(*ext),
                   fps, frame_size, isColor=True):
    print ("failed to open writer")
    sys.exit()
    
while 1:
    ret,img=cam.read()
    if not ret:
        break
    cimg=cv2.remap(img, map1, None,
                   cv2.INTER_LANCZOS4,
                   dst=None,
                   borderMode=cv2.BORDER_REFLECT101)
    simg=cv2.resize(cimg,frame_size)
    cv2.imshow("mapped",simg)
    writer.write(simg)
    cv2.waitKey(1)

writer.release()

if ext == "mp4v":
    # "Free MP4 Converter" does not recognise ".mp4v" extension.
    newfname=os.path.join(os.path.abspath("."),"converted.mp4")
    os.rename(fname,newfname)

#avconv -i myvideo.mp4 -acodec libvorbis -aq 5 -ac 2 -qmax 25 -threads 2 myvideo.webm
#avconv -i input.mp4 -threads 4 -b 50k b50k.webm
# use Free Mp4 Converter.
    
