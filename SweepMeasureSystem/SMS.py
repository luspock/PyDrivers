#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   1/10/2019 11:37 PM
# @Author   :   Luspock
# @File     :   SMS.py

import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QOpenGLWidget
from PySide2.QtCore import QTimer
from PySide2.QtGui import QTextCursor
from Ui_MainWindow import Ui_MainWindow
from Ui_Serial import Ui_SerialWindow

import serial
from PySerialPatched import comports  # patched list port function (virtual serial port)

import random
import numpy as np
import time


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.setWindowTitle("Sweep Measure System (SMS)")

        self.ui_serial = Ui_SerialWindow()
        self.ui_serial.setupUi(self.ui_main.tabSerial)  # register the serial page into tabwidget.tabSerial
        self.ui_main.tabWidget.setCurrentIndex(0)

        # matplot setting
        self.fig = Figure(figsize=(8, 4.5), dpi=100)
        self.static_canvas = FigureCanvas(self.fig)
        self.static_canvas.setParent(self.ui_main.tabPlot)

        self.axes = self.fig.add_subplot(211)
        self.axes_dynamic = self.fig.add_subplot(212)

        data = [random.random() for i in range(25)]

        self.axes.plot(data, '-r', linewidth=2.0)
        self.static_canvas.draw()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(20)
        # self.timer.stop()  # shutdown

        # serial settings
        self.ser = serial.Serial()
        self.Com_Dict = {}

        # counting
        self.data_bytes_sent = 0
        self.ui_serial.leSerialPortDataBytesSent.setText(str(self.data_bytes_sent))
        self.ui_serial.leSerialPortDataBytesSent.setEnabled(False)
        self.data_bytes_received = 0
        self.ui_serial.leSerialPortDataBytesReceived.setText(str(self.data_bytes_received))
        self.ui_serial.leSerialPortDataBytesReceived.setEnabled(False)

        # ui_serial serial default settings
        default_index = self.ui_serial.cbbSerialPortBaudrate.findText("9600")  # baudrate
        if default_index == -1:
            self.ui_serial.cbbSerialPortBaudrate.setCurrentIndex(0)
        else:
            self.ui_serial.cbbSerialPortBaudrate.setCurrentIndex(default_index)
        default_index = self.ui_serial.cbbSerialPortDatabit.findText("8")  # Databit
        if default_index == -1:
            self.ui_serial.cbbSerialPortDatabit.setCurrentIndex(0)
        else:
            self.ui_serial.cbbSerialPortDatabit.setCurrentIndex(default_index)
        default_index = self.ui_serial.cbbSerialPortParity.findText("N")  # Parity
        if default_index == -1:
            self.ui_serial.cbbSerialPortParity.setCurrentIndex(0)
        else:
            self.ui_serial.cbbSerialPortParity.setCurrentIndex(default_index)
        default_index = self.ui_serial.cbbSerialPortStopbit.findText("1")  # Stopbit
        if default_index == -1:
            self.ui_serial.cbbSerialPortStopbit.setCurrentIndex(0)
        else:
            self.ui_serial.cbbSerialPortStopbit.setCurrentIndex(default_index)

        self.ui_serial.btnSerialCLose.setEnabled(False)

        # Receive Timer
        self.receive_timer = QTimer(self)
        self.receive_timer.timeout.connect(self.receive_data)

        # ui_serial slot connection
        self.ui_serial.btnCheckSerialPort.clicked.connect(self.check_serial_port)
        self.ui_serial.btnSerialOpen.clicked.connect(self.open_serial_port)
        self.ui_serial.btnSerialCLose.clicked.connect(self.close_serial_port)
        self.ui_serial.btnSerialPortSend.clicked.connect(self.send_data)
        self.ui_serial.btnSerialPortSendClear.clicked.connect(self.clear_send_data)
        self.ui_serial.btnSerialPortReceiveClear.clicked.connect(self.clear_receive_data)

        # OpenGL setup
        self.openGL = QOpenGLWidget()
        self.openGL.setParent(self.ui_main.tabOpenGL)
        self.openGL.initializeGL = self.init_gl
        self.openGL.initializeGL()
        self.openGL.resizeGL(851, 651)
        self.openGL.paintGL = self.paint_gl
        self.update_times = 0

        self.timer_gl = QTimer()
        self.timer_gl.timeout.connect(self.openGL.update)
        self.timer_gl.start(20)

    def init_gl(self):
        gluPerspective(45, 851 / 651, 0.1, 50.0)
        gluLookAt(8.0, 8.0, 4.0, 0.0, 0.0, 0.0, -1, -1, 1)

    def paint_gl(self):
        glClear(GL_COLOR_BUFFER_BIT)
        line_length = 4
        cur_line_size = 5
        cube_length = 2.0
        glPushMatrix()
        glPushMatrix()
        glRotatef(self.update_times * 10, 0.0, 0.0, 1.0)

        glLineWidth(cur_line_size)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(line_length, 0.0, 0.0)
        glEnd()
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, line_length, 0.0)
        glEnd()
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, line_length)
        glEnd()
        glPopMatrix()

        glTranslate(-0.5*cube_length, -0.5*cube_length, -0.5*cube_length)
        glColor3f(1, 1, 0)
        glBegin(GL_QUAD_STRIP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, cube_length, 0.0)
        glVertex3f(cube_length, 0.0, 0.0)
        glVertex3f(cube_length, cube_length, 0.0)
        glVertex3f(cube_length, 0.0, -cube_length)
        glVertex3f(cube_length, cube_length, -cube_length)
        glVertex3f(0.0, 0.0, -cube_length)
        glVertex3f(0.0, cube_length, -cube_length)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, cube_length, 0.0)
        glEnd()
        glBegin(GL_QUAD_STRIP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(cube_length, 0.0, 0.0)
        glVertex3f(0.0, 0.0, -cube_length)
        glVertex3f(cube_length, 0.0, -cube_length)
        glVertex3f(0.0, cube_length, 0.0)
        glVertex3f(cube_length, cube_length, 0.0)
        glVertex3f(0.0, cube_length, -cube_length)
        glVertex3f(cube_length, cube_length, -cube_length)
        glEnd()
        glPopMatrix()
        self.update_times += 1

    def check_serial_port(self):
        # check virtual seiral port
        for port, desc, hwid in sorted(comports()):
            print("%s: %s [%s]" % (port, desc, hwid))
        port_list = list(sorted(comports()))
        self.ui_serial.cbbSerialPorts.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            # print(self.Com_Dict)
            self.ui_serial.cbbSerialPorts.addItem(port[0])
        if len(port_list) == 0:
            print("No serial port found")

    def open_serial_port(self):
        data_bits = {'5': serial.FIVEBITS,
                     '6': serial.SIXBITS,
                     '7': serial.SEVENBITS,
                     '8': serial.EIGHTBITS}
        parity = {'N': serial.PARITY_NONE,
                  'Odd': serial.PARITY_ODD,
                  'Even': serial.PARITY_EVEN}
        stop_bits = {'1': serial.STOPBITS_ONE,
                     '1.5': serial.STOPBITS_ONE_POINT_FIVE,
                     '2': serial.STOPBITS_TWO}
        self.ser.port = self.ui_serial.cbbSerialPorts.currentText()
        self.ser.baudrate = int(self.ui_serial.cbbSerialPortBaudrate.currentText())
        self.ser.bytesize = data_bits[self.ui_serial.cbbSerialPortDatabit.currentText()]
        self.ser.parity = parity[self.ui_serial.cbbSerialPortParity.currentText()]
        self.ser.stopbits = stop_bits[self.ui_serial.cbbSerialPortStopbit.currentText()]
        print("Serial Port: {0} {1} {2} {3}".format(self.ser.port, self.ser.baudrate,
                                                    self.ser.parity, self.ser.stopbits))
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "Cannot open this port")
        if self.ser.isOpen():
            self.receive_timer.start(100)
            print("{0} opened".format(self.ser.port))
            self.ui_serial.btnSerialOpen.setEnabled(False)
            self.ui_serial.btnSerialCLose.setEnabled(True)
        pass

    def close_serial_port(self):
        if self.ser.is_open:
            try:
                self.receive_timer.stop()
                self.ser.close()
                self.ui_serial.btnSerialOpen.setEnabled(True)
                self.ui_serial.btnSerialCLose.setEnabled(False)
                print("{0} closed".format(self.ser.port))
            except:
                pass

    def send_data(self):
        if self.ser.is_open:
            input_s = self.ui_serial.pteSerialPortInput.toPlainText()
            if input_s != '':
                if self.ui_serial.cbSerialPortSendHex.isChecked():
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, "Wrong Data", "Please input Hex Number")
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    input_s = (input_s + "\n").encode('utf-8')
                num = self.ser.write(input_s)
                self.data_bytes_sent += num
                self.ui_serial.leSerialPortDataBytesSent.setText(str(self.data_bytes_sent))

    def receive_data(self):
        if not self.ser.is_open:
            return
        try:
            num = self.ser.in_waiting
        except:
            self.ser.close()
            return
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            if self.ui_serial.cbSerialPortReceiveHex.isChecked():
                out_s = ''
                for i in range(len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.ui_serial.pteSerialPortReceive.insertPlainText(out_s)
            else:
                self.ui_serial.pteSerialPortReceive.insertPlainText(data.decode('utf-8'))  # unicode
            text_cursor = self.ui_serial.pteSerialPortReceive.textCursor()
            text_cursor.movePosition(QTextCursor.EndOfLine)
            self.ui_serial.pteSerialPortReceive.setTextCursor(text_cursor)
            self.data_bytes_received += num
            self.ui_serial.leSerialPortDataBytesReceived.setText(str(self.data_bytes_received))
        else:
            pass

    def clear_send_data(self):
        self.ui_serial.pteSerialPortInput.setPlainText("")
        self.data_bytes_sent = 0
        self.ui_serial.leSerialPortDataBytesSent.setText(str(self.data_bytes_sent))

    def clear_receive_data(self):
        self.ui_serial.pteSerialPortReceive.setPlainText("")
        self.data_bytes_received = 0
        self.ui_serial.leSerialPortDataBytesReceived.setText(str(self.data_bytes_received))

    def update_figure(self):
        t = np.linspace(0, 10, 101)
        self.axes_dynamic.cla()
        self.axes_dynamic.plot(t, np.sin(t+time.time()), 'r', linewidth=2.0)
        self.static_canvas.draw()


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Run the main Qt loop
    app.exec_()
