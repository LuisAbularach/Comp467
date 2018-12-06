import numpy as np
import cv2

def drawcircle(image, center, radius):
    cv2.circle(image, center, radius, (255,255,255), thickness=1, lineType=8, shift=0)