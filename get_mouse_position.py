#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/3 10:08
# @Author  : blvin.Don
# @File    : get_mouse_position.py


import os,time
import pyautogui as pag
try:
    while True:
            print("Press Ctrl-C to end")
            x,y = pag.position() #返回鼠标的坐标
            posStr="Position:"+str(x).rjust(4)+','+str(y).rjust(4)
            print (posStr)#打印坐标
            time.sleep(0.2)
            os.system('cls')#清楚屏幕
except  KeyboardInterrupt:
    print ('end....')