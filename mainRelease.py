"""
!/usr/bin/python
-*- coding: UTF-8 -*-

* Creator: Aldrich
* Create time: 2022/8/6
* Update time: 2022/8/8
* This is a tools to convert video from frame to frame image, you can also choose to add quality enhancements to export.
* This tool follows the 'Mozilla Public License Version 2.0' open source license, thanks for your cooperation.
"""

import os
import sys
import time

import numpy as np
import cv2
import tkinter
import logging
import windnd
import datetime
import threading
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno
from concurrent.futures import ThreadPoolExecutor


def getVideoInfo(source_name):
    global numFrames, optimize, tks, decodeFramesFirst, workDir
    return_value = 0
    try:
        cap = cv2.VideoCapture(source_name)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        numFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if askyesno("是否导出", "文件：{} \n宽度：{} \n高度：{} \n视频帧率：{} \n视频帧数：{}\n\n确定导出请单击“是”".format(msg, width, height, fps,
                                                                                             numFrames)):
            if askyesno("是否优化帧", '这会使导出的帧图像优化，但会增加导出速度'):
                optimize = 1
            else:
                optimize = 0
            tk.destroy()

            workDir = os.path.basename(msg)[:-4]

            logThread = threading.Thread(target=loggerWindow)
            logThread.start()
            decodeFramesFirst = int(numFrames / 2)

            tks = tkinter.Tk()
            tks.title('VTP (Video To frame Picture) 工作中')
            tks.geometry('430x120')
            tks.resizable(None, None)
            label = tkinter.Label(tks, text='\n\n正在导出中……', font=('微软雅黑', 12))
            label.grid(row=0, column=0, sticky=tkinter.W)
            tks.mainloop()
        else:
            pass
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        log1.info("导入错误 {}".format(str(e)))
        print(e)
        return_value = -1
    return return_value


class LoggerBox(tkinter.Text):

    def write(self, message):
        self.insert("end", message)


def loggerWindow():
    global log1, root
    root = tkinter.Tk()
    root.title("VTP 工作日志窗口")
    root.geometry("800x740")
    streamHandlerBox = LoggerBox(root, width=260, height=50)
    streamHandlerBox.place(x=1, y=1)
    log1 = logging.getLogger('log1')
    log1.setLevel(logging.INFO)
    handler = logging.StreamHandler(streamHandlerBox)
    log1.addHandler(handler)
    os.mkdir(workDir)
    log1.info(f'创建工作路径 {workDir}')
    os.chdir(workDir)
    log1.info(f'切换工作路径 {workDir}')
    if int(numFrames / 20) > 1:
        pool = ThreadPoolExecutor(max_workers=12)
        piece = int(numFrames / 12)

        data = (1, piece - 1)
        data1 = (piece - 1, piece * 2 - 1)
        data2 = (piece * 2, piece * 3 - 1)
        data3 = (piece * 3, piece * 4 - 1)
        data4 = (piece * 4, piece * 5 - 1)
        data5 = (piece * 5, piece * 6 - 1)
        data6 = (piece * 6, piece * 7 - 1)
        data7 = (piece * 7, piece * 8 - 1)
        data8 = (piece * 8, piece * 9 - 1)
        data9 = (piece * 9, piece * 10 - 1)
        data10 = (piece * 10, piece * 11 - 1)
        data11 = (piece * 11, piece * 12)

        pool.submit(uploadFrame, *data)
        pool.submit(uploadFrame, *data1)
        pool.submit(uploadFrame, *data2)
        pool.submit(uploadFrame, *data3)
        pool.submit(uploadFrame, *data4)
        pool.submit(uploadFrame, *data5)
        pool.submit(uploadFrame, *data6)
        pool.submit(uploadFrame, *data7)
        pool.submit(uploadFrame, *data8)
        pool.submit(uploadFrame, *data9)
        pool.submit(uploadFrame, *data10)
        pool.submit(uploadFrame, *data11)

    else:
        uploadFrame(0, numFrames)

    root.mainloop()


def uploadFrame(FrameOne, FrameTwo):
    captureFile = cv2.VideoCapture(f'{msg}')
    print(captureFile.isOpened())
    while True:
        ret, img = captureFile.read()
        if not ret:
            break
        if optimize == 1:
            img = cv2.bilateralFilter(img, 12, 17, 25)
            img = np.uint8(np.clip((0.982 * img + 9.45), 0, 255))
            cv2.waitKey(0)
        else:
            pass

        now = datetime.datetime.now()
        cv2.imwrite('%s.jpg' % ('pic_' + str(FrameOne)), img)  # 写出视频图片.jpg格式
        log1.info(f"{now} 已导出 {FrameOne} 帧，共 {numFrames} 帧")
        if FrameOne == int(FrameTwo):
            showinfo('完成', '当前线程已完成，请等待其他线程')
            sys.exit(0)
        FrameOne = FrameOne + 1


def getVideoFile():
    global tk

    def dropFile(files):
        global msg
        msg = '\n'.join((item.decode('gbk') for item in files))
        ask = askyesno('提示', f'确认文件为  {msg}  吗？')
        if ask:
            if msg.endswith(('mp4', 'avi', 'flv', 'f4v', 'webm', 'm4v', 'mov', 'wmv', 'mkv')):
                getVideoInfo(msg)
            else:
                showerror('错误', '不支持此格式\n目前支持的视频格式为：mp4、avi、flv、f4v、webm、m4v、mov、wmv、mkv')
        else:
            pass

    tk = tkinter.Tk()
    tk.title('VTP (Video To frame Picture)')
    tk.geometry('530x100')
    tk.resizable(None, None)
    windnd.hook_dropfiles(tk, func=dropFile)
    label = tkinter.Label(tk, text='\n请将视频拖入此处\n(支持的格式：mp4、avi、flv、f4v、webm、m4v、mov、wmv、mkv）', font=('微软雅黑', 12))
    label.grid(row=0, column=0, sticky=tkinter.W)
    tk.mainloop()


if __name__ == "__main__":
    getVideoFile()
