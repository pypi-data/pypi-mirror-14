#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient,cursor
conn = MongoClient("127.0.0.1",27017)
db = conn.jiupin #连接库
# lists=db.expo.find()
def to_dict(res):
    # print type(res)
    if isinstance(res,cursor.Cursor):
        out=[]
        for _ in res:
            del _['_id']
            out.append(_)
    else:
        del res['_id']
        out=res
    return out
