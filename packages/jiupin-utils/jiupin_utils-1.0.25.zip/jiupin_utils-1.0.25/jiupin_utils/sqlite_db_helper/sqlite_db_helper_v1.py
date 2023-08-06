# -*- coding: utf-8 -*-
# boois flask 框架,作者:周骁鸣 boois@qq.com
"""sqlite_db_helper用来访问sqlite数据库"""
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # pylint: disable=no-member

class DbHelper(object):
    """sqlite的数据访问类"""
    def __init__(self):
        pass

    @staticmethod
    def execute_non_query(cmdtxt, mapping=None, db_info=""):
        """执行一条sql语句,不返回任何数据,用于update、insert等"""

        if cmdtxt == "":
            return True
        try:
            conn = sqlite3.connect(db_info)
            conn.text_factory = str
            if mapping is not None:
                conn.execute(cmdtxt, mapping)
            else:
                conn.execute(cmdtxt)
            conn.commit()
            conn.close()
            return True
        except Exception, ex:
            if vars().has_key('conn'):
                conn.close()
            raise ex

    @staticmethod
    def execute_non_query_bat(cmdtxt, mapping_arr, db_info=""):
        """批量执行sql语句,不返回记录"""
        if not isinstance(mapping_arr, list):
            return
        if len(mapping_arr) == 0:
            return
        try:
            conn = sqlite3.connect(db_info)
            for mapping in mapping_arr:
                conn.execute(cmdtxt, mapping)
            conn.commit()
            conn.close()
            return True
        except Exception, ex:
            if vars().has_key('conn'):
                conn.close()
            raise ex

    @staticmethod
    def execute_scalar(cmdtxt, mapping=None, db_info=""):
        """执行一条语句,并返回第一条记录"""
        if len(cmdtxt) == 0:
            return None

        def dict_factory(cursor, row):
            """这个是一个高级的链接处理工厂,可以作为conn.factory的设定值,可以按需返回高级的结果"""
            _dict = {}
            for idx, col in enumerate(cursor.description):
                _dict[col[0]] = row[idx]
            return _dict

        try:
            conn = sqlite3.connect(db_info)
            conn.row_factory = dict_factory
            # if cmdtxt.lower().find("limit") == -1:
            #     cmdtxt = cmdtxt.rstrip(";") + " LIMIT 1 OFFSET 0"
            cursor = conn.cursor()
            if mapping is None:
                cursor.execute(cmdtxt)
            else:
                cursor.execute(cmdtxt, mapping)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception, ex:
            if vars().has_key('conn'):
                conn.close()
            raise ex

    @staticmethod
    def each(cmdtxt, mapping=None, each_fn=None, db_info=""):
        """执行一条sql,取回多条数据并用each_fn(data)来遍历它"""
        try:
            def dict_factory(cursor, row):
                """这个是一个高级的链接处理工厂,可以作为conn.factory的设定值,可以按需返回高级的结果"""
                _dict = {}
                for idx, col in enumerate(cursor.description):
                    _dict[col[0]] = row[idx]
                return _dict

            conn = sqlite3.connect(db_info)
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            if mapping is None:
                cursor.execute(cmdtxt)
            else:
                cursor.execute(cmdtxt, mapping)
            result = cursor.fetchall()
            if len(result) > 0 and each_fn != None:
                for i in xrange(len(result)):
                    each_fn(result[i])
            cursor.close()
            return result
        except Exception, ex:
            if vars().has_key('conn'):
                conn.close()
            raise ex

    @staticmethod
    def paging(tab_name="", fields="*", where_str="", mapping=(), sort_str="", page_size=10,
               current_page=1, each_fn=None, counter=True, db_info=""):
        # pylint: disable=too-many-locals,too-many-arguments
        """分页方法"""
        try:
            def dict_factory(cursor, row):
                """这个是一个高级的链接处理工厂,可以作为conn.factory的设定值,可以按需返回高级的结果"""
                _dict = {}
                for idx, col in enumerate(cursor.description):
                    _dict[col[0]] = row[idx]
                return _dict

            rscount = 0
            conn = sqlite3.connect(db_info)
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            if current_page < 1:
                current_page = 1
            if counter:
                comtxttmp = "select count(*) as __rscount from {tab_name} {where_str} {sort_str};"
                cmdtxt = comtxttmp.format(
                    tab_name=tab_name,
                    where_str=(where_str if where_str == "" else " where " + where_str),
                    sort_str=(sort_str if sort_str == "" else " order by " + sort_str),
                    fields=fields,
                    page_size=page_size,
                    page=str((current_page - 1) * page_size)
                )
                if mapping is None:
                    cursor.execute(cmdtxt)
                else:
                    cursor.execute(cmdtxt, mapping)
                rscount = cursor.fetchone().get("__rscount", 0)
            comtxttmp = "select {fields} from {tab_name}  {where_str} {sort_str} limit {page_size} offset {page}"
            cmdtxt = comtxttmp.format(
                tab_name=tab_name,
                where_str=(where_str if where_str == "" else " where " + where_str),
                sort_str=(sort_str if sort_str == "" else " order by " + sort_str),
                fields=fields,
                page_size=page_size,
                page=str((current_page - 1) * page_size)
            )
            if mapping is None:
                cursor.execute(cmdtxt)
            else:
                cursor.execute(cmdtxt, mapping)
            result = cursor.fetchall()
            if len(result) > 0 and each_fn is not None:
                setnum = 0
                for i in xrange(len(result)):
                    if result[i].has_key("__rscount"):
                        rscount = int(result["__rscount"])
                        continue
                    # result[i]["__setNum"](str(setnum))#给返回的记录中添加结果集set的索引
                    each_fn(result[i])
                    setnum += 1
            cursor.close()
            return rscount
        except Exception, ex:
            if vars().has_key('conn'):
                conn.close()
            raise ex
