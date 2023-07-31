'''
Author: wangyunfei
Date: 2023-07-29 13:21:49
LastEditors: wangyunfei
LastEditTime: 2023-07-30 16:58:34
Description: file content
FilePath: /platfrom/app/xuexiqingguo/initDevice.py
'''

from airtest.cli.parser import cli_setup
from airtest.core.api import auto_setup
import time
import os


from util.logger import LogSignleton


class InitDevice:
    def __init__(self, deviceID) -> None:
        runLog = 'device_{}_{}.log'.format(deviceID, time.strftime('%Y%m%d'))
        self.logger = LogSignleton(runLog).get_logger()
        self.projectRoot = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../../'))
        logDir = os.path.abspath(
            os.path.join(self.projectRoot, 'log', 'script', deviceID,
                         '{}'.format(time.strftime('%Y%m%d'))
                         )
        )
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        if not cli_setup():

            auto_setup(
                __file__,
                logdir=logDir,
                devices=[
                    "android://127.0.0.1:5037/{}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH".format(
                        deviceID)
                ],
                project_root=self.projectRoot
            )
