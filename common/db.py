'''
Author: wangyunfei
Date: 2023-07-30 11:00:28
LastEditors: wangyunfei
LastEditTime: 2023-08-01 20:31:07
Description: file content
FilePath: /platfrom/common/db.py
'''

import sqlite3


class ExeDataBase():

    def __init__(self, dbFile) -> None:
        self.dbFile = dbFile

    def check_table(self, tablename='xuxiqiangguo'):
        conn = sqlite3.connect(self.dbFile)
        cur = conn.cursor()
        sql = '''SELECT tbl_name FROM sqlite_master WHERE type = 'table' '''
        cur.execute(sql)
        values = cur.fetchall()
        cur.close()
        conn.close()
        tables = []
        for v in values:
            tables.append(v[0])
        if tablename not in tables:
            return True  # 可以建表
        else:
            # 不可以键表
            return False

    def inster_db(self, tableName, data):

        conn = sqlite3.connect(self.dbFile)
        cur = conn.cursor()
        seqStr = f"""INSERT INTO "main"."{tableName}" ("phone", "name", "isNewUser", "isApllyFor", "source", "phoneType", "deviceID", "ctime",  "protype") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cur.executemany(seqStr, data)
        conn.commit()
        cur.close()
        conn.close()

    def select_data(self, selectSql):
        conn = sqlite3.connect(self.dbFile)
        cur = conn.cursor()
        cur.execute(selectSql)
    # 提取查询到的数据
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def updata_data(self, updateSql):
        conn = sqlite3.connect(self.dbFile)
        cur = conn.cursor()
        cur.execute(updateSql)
        conn.commit()
        cur.close()
        conn.close()

    # cur.execute('select * from xuex')
    # print(cur.fetchall())
