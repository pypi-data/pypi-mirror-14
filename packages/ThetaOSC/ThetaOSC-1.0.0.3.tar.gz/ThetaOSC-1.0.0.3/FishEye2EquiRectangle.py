#!/usr/bin/python
"""
This should not be included into the distribution
"""
import cv2

def test():
    cap=cv2.VideoCapture("../Images/R0010001.m4v")
    ret,img=cap.read()[1]
    cv2.imshow("test",img)
    # img.shape(1080, 1920, 3)
    limg=image[:960,:960,:]
    rimg=image[:960,960:,:]
    cv2.imshow("left",limg)
    cv2.imshow("right",rimg)
    return

