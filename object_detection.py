#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/3 10:34
# @Author  : blvin.Don
# @File    : object_detection.py
import cv2, pyautogui
import numpy as np
global point1, point2
from math import fabs
global start, elapsed
import time
Kp = 0.2
# from UAV_tracking.Center import Get_Center
from socket import *
HOST = '192.168.0.101'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))

def send_msg(a,b,c,d,e):
    message = str(str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d)+ ',' + str(e))
    s.sendall(message.encode('utf-8'))
    print("send success!")

send_msg(0,0,0,4,0)


def get_zhongshu(alist):
    H_temp = []
    for h in alist:
        H_temp += list(h)
    counts = np.bincount(H_temp)
    return np.argmax(counts)

def myfind(x,y):
    return [ a for a in range(0,len(y),5) if y[a] == x]

def get_image():
    img = pyautogui.screenshot(region=[470, 0, 900, 425])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def control_command(offset_x, offset_y):
    global start, elapsed
    if fabs(offset_x) > 20:
        delta_x = (offset_x / 450.00) *90*Kp
        print("X:",0,0,delta_x, 4, 0)
        send_msg(0,0,delta_x, 4, 0)
        time.sleep(0.01)
    # if fabs(offset_x) <= 50:
    #     send_msg(0, 0, 0, 0, 0)
    if fabs(offset_y) > 10:
        delta_y = -(offset_y / 212.50)*2
        print("Y:",0, delta_y,0, 4, 0)
        send_msg(0, delta_y,0, 4, 0)
        start = time.clock()
    # if fabs(offset_y) <= 40:
    #     send_msg(0, 0, 0, 0, 0)
    if fabs(offset_y) <= 10 and fabs(offset_x) <= 20:
        send_msg(0,0,0,0,0)
    elapsed = (time.clock() - start)
    print("Duration:", elapsed)
    if elapsed > 3:
        print("emergent stop!")
        send_msg(0, 0, 0, 0, 0)


def on_mouse(event, x, y, flags, param):
    global point1, point2
    img = get_image()
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 5)
        # cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5) 
        cv2.imshow('image', img2)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])
        cut_img = img[min_y:min_y + height, min_x:min_x + width]
        # print(cut_img.shape)
        Img2_HSV = cv2.cvtColor(cut_img, cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(Img2_HSV)
        H_Z, S_Z, V_Z = get_zhongshu(H), get_zhongshu(S), get_zhongshu(V)
        # print(H_Z, S_Z, V_Z)
        while True:
            img = get_image()
            HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([int(H_Z) - 20, int(S_Z) - 20, int(V_Z) - 20])
            upper = np.array([int(H_Z) + 20, int(S_Z) + 20, int(V_Z) + 20])
            mask = cv2.inRange(HSV, lower, upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts)>0:
                c = max(cnts, key=cv2.contourArea)
                ((x,y),radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                print("center:",center)
                offset_x = center[0] - 450
                offset_y = center[1] - 213
                print("offset:",offset_x,offset_y)
                msg = control_command(offset_x,offset_y)
                if radius > 5:
                    cv2.circle(img, (int(x),int(y)), int(radius), (255, 0, 0), 2)

            cv2.imshow('image', img)
            if cv2.waitKey(10) == 27:
                break




def main():

    cv2.namedWindow('image')
    img = get_image()
    place = cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()