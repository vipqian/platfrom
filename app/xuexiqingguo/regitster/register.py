'''
Author: wangyunfei
Date: 2023-07-29 21:38:58
LastEditors: wangyunfei
LastEditTime: 2023-08-01 21:34:09
Description: file content
FilePath: /platfrom/app/xuexiqingguo/regitster/register.py
'''

from airtest.core.api import start_app, shell, wait, Template, stop_app, touch
from airtest.core.api import exists, swipe, clear_app
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time

from app.xuexiqingguo.initDevice import InitDevice
from common.getCode import GetCode
from common.db import ExeDataBase


class Register(InitDevice):

    def __init__(self, deviceID, user, phoneType='vivox9') -> None:
        self.appName = 'cn.xuexi.android'
        super().__init__(deviceID)
        self.deviceID = deviceID
        self.timeout = 30
        self.imageDir = f'{self.projectRoot}/app/xuexiqingguo/regitster/img'
        passwd = 'T8TqeyE4COp6'
        self.codePlat = GetCode(user, passwd)
        self.clear_app_data()
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        self.phoneType = phoneType

    def register_app(self, user: str, phone: str, status=True):
        """对用户进行注册
        返回码说明:1、注册成功  -1、页面加载失败或其他失败 -2、获取验证码失败

        Args:
            user (str): 用户名
            phone (str): 电话号
            status (bool, optional): 是否为清理后的app启动. Defaults to True.

        Returns:
            1, -1, -2
        """
        # 如果是新登录的输入显示输入手机号
        if status:
            try:
                wait(Template(f"{self.imageDir}/tpl1690648538628.png",
                              record_pos=(0.001, -0.142),
                              resolution=(1080, 1920)),
                     timeout=self.timeout)
            except Exception as msg:
                self.logger.error("input phone not find")
                return '-1'
        else:

            # 进入app后查看是否有删除的按钮
            try:
                delButton = wait(Template(f"{self.imageDir}/tpl1690098259837.png",
                                          record_pos=(0.374, -0.138),
                                          resolution=(1080, 1920)),
                                 timeout=self.timeout)
            except Exception as msg:
                self.logger.error('del button not find')
                return '-1'
            touch(delButton)
        # # 输入电话号
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(phone)
        )
        # 点击注册按钮
        touch(Template(f"{self.imageDir}/tpl1689771971007.png",
              record_pos=(-0.008, 0.41), resolution=(1080, 1920)))
        try:
            # 等待进入到新用户注册页面
            wait(Template(f"{self.imageDir}/tpl1690207110253.png",
                          record_pos=(-0.238, -0.56),
                          resolution=(1080, 1920)),
                 timeout=self.timeout)
        except Exception as msg:
            self.logger.error('regist page not find')
            return -1
        # 再次检查是否收入手机号
        if exists(Template(f"{self.imageDir}/tpl1690207320759.png",
                           record_pos=(-0.034, -0.218),
                           resolution=(1080, 1920))):
            # 重新输入手机号码
            shell(
                "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(phone)
            )
        # 点击同意协议
        touch(Template(f"{self.imageDir}/tpl1689772640868.png",
                       record_pos=(-0.394, 0.081), resolution=(1080, 1920)))
        # 存在点击下一步
        touch(Template(f"{self.imageDir}/tpl1689772694672.png",
                       record_pos=(-0.007, -0.047), resolution=(1080, 1920)))
        # 退拽验证
        count = 0
        while True:
            count += 1
            try:
                swipe(Template(f"{self.imageDir}/tpl1689773657123.png",
                               record_pos=(-0.278, 0.11),
                               resolution=(1080, 1920)),
                      Template(f"{self.imageDir}/tpl1689773768362.png",
                               record_pos=(0.144, 0.119),
                               resolution=(1080, 1920)), duration=5, steps=40)
            except Exception as msg:
                self.logger.info(msg)
                self.logger.warning('swipe error count : {}'.format(count))
            time.sleep(2)
            # 检查是否进入到下一个页面
            if exists(Template(
                f"{self.imageDir}/tpl1690207551389.png",
                    record_pos=(-0.209, -0.565), resolution=(1080, 1920))):
                break
            else:
                if count >= 5:
                    self.logger.error(
                        "swipe error count >= {}, register Error".format(
                            count))
                    return -1

        # 输入code码
        code = self.codePlat.get_code()
        if code == '':
            self.logger.info(f'{phone} get code error')
            return '-2'
        self.logger.info(f'{phone} get code: {code}')
        shell(
            "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(code)
        )
        # 检查code码验证成功
        try:
            # 检查页面上上有输入密码字样
            wait(Template(f"{self.imageDir}/tpl1690301022717.png",
                 record_pos=(-0.225, -0.561), resolution=(1080, 1920)))
            # 输入密码
            shell(
                "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(
                    '12345678')
            )
            # 点击下一步
            touch(Template(f"{self.imageDir}/tpl1690301078941.png", record_pos=(
                0.001, 0.048), resolution=(1080, 1920)))
            # 等待填写基本信息
            wait(Template(f"{self.imageDir}/tpl1690208472011.png", rgb=False,
                 record_pos=(-0.218, -0.563), resolution=(1080, 1920)),
                 timeout=10)
            # 输入用户名
            shell(
                "am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(user)
            )
            # 点击进行学习强国
            touch(Template(f"{self.imageDir}/tpl1690208724236.png",
                  record_pos=(-0.019, 0.019), resolution=(1080, 1920)))
            time.sleep(3)
            return '1'
        except Exception as msg:
            self.logger.warning("The Enter password page is not displayed")
            return '-1'

    def change_name(self, name):
        # 点击我的页面
        touch(Template(f"{self.imageDir}/tpl1690209180907.png", record_pos=(0.415, -0.756), resolution=(1080, 1920)))
        # 进入到用户页面
        touch(Template(f"{self.imageDir}/tpl1690815389908.png", record_pos=(0.425, -0.601), resolution=(1080, 1920)))
        try:
            # 等待计入我的页面是否成功
            wait(Template(f"{self.imageDir}/tpl1690815432386.png", record_pos=(-0.003, -0.744), resolution=(1080, 1920)))
        except:
            # 没有进入到我的页面返回-1
            self.logger.error('My info page is not displayed')
            return False
        # 点击昵称
        touch(Template(f"{self.imageDir}/tpl1690815442413.png", record_pos=(-0.179, -0.428), resolution=(1080, 1920)))
        # 修改用户名
        self.poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android.widget.EditText").set_text(name)
        # 点击提交按钮
        touch(Template(f"{self.imageDir}/tpl1690891761420.png", record_pos=(0.229, -0.237), resolution=(1080, 1920)))
        time.sleep(2)
        return True

    def clear_app_data(self):
        """清理数据后启动app
        """
        clear_app(self.appName)
        start_app(self.appName)
        try:
            wait(Template(f"{self.imageDir}/tpl1690649698361.png",
                 record_pos=(-0.006, -0.259), resolution=(1080, 1920)))
        except:
            self.logger.error('Boot page not found')
            return
        touch(Template(f"{self.imageDir}/tpl1690649714682.png",
              record_pos=(0.184, 0.34), resolution=(1080, 1920)))

    def get_code_error(self):
        """获取咱证码错误的处理
        """
        touch(Template(f"{self.imageDir}/tpl1690468010508.png",
              record_pos=(-0.415, -0.76), resolution=(1080, 1920)))
        wait(Template(f"{self.imageDir}/tpl1690468041670.png",
             record_pos=(-0.257, -0.56), resolution=(1080, 1920)))
        touch(Template(f"{self.imageDir}/tpl1690468048999.png",
              record_pos=(-0.418, -0.754), resolution=(1080, 1920)))

    def get_regist_phone(self):
        """获取已经注册过的手机号

        Returns:
            _list_: 已经注册过的手机号列表
        """
        with open('/Users/yunfeiwang/project/platfrom/data/phone.txt', 'r') as f:
            return f.read().split('\n')

    def updata_regist_phone(self, phone):
        """更新已经注册过的手机号

        Args:
            phone (_str_): 手机号
        """
        with open('/Users/yunfeiwang/project/platfrom/data/phone.txt', 'a+') as f:
            f.write(f'{phone}\n')

    # def main(self, source: str, q):
    #     """对用户列表中的用户进行注册

    #     Args:
    #         data (list): 用户列表
    #     """
    #     self.logger.info('111111111111')
    #     dbfile = '/Users/yunfeiwang/project/platfrom/data/platfrom.txt'
    #     myDB = ExeDataBase(dbfile)
    #     startTime = time.time()
    # #     appStatus = True
    # while not q.empty():
    #         name = q.get()
    #         if len(name) == 0:
    def main(self, data: list, registedList: list, source: str):
        """对用户列表中的用户进行注册

        Args:
            data (list): 用户列表
        """
        dbfile = '/Users/yunfeiwang/project/platfrom/data/platfrom.txt'
        myDB = ExeDataBase(dbfile)
        startTime = time.time()
        appStatus = True
        for name in data:
            if len(name) == 0:
                continue
            if name in registedList:
                self.logger.info(f'{name} is eregistred')
                continue
            self.logger.info(f"{name} register start")
            while True:
                registPhone = self.get_regist_phone()
                phone = self.codePlat.get_phone()
                if phone in registPhone:
                    self.logger.warning(f'{phone} has been registered')
                    continue
                status = self.register_app(name, phone, appStatus)
                if status == '1':
                    self.updata_regist_phone(phone)
                    timStr = time.strftime('%Y_%m_%d %H:%M:%S')
                    data = [(phone, name, '1', '0', source, self.phoneType ,
                             self.deviceID, timStr, '学习强国')]
                    myDB.inster_db('xuexi', data)
                    self.logger.info(
                        f"{name} register success, phone: {phone}")
                    self.clear_app_data()
                    appStatus = True
                    break
                elif status == '-2':
                    self.get_code_error()
                    appStatus = False
                else:
                    appStatus = True
                    if exists(Template(f"{self.imageDir}/tpl1690208846273.png", record_pos=(-0.389, -0.757), resolution=(1080, 1920))):
                        self.logger.warning(f'{phone} has been registered')
                        if self.change_name(name):
                            self.updata_regist_phone(phone)
                            timStr = time.strftime('%Y_%m_%d %H:%M:%S')
                            data = [(phone, name, '0', '0', source, self.phoneType, self.deviceID, timStr, '学习强国')]
                            myDB.inster_db('xuexi', data)
                            self.clear_app_data()
                            break
                        else:
                            self.clear_app_data()
                    else:
                        stop_app(self.appName)
                        start_app(self.appName)
            self.logger.info("{} register finish duration: {:.2f}".format(
                name, time.time()-startTime))
