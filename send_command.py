#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/6 15:02
# @Author  : blvin.Don
# @File    : send_command.py

from socket import *
HOST = '192.168.31.105'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))



def send_msg(a,b,c,d,e):
    message = str(str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d)+ ',' + str(e))
    s.sendall(message.encode('utf-8'))
    print("send success!")
