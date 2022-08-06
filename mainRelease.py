"""
!/usr/bin/python
-*- coding: UTF-8 -*-

* Creator: Aldrich
* Create time: 2022/8/6
* This is a tools to convert video from frame to frame image, you can also choose to add quality enhancements to export.
* This tool follows the 'Mozilla Public License Version 2.0' open source license, thanks for your cooperation.
"""


import os
import numpy as np
import cv2
import tkinter
import windnd
import threading
from tkinter.messagebox import showinfo, showerror, askyesno


def getVedioInfo(source_name):
    global numFrames, optimize, tks
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

            tks = tkinter.Tk()
            tks.title('VTP (Vedio To frame Picture) 工作中')
            tks.geometry('430x120')
            tks.resizable(None, None)
            uploadThread = threading.Thread(target=uploadFrame)
            uploadThread.start()
            label = tkinter.Label(tks, text='\n\n正在导出中……', font=('微软雅黑', 12))
            label.grid(row=0, column=0, sticky=tkinter.W)
            tks.mainloop()
        else:
            pass
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        showerror("文件:{} 导入错误 {}\n".format(source_name, str(e)))
        print(e)
        return_value = -1
    return return_value


def uploadFrame():
    capture = cv2.VideoCapture(f'{msg}')
    print(capture.isOpened())
    num = 0
    os.mkdir(f'{os.path.basename(msg)[:-4]}')
    os.chdir(f'{os.path.basename(msg)[:-4]}')
    while True:
        ret, img = capture.read()
        if not ret:
            break
        if optimize == 1:
            img = cv2.bilateralFilter(img, 12, 17, 25)
            img = np.uint8(np.clip((0.982 * img + 9.45), 0, 255))
            cv2.waitKey(0)
        else:
            pass
        cv2.imwrite('%s.jpg' % ('pic_' + str(num)), img)  # 写出视频图片.jpg格式
        if num == int(numFrames):
            break
        num = num + 1
    showinfo('完成', '转换完成')
    tks.destroy()
    os.system(f'explorer.exe {os.path.basename(msg)[:-4]}')


def getVideoFile():
    global tk

    def dropFile(files):
        global msg
        msg = '\n'.join((item.decode('gbk') for item in files))
        ask = askyesno('提示', f'确认文件为  {msg}  吗？')
        if ask:
            if msg.endswith(('mp4', 'avi', 'flv', 'f4v', 'webm', 'm4v', 'mov', 'wmv')):
                getVedioInfo(msg)
            else:
                showerror('错误', '不支持此格式\n目前支持的视频格式为：mp4、avi、flv、f4v、webm、m4v、mov、wmv')
        else:
            pass

    tk = tkinter.Tk()
    tk.title('VTP (Vedio To frame Picture)')
    tk.geometry('475x120')
    tk.resizable(None, None)
    windnd.hook_dropfiles(tk, func=dropFile)
    label = tkinter.Label(tk, text='\n请将视频拖入此处\n(支持的格式：mp4、avi、flv、f4v、webm、m4v、mov、wmv）', font=('微软雅黑', 12))
    label.grid(row=0, column=0, sticky=tkinter.W)
    tk.mainloop()


if __name__ == "__main__":
    getVideoFile()
