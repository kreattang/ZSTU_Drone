#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 20:43
# @Author  : blvin.Don
# @File    : goto_object_area.py

import time
from socket import *
import csv


HOST = '192.168.0.100'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))

def get_time():
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    return now
fname = get_time()+r"trajectory_info.txt"
file = open('I:/PycharmProjects/UAV_ZSTU/UAV_tracking/logs/'+fname,'w')
def write_trajectory(file,msg):
    file.writelines(msg)
    file.writelines("\n")


def send_msg(a,b,c,d,e):
    message = str(str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d)+ ',' + str(e))
    s.sendall(message.encode('utf-8'))
    print("send success!")


# 飞到4m
send_msg(0,0,0,4,0)
write_trajectory(file,get_time()+","+str((0,0,0,4,0)))
time.sleep(4)

# 向前飞4m
send_msg(0, 0.8 ,0, 4, 0)
write_trajectory(file,get_time()+","+str((0, 0.8 ,0, 4, 0)))
time.sleep(20)


# 停止
send_msg(0, 0 ,0, 0, 0)
write_trajectory(file,get_time()+","+str((0, 0.4 ,0, 4, 0)))

# 向左飞4m
send_msg(0, 0,-30, 4, 0)
write_trajectory(file,get_time()+","+str((0, 0,-30, 4, 0)))
time.sleep(2)

# 前进
send_msg(0, 0.8 ,0, 4, 0)
write_trajectory(file,get_time()+","+str((0, 0.8 ,0, 4, 0)))
time.sleep(5)

# 停止
send_msg(0, 0 ,0, 0, 0)
write_trajectory(file,get_time()+","+str((0, 0.4 ,0, 4, 0)))