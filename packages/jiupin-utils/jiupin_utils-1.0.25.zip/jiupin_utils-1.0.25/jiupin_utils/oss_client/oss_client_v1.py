#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oss2
APP_ID='A3kzBRzEvHNpj0Ft'
APP_KEY='ShJJLCrQPgxt1EDJn8GFpyLYPEBPMw'
END_POINT='oss-cn-hangzhou.aliyuncs.com'
BUCKET='jiupin-static'
#
# TEST_PREFIX='jiupin-expo'

auth = oss2.Auth(APP_ID, APP_KEY)
service = oss2.Service(auth, END_POINT)
# print([b.name for b in oss2.BucketIterator(service)])
bucket = oss2.Bucket(auth, END_POINT, BUCKET)
def list_files(path):
    res=bucket.list_objects(path)
    out=[]
    for x in res.object_list:
        if not x.key.endswith("/"):
            out.append(x.key)
    return out
def put_object(object,content):
    return bucket.put_object(object,content)

def is_exists(path):
    try:
        bucket.head_object(path)
        return True
    except Exception,e:
        print e
        return False
def get_last_modified(object):
    try:
        res=bucket.head_object(object)
        # print res
        return res.last_modified
    except:
        return ""
if __name__ == '__main__':
    # print list_files("expo/c5284bf6a9e241048c0ee3ce481ba1f8/head_imgs")
    #http://jiupin-static.oss-cn-hangzhou.aliyuncs.com/vcard/bc97a7bf6d2d413d8f3841d08a19785c/back_img.jpg?v=1457156751.01&v=1457156751.01
    # print is_exists("vcard/bc97a7bf6d2d413d8f3841d08a19785c/back_img.jpg&a")
    # print is_exists("vcard/bc97a7bf6d2d413d8f3841d08a19785c/back_img.jpg")
    res= bucket.head_object("app/apk/b.apk")
    print dir(res)
