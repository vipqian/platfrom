'''
Author: wangyunfei
Date: 2023-07-29 13:16:53
LastEditors: wangyunfei
LastEditTime: 2023-07-30 16:45:32
Description: file content
FilePath: /platfrom/main_new.py
'''

from app.xuexiqingguo.regitster.register import Register
from common.db import ExeDataBase


def main():
    source = '三拔子乡'
    tableName = 'xuexi'
    deviceID = 'b7ffe811'
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT name FROM {tableName} WHERE source='{source}'"
    registedList = []
    user = 'wangyunfei1'
    for i in mgDB.select_data(sql):
        registedList.append(i[0])
    rfg = Register(deviceID, user)
    nameFile = '/Users/yunfeiwang/project/platfrom/data/name2.txt'
    with open(nameFile, 'r') as f:

        data = f.read().split('\n')
    rfg.main(data, registedList, source)


if __name__ == '__main__':
    main()
