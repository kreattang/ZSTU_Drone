#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 21:31
# @Author  : blvin.Don
# @File    : Center.py

from sklearn.cluster import KMeans
import numpy as np
from collections import Counter

def counter(arr):
    return Counter(arr).most_common(2)

def label(li):
    Y = []
    for l in li:
        Y.append(l[1])
    return Y.index(max(Y))

def Get_Center(X):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    temp = kmeans.cluster_centers_[int(label(counter(kmeans.labels_)))]
    return [int(temp[0]),int(temp[1])]