#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import datetime


def strtotime(txt):
    #2015-02-01
    try:
        p_tuple=time.strptime(txt,'%Y-%m-%d %H:%M:%S')
        return time.mktime(p_tuple)
    except:
        return 0
def format(stamp,fmt=None):
    if not fmt:
        fmt='%Y-%m-%d %H:%M:%S'
    p_tuple=time.localtime(stamp)
    return time.strftime(fmt,p_tuple)
def get_time_diff(stamp1,stamp2):
    #TODO 年月
    diff=abs(int(stamp2-stamp1))
    print diff
    res=[]
    # mon=diff/86400/30
    # if mon>0:
    #     res.append("%s个月"% mon)
    day=diff/86400
    if day>0:
        res.append("%s天"% day)
    diff2=diff%86400
    hour=diff2/3600
    if hour>0:
        res.append("%s小时" % hour)
    diff3=diff2%3600
    min=diff3/60
    if min>0:
        res.append("%s分" % min)
    sec=diff3%60
    if sec>0:
        res.append("%s秒" % sec)
    return "".join(res)

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')
if __name__ == '__main__':

    # print strtotime("2015-01-04 00:00:00")
    # a="2011-09-28 10:00:00"
    # p_tuple=time.strptime(a,'%Y-%m-%d %H:%M:%S')
    # print p_tuple
    # print type(p_tuple)
    #转化为时间戳
    # stamp=time.mktime(p_tuple)
    # print stamp
    #将时间戳转化为localtime
    # loaltime=time.localtime(stamp)
    # print loaltime
    #将时间戳格式化
    # datetime1=time.strftime('%Y-%m-%d %H:%M:%S',loaltime)
    # datetime1=time.strftime('%Y-%m-%d %H:%M:%S',p_tuple)
    # print datetime1

    # print get_time_diff(strtotime("2016-02-26 00:00:00"),strtotime("2017-06-26 12:34:23"))
    # print now()
    d1 = datetime.datetime.fromtimestamp(strtotime("2016-02-11 22:14:00"))
    # print type(d1)
    # time.sleep(3)
    d2 = datetime.datetime.now()
    d = d2-d1      ### 产生的是 datetime.timedelta 对象
    # print type(d)
    print d
    print d.days