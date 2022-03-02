# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:25:31 2022

@author: DestRuktoR
"""
import cv2 
import numpy as np
import datetime
import time
import pymysql
import os

Make = pymysql.connect(host='localhost', user = 'server', passwd = 'Dabase', db = 'performance')
MySQL = Make.cursor()

cap = cv2.VideoCapture(0)
start_timeframe = datetime.datetime.now()

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorKNN()
    
time.sleep(1)
total_frames = 0

while(1):
        
    total_frames += 1
        
    ret, frame = cap.read()
        
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    current_framediff = datetime.datetime.now() - start_timeframe

    fps = total_frames/current_framediff.seconds
    temperature = os.popen("cat /sys/class/thermal/thermal_zone0/temp")    

    MySQL.execute(f"INSERT INTO Temp_FPS(Epoch, FPS, Temperature) VALUES({current_framediff.seconds}, {fps}, {temperature.read()});")

    print(fps)

    cv2.imshow('Frame',fgmask)
        
    if cv2.waitKey(1) == 13:
        break
        
cap.release()
 
Make.commit()


cv2.destroyAllWindows()
Make.close()
MySQL.close()
