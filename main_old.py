'''
Author: wangyunfei
Date: 2023-07-29 13:16:53
LastEditors: wangyunfei
LastEditTime: 2023-08-01 21:36:51
Description: file content
FilePath: /platfrom/main_old.py
'''

from app.xuexiqingguo.regitster.register import Register
from app.xuexiqingguo.aplly.aplly import ApllyUser
from common.db import ExeDataBase
from common.initAplly import init_aplly_for_data


def main():
    source = '胡杖子'
    tableName = 'xuexi'
    deviceID = '1d3b47dd'
    user = 'wangyunfei'

    # 注册
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT name FROM {tableName} WHERE source='{source}'"
    registedList = []
    for i in mgDB.select_data(sql):
        registedList.append(i[0])
    rfg = Register(deviceID, user)
    nameFile = '/Users/yunfeiwang/project/platfrom/data/name1.txt'
    with open(nameFile, 'r') as f:

        data = f.read().split('\n')
    rfg.main(data, registedList, source)

    # 申请
    # aplly = ApllyUser(deviceID, user)
    # apllyData = init_aplly_for_data(source, tableName)
    # print(apllyData)
    # aplly.main(apllyData)


if __name__ == '__main__':
    main()