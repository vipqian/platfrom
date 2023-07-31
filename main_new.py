'''
Author: wangyunfei
Date: 2023-07-29 13:16:53
LastEditors: wangyunfei
LastEditTime: 2023-07-31 20:25:49
Description: file content
FilePath: /platfrom/main_new.py
'''

from app.xuexiqingguo.regitster.register import Register
from common.db import ExeDataBase


def main():
    # 来源
    source = '三拔子乡'
    # 数据库中的表名
    tableName = 'xuexi'
    # 手机的设备ID
    deviceID = 'b7ffe811'
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT name FROM {tableName} WHERE source='{source}'"
    registedList = []
    # 打码平台账号 
    user = 'wangyunfei1'
    for i in mgDB.select_data(sql):
        registedList.append(i[0])
    rfg = Register(deviceID, user)
    # 要注册的用户的文件
    nameFile = '/Users/yunfeiwang/project/platfrom/data/name2.txt'
    with open(nameFile, 'r') as f:
        data = f.read().split('\n')
    rfg.main(data, registedList, source)


if __name__ == '__main__':
    main()
