'''
Author: wangyunfei
Date: 2023-08-01 22:25:15
LastEditors: wangyunfei
LastEditTime: 2023-08-01 22:47:09
Description: file contentm
FilePath: /platfrom/util/write_excel.py
'''

import xlrd
import xlwt
from xlutils.copy import copy
from common.db import ExeDataBase


def write_to_excel(words, filename, sheet_name='sheet1'):
    '''
    将item存储到excel中。
    :param words: 保存item的list    [{},{}]格式
    :return:
    '''
    try:
        # 1、创建工作薄
        work_book = xlwt.Workbook(encoding='utf-8')
        # 2、创建sheet表单
        sheet = work_book.add_sheet(sheet_name)
        # 3、写表头
        # head = ['英文','中文']
        head = []
        for k in words[0].keys():
            head.append(k)

        for i in range(len(head)):
            sheet.write(0, i, head[i])
        # 4、添加内容
        # 行号
        i = 1
        for item in words:
            for j in range(len(head)):
                sheet.write(i, j, item[head[j]])
            # 写完一行，将行号+1
            i += 1
        # 保存
        work_book.save(filename)
        print('写入excel成功！')

    except Exception as e:
        print('写入excel失败！', e)


def init_data(source, tableName='xuexi'):
    mgDB = ExeDataBase('/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
    sql = f"SELECT * FROM {tableName} WHERE source='{source}'"
    dbData = mgDB.select_data(sql)
    data = []
    # ('17308351425', '胡建军', '0', '1', '胡杖子', 'vivox9', 'b7ffe811', '2023_08_01 21:31:40', '2023_08_01 22:01:12', '学习强国')
    for i in dbData:
        temp = {}
        temp['姓名'] = i[1]
        temp['电话'] = i[0]
        if i[2] == '1':
            temp['新用户'] = '是'
        else:
            temp['新用户'] = '否'
        data.append(temp)
    print(data)
    return data
if __name__ == '__main__':
    source = '胡杖子'
    init_data()
