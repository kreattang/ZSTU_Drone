#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/3 9:39
# @Author  : blvin.Don
# @File    : get_screen_image.py


import pyautogui
import numpy as np
import cv2

img = pyautogui.screenshot(region=[470,0,900,425]) # x,y,w,h
# img.save('screenshot.png')
# img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
