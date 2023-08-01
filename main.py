'''
Author: wangyunfei
Date: 2023-07-29 13:16:53
LastEditors: wangyunfei
LastEditTime: 2023-08-01 21:20:10
Description: file content
FilePath: /platfrom/main_old.py
'''

from app.xuexiqingguo.regitster.register import Register
from app.xuexiqingguo.aplly.aplly import ApllyUser
from common.db import ExeDataBase
from common.initAplly import init_aplly_for_data
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from util.logger import LogSignleton
from util.read_excel import ReadExcel


import time
from multiprocessing import Pool, Manager


def main():
    runLog = 'main_{}.log'.format(time.strftime('%Y%m%d'))
    logger = LogSignleton(runLog).get_logger()
    excelpath = '/Users/yunfeiwang/Desktop/name.xls'
    sheet = "Sheet1"
    data = ReadExcel(excelpath, sheet).data_list()

    source = '胡杖子'
    tableName = 'xuexi'
    deviceID = '1d3b47dd'
    deviceID1 = 'b7ffe811'
    user = 'wangyunfei'
    user1 = 'wangyunfei1'

    # 注册
    logger.info('开始进行注册')
    logger.info(f'来源:{source}')
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT name FROM {tableName} WHERE source='{source}'"
    registedList = []
    for i in mgDB.select_data(sql):
        registedList.append(i[0])
    logger.info('已经注册的用户{}'.format(registedList))
    q = Manager().Queue()

    rfg = Register(deviceID, user)
    rfg1 = Register(deviceID1, user1)

    count = 0
    for i in data:
        if i['name'] in registedList:
            logger.warning(f"{i['name']}已经被注册过")
        else:
            count += 1
            q.put(i['name'])
            if count >= 30:
                break

    m1 = rfg.main
    m2 = rfg1.main

    pool = Pool(2)
    pool.apply_async(m1, (source, q,))
    pool.apply_async(m2, (source, q,))

    pool.close()
    pool.join()

    # 申请
    # aplly = ApllyUser(deviceID, user)
    # apllyData = init_aplly_for_data(source, tableName)
    # print(apllyData)
    # aplly.main(apllyData)


if __name__ == '__main__':
    main()
