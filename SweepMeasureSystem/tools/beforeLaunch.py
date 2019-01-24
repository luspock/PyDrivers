#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   1/12/2019 6:11 PM
# @Author   :   Luspock
# @File     :   beforeLaunch.py

import os
import sys

compileTasks = [['SMS.ui', 'Ui_MainWindow.py'],
                ['serial.ui', 'Ui_Serial.py']]

compiler = r"C:\Users\luspock\.virtualenvs\SweepMeasureSystem\Scripts\pyside2-uic.exe"

WorkingDirectory = sys.path[0] + "\\..\\"


def compile_ui():
    for task in compileTasks:
        os.system("{0} -x {1} -o {2}".format(compiler, WorkingDirectory+task[0], WorkingDirectory+task[1]))


if __name__ == "__main__":
    compile_ui()
