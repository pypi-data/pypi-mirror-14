#!python
#-*- coding:utf-8 -*-
"""
Converting a movie file from Theta-S, MP4 file format with 
dual fishey projection, to Equiangular projection movie.

You need to converte movie into webm format file using
other application , such as "Free MP4 Converter".
"""
from __future__ import print_function

import cv2
import numpy
import time

import os,os.path
import sys
sys.path.insert(0,"./build/lib.macosx-10.6-intel-2.7")

from generate_DF_to_ER_map import generate_DFtoER_map

def DFtoER(fn,scale=1.0,outdir="."):
    cam=cv2.VideoCapture(fn)
    ret,img=cam.read()
    h,w,d=img.shape
    #print (h, w)
    #print(time.ctime())
    sh=int(scale*h+0.5)
    sw=int(scale*w+0.5)
    map1=generate_DFtoER_map(w,h,0.895)
    # open writer
    writer = cv2.VideoWriter ()
    fcc=cam.get(cv2.CAP_PROP_FOURCC)
    fmt=cam.get(cv2.CAP_PROP_FORMAT)
    fps = cam.get(cv2.CAP_PROP_FPS)
    frame_size=(sw, sh)
    ext='mp4v'
    fname="%s%s%s"%(os.path.join(os.path.abspath(outdir),
                                os.path.splitext(os.path.basename(fn))[0]),
                    os.path.extsep,
                    "m4v")
    if not writer.open(fname,
                       cv2.VideoWriter_fourcc(*ext),
                       fps, frame_size, isColor=True):
        print ("failed to open writer")
        sys.exit()
    print ("output to ",fname)
    cam=cv2.VideoCapture(fn)
    while 1:
        ret,img=cam.read()
        if not ret:
            break
        erimg=cv2.remap(img, map1, None,
                   cv2.INTER_LANCZOS4,
                   dst=None,
                   borderMode=cv2.BORDER_REFLECT101)
        erimg=cv2.resize(erimg, (sw,sh))
        cv2.imshow("mapped", erimg)
        writer.write(erimg)
        cv2.waitKey(1)
    writer.release()
    print ("Done")
    
#avconv -i myvideo.mp4 -acodec libvorbis -aq 5 -ac 2 -qmax 25 -threads 2 myvideo.webm
#avconv -i input.mp4 -threads 4 -b 50k b50k.webm
# use Free Mp4 Converter.
    

if __name__ == "__main__":
    
    #DFtoER("../Images/R0010080.MP4", 0.5, "../Movies")
    DFtoER("../Images/R0010079.MP4", 0.5, "../Movies")
