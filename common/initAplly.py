'''
Author: wangyunfei
Date: 2023-07-30 15:23:30
LastEditors: wangyunfei
LastEditTime: 2023-07-30 15:26:39
Description: file content
FilePath: /platfrom/common/initAplly.py
'''
from common.db import ExeDataBase


def init_aplly_for_data(source, tableName='xuexi'):
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT * FROM {tableName} WHERE source='{source}' and isApllyFor='0'"
    temp = mgDB.select_data(sql)
    data = []
    for userInfo in temp:
        phone = userInfo[0]
        name = userInfo[1]
        data.append((name, phone))
    return data
