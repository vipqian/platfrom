
import time
from airtest.core.api import wait, touch, Template, shell, swipe, exists
from app.xuexiqingguo.initDevice import InitDevice
from common.getCode import GetCode
from common.db import ExeDataBase


class ApllyUser(InitDevice):

    def __init__(self, deviceID, user) -> None:
        super().__init__(deviceID)
        self.imageDir = f'{self.projectRoot}/app/xuexiqingguo/aplly/img'
        passwd = 'T8TqeyE4COp6'
        self.codePlat = GetCode(user, passwd)

    def apply(self, phone, name):
        self.logger.info(f'{name} aplloy for start phone: {phone}')
        count = 0
        while True:
            try:
                count += 1
                tempphone = self.codePlat.get_phone(phone)
                if phone == tempphone:
                    break
            except Exception as msg:
                self.logger.warning(msg)
                time.sleep(1)
                if count >= 10:
                    # 获取手机号失败
                    return '-1'

        wait(Template(f"{self.imageDir}/tpl1690357166049.png",
             record_pos=(0.246, -0.368), resolution=(1080, 1920)))
        touch(Template(f"{self.imageDir}/tpl1690357166049.png",
              record_pos=(0.246, -0.368), resolution=(1080, 1920)))
        wait(Template(f"{self.imageDir}/tpl1690357247730.png",
             record_pos=(-0.019, 0.537), resolution=(1080, 1920)))
        touch(Template(f"{self.imageDir}/tpl1690357306063.png",
              record_pos=(-0.289, -0.092), resolution=(1080, 1920)))
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(phone)
        )
        touch(Template(f"{self.imageDir}/tpl1690357469158.png",
              record_pos=(0.305, 0.05), resolution=(1080, 1920)))
        # 获取验证码
        count = 0
        while True:
            count += 1
            swipe(Template(f"{self.imageDir}/tpl1690357801325.png", record_pos=(-0.342,
                  0.233), resolution=(1080, 1920)), vector=[0.7429, -0.0025])
            time.sleep(2)
            if exists(Template(f"{self.imageDir}/tpl1690357927984.png", record_pos=(-0.048, 0.227), resolution=(1080, 1920))):
                break
            else:
                if count >= 5:
                    self.logger.error(
                        "Drag-and-drop to get verification code error")
                    return '-2'
        touch(Template(f"{self.imageDir}/tpl1690357987564.png", record_pos=(-0.192, 0.052), resolution=(1080, 1920)))
        code = self.codePlat.get_code()
        if code == '':
            self.logger.error('get code error')
            return '-3'
        # 输入验证吗
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(code)
        )
        # 输入用户名
        touch(Template(f"{self.imageDir}/tpl1690358012548.png",
              record_pos=(-0.287, 0.367), resolution=(1080, 1920)))
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(name)
        )
        # 申请理由
        touch(Template(f"{self.imageDir}/tpl1690379616212.png",
              record_pos=(-0.233, 0.344), resolution=(1080, 1920)))
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format('学习')
        )
        touch(Template(f"{self.imageDir}/tpl1690358146977.png",
              record_pos=(-0.015, 0.69), resolution=(1080, 1920)))
        try:
            wait(Template(f"{self.imageDir}/tpl1690705723016.png",
                 record_pos=(-0.003, -0.243), resolution=(1080, 1920)))
            self.logger.info(f'{name} {phone} aplly for success')
            return '1'
        except:
            self.logger.error('aplly page not find')
            return '-4'

    def click_back(self):
        touch(Template(f"{self.imageDir}/tpl1690380885670.png",
              record_pos=(-0.448, -0.756), resolution=(1080, 1920)))

    def main(self, data, tableName='xuexi'):
        mgDB = ExeDataBase(
            '/Users/yunfeiwang/project/platfrom/data/platfrom.txt')
        for i in data:
            name = i[0]
            phone = i[1]
            status = self.apply(phone, name)
            if status == '1':
                timStr = time.strftime('%Y_%m_%d %H:%M:%S')
                updateSql = f"""UPDATE "main"."{tableName}" SET "isApllyFor" = '1', "isApllyForTime" = '{timStr}' WHERE "phone" = '{phone}'"""
                mgDB.updata_data(updateSql)
                self.click_back()
            elif status == '-1':
                self.logger.error(f'{name} get phone error phone: {phone}')
            elif status == '-2':
                self.click_back()
            elif status == '-3':
                self.click_back()
            else:
                self.click_back()

