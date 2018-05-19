# -*- coding:utf-8 -*-
import os
from Tkinter import *
from tkMessageBox import *
import cv2
import numpy as np
import PIL
from doFunction import imageProcessing
from DBView import *
import ttk
import threading
import imutils
import ConfigParser
import sys
import math
import time
import tkFileDialog
from ScrolledText import ScrolledText

# ----------------------------------------- 主页面 -----------------------------------------
class InputFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.message_info = None
        self.run_image = None
        self.stop_image = None
        self.canvas_image = None
        self.testimagepath = None
        self.open_image = None
        self.mark_image = None
        self.test_image = None
        self.timenum = None
        self.index2 = 0
        self.listoftestimage = ['LearningTemplate2.png', 'Template2.png', 'Template3.png', 'Template4.png', 'Template1.png', 'CostumeTest1.png', 'CostumeTest2.png', 'CostumeTest4.png']
        self.targetimage = os.getcwd()+"/img/circular.jpg"
        self.createPage()

    # 获取图片
    def createPage(self):

        # 此方法用来保存PhotoImage对象即可
        imgDict = {}
        def getImgWidget(filePath):
            if os.path.exists(filePath) and os.path.isfile(filePath):
                if filePath in imgDict and imgDict[filePath]:
                    return imgDict[filePath]
                img = PIL.Image.open(filePath)
                # print(img.size)
                img = PIL.ImageTk.PhotoImage(img)
                imgDict[filePath] = img
                return img
            return None

        # 此方法用来输出消息和开发时测试
        def sendmessage(event):
            if self.testimagepath == None or self.testimagepath == '':
                showinfo(title='步骤错误', message='请先选择测试图片')
            else:
                result = imageProcessing().patterMatching(self.targetimage, self.testimagepath)
                # 测试内容
                msgcontent = '测试完成，结果如下：\n'
                for i in range(0, len(result[1])):
                    temp = "第" + bytes(i) + "号图的匹配度：" + bytes(result[1][i]) + '\n'
                    msgcontent = msgcontent + temp
                msgcontent = msgcontent + '测试为圆概率比较大的为：\n'
                for i in range(0, len(result[0])):
                    temp = "第" + bytes(result[0][i]) + '号图\n'
                    msgcontent = msgcontent + temp
                text_msglist.insert(END, msgcontent)

        # 此方法用来打开测试图片
        def openPhoto(event):
            self.testimagepath = tkFileDialog.askopenfilename(initialdir='D:\workspace\Python\machine\image')
            self.canvas_image.create_image(0, 163, anchor=W, image=getImgWidget(self.testimagepath), tags="mark")

        def markPhoto(event):
            if self.testimagepath == None or self.testimagepath == '':
                showinfo(title='步骤错误', message='请先选择测试图片')
            else:
                imageProcessing().imageMark(self.testimagepath)
                self.canvas_image.delete("mark")
                self.canvas_image.create_image(0, 163, anchor=W, image=getImgWidget(os.getcwd()+'\img\Mark.jpg'),
                                               tags="mark")

        def changepic():
            index = 0
            # 读取配置文件
            cf = ConfigParser.ConfigParser()
            cf.read("setting.ini")

            org_x = cf.get("set", "org_x")
            org_y = cf.get("set", "org_y")
            or_width = cf.get("set", "or_width")
            or_height = cf.get("set", "or_height")
            self.timenum = float(cf.get("set", "operationtimeinterval"))
            while index < 8:
                self.canvas_image.delete('mark2')
                self.canvas_image.create_image(0, 163, anchor=W,
                                               image=getImgWidget(os.getcwd() + '\img\\' + self.listoftestimage[index]),
                                               tags="mark1")

                time.sleep(self.timenum)
                # 获取轮廓操作,获取相关信息
                messages1 = imageProcessing().reduction_of_coordinates(os.getcwd() + '\img\\' + self.listoftestimage[index], float(org_x), float(org_y), float(or_width), float(or_height), self.index2)
                text_msglist.insert(END, '第%d号图寻找到的坐标是：x=%d,y=%d\n'%(index+1, messages1[0], messages1[1]))

                self.canvas_image.delete('mark1')
                self.canvas_image.create_image(0, 163, anchor=W,
                                               image=getImgWidget(os.getcwd()+'\img\cash\RmustResult'+str(self.index2)+'.jpg'),
                                               tags="mark2")
                '''
                time.sleep(1)
                # 获取极点操作
                messages2 = imageProcessing().markMost(os.getcwd() + '\img\\' + self.listoftestimage[index], index)
                self.canvas_image.create_image(0, 163, anchor=W,
                                               image=getImgWidget(os.getcwd()+'\img\RmustResult'+str(index)+'.jpg'),
                                               tags="mark")
                text_msglist.insert(END, '第%d号图的极点是：\n' % (index + 1))
                for i in range(0, 4):
                    text_msglist.insert(END, 'x=%d,y=%d\n' % (messages2[i][0], messages2[i][1]))
                '''
                time.sleep(self.timenum)
                self.index2 = self.index2 + 1
                index = index + 1
            print 'run end'

        def runtest(event):
            th = threading.Thread(target=changepic, args=())
            th.setDaemon(True)  # 守护线程
            th.start()

            # 创建几个frame作为容器
        frame_left_top = Frame(self, width=585, height=350, bg='white')
        frame_left_center = Frame(self, width=585, height=180, bg='white')
        frame_left_bottom = Frame(self, width=585, height=20, bg='white')
        frame_right = Frame(self, width=200, height=574, bg='white')

        frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        frame_left_center.grid(row=1, column=0, padx=2, pady=5)
        frame_left_bottom.grid(row=2, column=0, padx=2, pady=5)
        frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)

        frame_left_top.grid_propagate(0)
        frame_left_center.grid_propagate(0)
        frame_left_bottom.grid_propagate(0)
        frame_right.grid_propagate(0)

        # 创建需要的几个元素
        px = 20
        py = 10
        Label(frame_left_center, bg='white').grid(row=0, column=0, padx=20, pady=py)
        # 运行测试按钮
        self.run_image = PhotoImage(file=os.getcwd()+"/img/run_icon.gif")
        run_button = Canvas(frame_left_center, height=70, width=70, bg='white', highlightthickness=0)
        run_button.grid(row=0, column=1, padx=px, pady=py)
        run_button.create_image(35, 35, image=self.run_image)
        run_button.bind('<ButtonPress-1>', runtest)

        self.stop_image = PhotoImage(file=os.getcwd()+"/img/stop_icon.gif")
        stop_button = Canvas(frame_left_center, height=70, width=70, bg='white', highlightthickness=0)
        stop_button.grid(row=0, column=2, padx=px, pady=py)
        stop_button.create_image(35, 35, image=self.stop_image)

        Label(frame_left_center, bg='white').grid(row=0, column=3, padx=25, pady=py)
        text_frame = LabelFrame(frame_left_center, width=200, height=150, text='运行测试', font=("宋体", 10), bg='white')
        text_frame.grid(row=0, column=4, padx=px, pady=py)
        text_frame.grid_propagate(0)

        # 控制台信息输出框
        self.message_info =PhotoImage(file=os.getcwd()+"/img/message_info.gif")
        Label(frame_right, image=self.message_info).grid(row=0, column=0, stick=W)
        text_msglist = ScrolledText(frame_right, height=42, width=25)
        text_msglist.grid(row=1, column=0, padx=2)

        # 开始进行测试
        self.test_image = PhotoImage(file=os.getcwd()+"/img/test_pic.gif")
        button_sendmsg = Canvas(text_frame, height=30, width=100, bg='white', highlightthickness=0)
        button_sendmsg.grid(row=2, column=0, padx=55, pady=6)
        button_sendmsg.create_image(50, 15, image=self.test_image)
        button_sendmsg.bind('<ButtonPress-1>', sendmessage)

        # 打开测试图片
        self.open_image = PhotoImage(file=os.getcwd()+"/img/open_pic.gif")
        button_openPhoto = Canvas(text_frame,  height=30, width=100, bg='white', highlightthickness=0)
        button_openPhoto.grid(row=0, column=0, padx=55, pady=6)
        button_openPhoto.create_image(50, 15, image=self.open_image)
        button_openPhoto.bind('<ButtonPress-1>', openPhoto)

        # 标记测试图片
        self.mark_image = PhotoImage(file=os.getcwd()+"/img/mark_pic.gif")
        button_mark = Canvas(text_frame,  height=30, width=100, bg='white', highlightthickness=0)
        button_mark.grid(row=1, column=0, padx=55, pady=6)
        button_mark.create_image(50, 15, image=self.mark_image)
        button_mark.bind('<ButtonPress-1>', markPhoto)

        # 背景框图片
        self.canvas_image = Canvas(frame_left_top, width=560, height=325)
        self.canvas_image.grid(padx=10, pady=10)

# ----------------------------------------- 系统设置界面 -----------------------------------------
class QueryFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.picURL = StringVar()
        self.createPage()

    def createPage(self):
        def init():
            # 编码问题解决代码
            reload(sys)
            sys.setdefaultencoding('utf8')

            # 读取配置文件
            cf = ConfigParser.ConfigParser()
            cf.read("setting.ini")

            temp = cf.get("set", "matchpattern")
            if temp == '图形匹配':
                match_pattern_type.current(0)
            else:
                match_pattern_type.current(1)
            temp = cf.get("set", "targetshape")
            if temp == '圆形':
                shap_type.current(0)
            elif temp == '三角形':
                shap_type.current(1)
            elif temp == '正方形':
                shap_type.current(2)
            else:
                shap_type.current(3)
            temp = cf.get("set", "targetcolor")
            if temp == '红色':
                coler_type.current(0)
            elif temp == '蓝色':
                coler_type.current(1)
            elif temp == '黄色':
                coler_type.current(2)
            else:
                coler_type.current(3)
            slm.set(float(cf.get("set", "matchingmsensitivity")))
            stime.set(float(cf.get("set", "operationtimeinterval")))

            temp = cf.get("set", "imagereadingmode")
            if temp == '以彩色模式读取':
                photo_read_type.current(0)
            elif temp == '以灰度模式读取':
                photo_read_type.current(1)
            else:
                photo_read_type.current(2)
            temp = cf.get("set", "contourretrievalmode")
            if temp == '建立一个等级树结构的轮廓':
                contour_retrieval.current(0)
            elif temp == '只检测外轮廓':
                contour_retrieval.current(1)
            elif temp == '检测的轮廓不建立等级关系':
                contour_retrieval.current(2)
            else:
                contour_retrieval.current(3)
            temp = cf.get("set", "contourapproximationmethod")
            if temp == '存储所有的轮廓点':
                contour_approximate.current(0)
            else:
                contour_approximate.current(1)
            temp = cf.get("set", "valueprocessingmethod")
            if temp == 'BINARY_INV':
                thresh.current(0)
            elif temp ==  'BINARY':
                thresh.current(1)
            elif temp == 'TRUNC':
                thresh.current(2)
            elif temp == 'TOZERO':
                thresh.current(3)
            else:
                thresh.current(4)

            chuli.set(cf.getint("set", "newvalvevalueaftertreatment"))
            fenlei.set(cf.getint("set", "thethresholdoftheclassification"))

            temp = cf.get("set", "tagcolor")
            if temp == '蓝色':
                colselete.current(0)
            elif temp == '红色':
                colselete.current(1)
            else:
                colselete.current(2)

            s1.set(cf.getint("set", "thethicknessofthetag"))

            self.picURL.set(cf.get("set", "customtargetimageaddress"))
            coloRGB.set(cf.get("set", "customcolorrgb"))

        def settingsave():
            # 编码问题解决代码
            reload(sys)
            sys.setdefaultencoding('utf8')

            # 读取配置文件
            cf = ConfigParser.ConfigParser()
            cf.read("setting.ini")

            cf.set("set", "matchpattern", match_pattern_type.get())
            cf.set("set", "targetshape", shap_type.get())
            cf.set("set", "targetcolor", coler_type.get())
            cf.set("set", "matchingmsensitivity", slm.get())
            cf.set("set", "operationtimeinterval", stime.get())

            cf.set("set", "imagereadingmode", photo_read_type.get())
            cf.set("set", "contourretrievalmode", contour_retrieval.get())
            cf.set("set", "contourapproximationmethod", contour_approximate.get())
            cf.set("set", "valueprocessingmethod", thresh.get())
            cf.set("set", "newvalvevalueaftertreatment", chuli.get())
            cf.set("set", "thethresholdoftheclassification", fenlei.get())

            cf.set("set", "customtargetimageaddress", self.picURL.get())
            cf.set("set", "customcolorrgb", coloRGB.get())

            cf.set("set", "tagcolor", colselete.get())
            cf.set("set", "thethicknessofthetag", s1.get())

            # 写入配置文件
            with open("setting.ini", "w+") as f:
                cf.write(f)

            showinfo(title='提示', message='保存成功！')

        def settingdefault():
            match_pattern_type.current(0)
            shap_type.current(0)
            coler_type.current(0)
            slm.set(0.5)
            stime.set(3)
            photo_read_type.current(0)
            contour_retrieval.current(0)
            contour_approximate.current(0)
            thresh.current(0)
            chuli.set(127)
            fenlei.set(255)

            colselete.current(0)
            s1.set(2)

        def openfile():
            filename = tkFileDialog.askopenfilename(initialdir='C:/')
            self.picURL.set(filename)

        px = 5
        py = 8
        # ------------------- 匹配模式设置 -------------------
        Label(self, text='系统设置', width=30, font=("宋体", 18, "bold")).grid(row=0, column=0, columnspan=8, padx=0, pady=10)
        pi_frame = LabelFrame(self, width=350, height=310, text='匹配模式设置', font=("宋体", 14))
        pi_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        pi_frame.grid_propagate(0)
        Label(pi_frame, text='匹配模式').grid(row=0, column=0, columnspan=2, padx=px, pady=py)
        match_pattern_type = ttk.Combobox(pi_frame, values=('图形匹配', '颜色匹配'), state="readonly")
        match_pattern_type.current(0)
        match_pattern_type.grid(row=0, column=2, columnspan=2, padx=px, pady=py)
        Label(pi_frame, text='目标形状').grid(row=1, column=0, columnspan=2, padx=px, pady=py)
        Label(pi_frame, text='目标颜色').grid(row=2, column=0, columnspan=2, padx=px, pady=py)
        shap_type = ttk.Combobox(pi_frame, values=('圆形', '三角形', '正方形', '自定义'), state="readonly")
        shap_type.grid(row=1, column=2, columnspan=2, padx=px, pady=py)
        shap_type.current(0)
        coler_type = ttk.Combobox(pi_frame, values=('红色', '蓝色', '黄色', '自定义'), state="readonly")
        coler_type.grid(row=2, column=2, columnspan=2, padx=px, pady=py)
        coler_type.current(1)
        Label(pi_frame, text='匹配灵敏度', width=20).grid(row=3, column=0, columnspan=2, padx=px, pady=py)
        Label(pi_frame, text='运算时间间隔', width=20).grid(row=4, column=0, columnspan=2, padx=px, pady=py)
        slm = Scale(pi_frame, length=150, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
        slm.grid(row=3, column=2, columnspan=2, padx=px, pady=py)
        slm.set(0.5)
        stime = Scale(pi_frame, length=150, from_=0, to=5, resolution=0.1, orient=HORIZONTAL)
        stime.grid(row=4, column=2, columnspan=2, padx=px, pady=py)
        stime.set(3)

        # ------------------- 图像识别设置 -------------------
        shi_frame = LabelFrame(self, width=350, height=310, text='图像识别设置', font=("宋体", 14))
        shi_frame.grid(row=1, column=4, columnspan=4, padx=10, pady=10)
        shi_frame.grid_propagate(0)

        Label(shi_frame, text='图片读取模式').grid(row=0, column=0, padx=px, pady=py)
        photo_read_type = ttk.Combobox(shi_frame, values=('以彩色模式读取', '以灰度模式读取','包括alpha通道读取'), state="readonly")
        photo_read_type.grid(row=0, column=1, padx=px, pady=py)
        photo_read_type.current(0)

        Label(shi_frame, text='轮廓检索模式').grid(row=1, column=0, padx=px, pady=py)
        contour_retrieval = ttk.Combobox(shi_frame, values=('建立一个等级树结构的轮廓', '只检测外轮廓', '检测的轮廓不建立等级关系', '建立两个等级的轮廓'), state="readonly")
        contour_retrieval.grid(row=1, column=1, padx=px, pady=py)
        contour_retrieval.current(0)

        Label(shi_frame, text='轮廓近似方法', width=20).grid(row=2, column=0, padx=px, pady=py)
        contour_approximate = ttk.Combobox(shi_frame, values=('存储所有的轮廓点', '只保留终点坐标的轮廓点'), state="readonly")
        contour_approximate.grid(row=2, column=1, padx=px, pady=py)
        contour_approximate.current(0)

        Label(shi_frame, text='阈值处理方法', width=20).grid(row=3, column=0, padx=px, pady=py)
        thresh = ttk.Combobox(shi_frame, values=('BINARY_INV', 'BINARY', 'TRUNC', 'TOZERO', 'TOZERO_INV'), state="readonly")
        thresh.grid(row=3, column=1, padx=px, pady=py)
        thresh.current(0)

        Label(shi_frame, text='处理后的新阈值', width=20).grid(row=4, column=0, padx=px, pady=py)
        chuli = Scale(shi_frame, length=150, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        chuli.grid(row=4, column=1, columnspan=2, padx=px, pady=py)
        chuli.set(127)

        Label(shi_frame, text='进行分类的阈值', width=20).grid(row=5, column=0, padx=px, pady=py)
        fenlei = Scale(shi_frame, length=150, from_=0, to=255, resolution=1, orient=HORIZONTAL)
        fenlei.grid(row=5, column=1, columnspan=2, padx=px, pady=py)
        fenlei.set(255)

        # ------------------- 自定义设置 -------------------
        zi_frame = LabelFrame(self, width=350, height=120, text='自定义设置', font=("宋体", 14))
        zi_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        zi_frame.grid_propagate(0)
        Label(zi_frame, text='自定义目标图像地址').grid(row=0, column=0, padx=px, pady=py)
        Entry(zi_frame, textvariable=self.picURL).grid(row=0, column=1, padx=px, pady=py)
        Button(zi_frame, text='打开',command=openfile).grid(row=0, column=2, padx=px, pady=py)
        Label(zi_frame, text='自定义颜色RGB', width=15).grid(row=1, column=0, padx=px, pady=py)
        coloRGB = StringVar()
        Entry(zi_frame, textvariable=coloRGB).grid(row=1, column=1, padx=px, pady=py)

        # ------------------- 绘图设置 -------------------
        hui_frame = LabelFrame(self, width=350, height=120, text='绘图设置', font=("宋体", 14))
        hui_frame.grid(row=2, column=4, columnspan=4, padx=10, pady=10)
        hui_frame.grid_propagate(0)
        Label(hui_frame, text='标记颜色').grid(row=0, column=0, padx=px, pady=py)
        colselete = ttk.Combobox(hui_frame, values=('蓝色', '红色', '黄色'), state="readonly")
        colselete.current(0)
        colselete.grid(row=0, column=1, padx=px, pady=py)
        Label(hui_frame, text='标记厚度', width=20).grid(row=1, column=0, padx=px, pady=py)
        # 返回值
        defv = StringVar()
        s1 = Scale(hui_frame, from_=0, to=10, length=150, resolution=1, orient=HORIZONTAL, variable=defv)
        s1.grid(row=1, column=1, padx=px, pady=py)
        s1.set(2)

        Button(self, text='默认', width=10, command=settingdefault).grid(row=3, column=6, padx=2, pady=10, sticky=E)
        Button(self, text='保存', width=10, command=settingsave).grid(row=3, column=7, padx=2, pady=10, sticky=W)

        init()

# ----------------------------------------- 摄像头设置界面 -----------------------------------------
class CountFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.photo_Canvas = None
        self.image = None
        self.cam_type = None
        self.cam_set = None
        self.stopEvent = threading.Event()
        self.onCreate = threading.Event()
        self.thread = None
        self.createPage()
        self.initconf()

    def initconf(self):
        cf = ConfigParser.ConfigParser()
        cf.read("setting.ini")

        temp = cf.get("set", "cameratype")
        if temp == '笔记本摄像头':
            self.cam_type.current(0)
            self.cam_set = 0
        else:
            self.cam_type.current(1)
            self.cam_set = 1

    def videoLoop(self):
        try:
            cap = cv2.VideoCapture(self.cam_set)
            while not self.stopEvent.is_set():
                ret, self.frame = cap.read()
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = PIL.Image.fromarray(image)
                self.image = PIL.ImageTk.PhotoImage(image)
                self.photo_Canvas.create_image(0, 120, anchor=W, image=self.image, tags="mark")

            '''
            self.onCreate.set()
            cap = cv2.VideoCapture(self.cam_set)
            flag = 1
            while True:
                if not self.stopEvent.is_set():
                    if flag == 0:
                        cap = cv2.VideoCapture(self.cam_set)
                        flag = 1
                    ret, self.frame = cap.read()
                    print cap
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    image = PIL.Image.fromarray(image)
                    self.image = PIL.ImageTk.PhotoImage(image)
                    self.photo_Canvas.create_image(0, 120, anchor=W, image=self.image, tags="mark")
                elif flag == 1:
                    cap.release()
                    flag = 0
            '''
        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def cameratest(self):
        '''
        if self.onCreate.is_set():
            self.stopEvent.clear()
        else:
            self.thread.start()
        '''
        self.stopEvent.clear()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.setDaemon(True)
        self.thread.start()
    def takephoto(self):
        self.stopEvent.set()
        time.sleep(0.5)
        cap = cv2.VideoCapture(self.cam_set)
        ret, self.frame = cap.read()
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        self.image = PIL.ImageTk.PhotoImage(image)
        self.photo_Canvas.create_image(0, 175, anchor=W, image=self.image, tags="mark")
        cap.release()


    def saveconf(self, event):
        cf = ConfigParser.ConfigParser()
        cf.read("setting.ini")

        cf.set("set", "cameratype", self.cam_type.get())
        with open("setting.ini", "w+") as f:
            cf.write(f)

        temp = self.cam_type.get()
        if temp == '笔记本摄像头':
            self.cam_set = 0
        else:
            self.cam_set = 1

    def createPage(self):

        px = 15
        py = 5
        Label(self, text='摄像头设置', width=30, font=("宋体", 18, "bold")).grid(row=0, column=0, columnspan=4, padx=0,
                                                                          pady=40)
        self.photo_Canvas = Canvas(self, bg='white', width=460, height=350)
        self.photo_Canvas.grid(row=1, column=0, columnspan=3, rowspan=3, padx=px, pady=py)
        Button(self, text='摄像头视频模式测试', width=30, command=self.cameratest).grid(row=1, column=3, padx=px, pady=py)
        Button(self, text='拍照测试测试', width=30, command=self.takephoto).grid(row=2, column=3, padx=px, pady=py)
        self.cam_type = ttk.Combobox(self, values=('笔记本摄像头', '其他摄像头'), state="readonly", width=30)
        self.cam_type.current(0)
        self.cam_type.grid(row=3, column=3, padx=px, pady=py)
        self.cam_type.bind('<<ComboboxSelected>>', self.saveconf)

# ----------------------------------------- 坐标校验设置 -----------------------------------------
class CheckFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.testimagepath = None
        self.physicalheight = StringVar()
        self.physicalwidth = StringVar()
        self.physicalwidth.set(5)
        self.pixelheight = StringVar()
        self.pixelwidth = StringVar()
        self.restext = None
        self.photo_lable = None
        self.createPage()
        self.count = 0

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def createPage(self):
        # 此方法用来保存PhotoImage对象即可
        imgDict = {}
        def getImgWidget(filePath):
            if os.path.exists(filePath) and os.path.isfile(filePath):
                if filePath in imgDict and imgDict[filePath]:
                    return imgDict[filePath]
                img = PIL.Image.open(filePath)
                # print(img.size)
                img = PIL.ImageTk.PhotoImage(img)
                imgDict[filePath] = img
                return img
            return None

        def takecamera():
            pass

        def tacktest():
            self.testimagepath = tkFileDialog.askopenfilename(initialdir='D:\workspace\Python\machine\image')
            self.photo_lable.create_image(0, 150, anchor=W, image=getImgWidget(self.testimagepath))

        def autoget():
            if self.testimagepath == None or self.testimagepath == '':
                showinfo("步骤错误", "请输入测试图片")
            else:
                img = cv2.imread(self.testimagepath)
                size = img.shape

                self.physicalheight.set(imageProcessing().distancecheck(self.testimagepath))

                self.pixelheight.set(size[0])
                self.pixelwidth.set(size[1])

        def savedata():
                pass

        px = 15
        py = 5
        Label(self, text='坐标校验设置', width=30, font=("宋体", 18, "bold")).grid(row=0, column=0, columnspan=4, padx=0, pady=20)
        self.photo_lable = Canvas(self, bg='white', width=500, height=375)
        self.photo_lable.grid(row=1, column=0, columnspan=2, rowspan=3, padx=px, pady=py)
        self.photo_lable.bind('<ButtonPress-1>', self.action)

        jiagong_frame = LabelFrame(self, width=230, height=100, text='标尺设置', font=("宋体", 10))
        jiagong_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10)
        jiagong_frame.grid_propagate(0)
        Label(jiagong_frame, text='像素距离').grid(row=0, column=0, padx=5, pady=8)
        Entry(jiagong_frame, textvariable=self.physicalheight).grid(row=0, column=1, padx=5, pady=8)
        Label(jiagong_frame, text='物理距离').grid(row=1, column=0, padx=5, pady=8)
        Entry(jiagong_frame, textvariable=self.physicalwidth).grid(row=1, column=1, padx=5, pady=8)

        xiangsu_frame = LabelFrame(self, width=230, height=100, text='图像像素设置', font=("宋体", 10))
        xiangsu_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        xiangsu_frame.grid_propagate(0)
        Label(xiangsu_frame, text='图片高度').grid(row=0, column=0, padx=5, pady=8)
        Entry(xiangsu_frame, textvariable=self.pixelheight).grid(row=0, column=1, padx=5, pady=8)
        Label(xiangsu_frame, text='图片宽度').grid(row=1, column=0, padx=5, pady=8)
        Entry(xiangsu_frame, textvariable=self.pixelwidth).grid(row=1, column=1, padx=5, pady=8)

        shuchu_frame = LabelFrame(self, width=230, height=100, text='坐标转换输出区', font=("宋体", 10))
        shuchu_frame.grid(row=3, column=2, columnspan=2, padx=10, pady=10)
        shuchu_frame.grid_propagate(0)
        self.restext = Text(shuchu_frame, width=25, height=5)

        self.restext.grid(padx=5, pady=5)
        self.restext.insert(END, '坐标换算结果输出,请点击右侧区域选点')

        Button(self, text='输入摄像头画面', command=takecamera).grid(row=4, column=2, padx=5, pady=10)
        Button(self, text='输入测试图片', command=tacktest).grid(row=4, column=3, padx=5, pady=10)

        Button(self, text='自动获取相关数据', command=autoget).grid(row=5, column=2, padx=5, pady=2)
        Button(self, text='保存校准设置', command=savedata).grid(row=5, column=3, padx=5, pady=2)

    def action(self, event):

        def diss(x1, x2, y1, y2):
            return math.sqrt(math.pow(abs(y2 - y1), 2) + math.pow(abs(x2 - x1), 2))

        if self.count == 0:
            self.restext.delete(0.0, END)
            self.photo_lable.delete('line')
            self.x1 = event.x
            self.y1 = event.y
            self.restext.insert(END, "您选的第一个坐标:%d,%d"% (self.x1, self.y1))
            self.count = 1
        else:
            self.x2 = event.x
            self.y2 = event.y
            self.restext.insert(END, "您选的第二个坐标:%d,%d" % (self.x2, self.y2))
            if self.physicalheight.get() == '' or self.physicalwidth.get() == '':
                self.restext.insert(END, "请在上方输入参数" )
            else:
                # 画图
                self.photo_lable.create_line(self.x1, self.y1, self.x2, self.y2, tags='line')
                ans =diss(self.x1, self.x2, self.y1, self.y2) / (float(self.physicalheight.get())/float(self.physicalwidth.get()))
                self.restext.insert(END, "换算出的物理距离为:%d" % (ans,))

            self.count = 0

# ----------------------------------------- 机器学习设置 -----------------------------------------
class LearnFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.view_canvas = None
        self.learn_pic = None
        self.point_inf = None
        self.info_lable = None
        self.createPage()

    def point(self, event):
        # print event.x
        # print event.y
        self.info_lable['text'] = '当前选择的坐标：x=%d y=%d'%(event.x, event.y)
        self.view_canvas.delete("oval")
        # 做标记
        x1, y1 = (event.x - 5), (event.y - 5)
        x2, y2 = (event.x + 5), (event.y + 5)
        self.view_canvas.create_oval(x1, y1, x2, y2, fill="red", tags="oval")
        self.point_inf = imageProcessing().boundingRectangle(os.getcwd()+"/img/LearningTemplate.png", event.x, event.y)
        print self.point_inf
        #imageProcessing().reduction_of_coordinates(os.getcwd()+"/img/LearningTemplate.png", self.point_inf[0], self.point_inf[1], self.point_inf[2], self.point_inf[3])

    def clearpoint(self):
        self.view_canvas.delete("oval")

    def save_point(self):

        if self.point_inf == None:
            showinfo(title='失败', message='请选择加工点！')
        else:
            # 读取配置文件
            cf = ConfigParser.ConfigParser()
            cf.read("setting.ini")

            cf.set("set", "org_x", self.point_inf[0])
            cf.set("set", "org_y", self.point_inf[1])
            cf.set("set", "or_width", self.point_inf[2])
            cf.set("set", "or_height", self.point_inf[3])

            # 写入配置文件
            with open("setting.ini", "w+") as f:
                cf.write(f)

            showinfo(title='提示', message='加工点信息保存成功！')

    def createPage(self):
        self.learn_pic = PhotoImage(file=os.getcwd()+"/img/LearningTemplate.gif")
        Label(self, text='学习自定义加工点（测试版功能）', width=50, font=("宋体", 14, "bold")).grid(row=0, column=0, columnspan=2, padx=0, pady=20)
        Label(self, text='直接在下方图片内点击，选择你要加工的地方', width=50, font=("宋体", 10,)).grid(row=1, column=0, columnspan=2, padx=0, pady=0)
        self.view_canvas = Canvas(self, height=375, width=500, bg='white', highlightthickness=0)
        self.view_canvas.create_image(250, 187.5, image=self.learn_pic)
        self.view_canvas.grid(row=2, column=0, padx=0, pady=10)
        self.info_lable = Label(self, text='当前未添加任何加工点')
        self.info_lable.grid(row=3, column=0, padx=10, sticky=W)
        Button(self, text='清除加工点', command=self.clearpoint).grid(row=4, column=0, padx=10, pady=10, sticky=W)
        Button(self, text='确认加工点', command=self.save_point).grid(row=4, column=0, padx=10, pady=10, sticky=E)
        self.view_canvas.bind('<ButtonPress-1>', self.point)

# ----------------------------------------- 用户管理界面 -----------------------------------------
class AboutFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        # 创建几个frame作为容器
        frame_left_top = Frame(self, width=585, height=540, bg='white')
        frame_right = Frame(self, width=200, height=568, bg='white')
        frame_left_bottom = Frame(self, width=585, height=20, bg='white')

        frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
        frame_left_bottom.grid(row=2, column=0, padx=2, pady=5)

        frame_left_top.grid_propagate(0)
        frame_right.grid_propagate(0)
        frame_left_bottom.grid_propagate(0)

        self.addpage = addPage(frame_left_top)  # 创建不同Frame
        self.delepage = delePage(frame_left_top)
        self.modpage = modPage(frame_left_top)
        self.selepage = selePage(frame_left_top)
        self.addpage.grid(row=0, column=0)  # 默认显示数据录入界面

        # 创建需要的几个元素
        Label(frame_right, width=20, bg='white').grid(row=0, column=0, padx=20, pady=50)
        button_add = Button(frame_right, width=20, text='增加', command=self.addUser)
        button_dele = Button(frame_right, width=20, text='删除', command=self.deleUser)
        button_mod = Button(frame_right, width=20, text='修改', command=self.modUser)
        button_sele = Button(frame_right, width=20, text='查询', command=self.seleUser)

        # 把元素填充进frame
        button_dele.grid(row=1, column=0, padx=20, pady=20)
        button_add.grid(row=2, column=0, padx=20, pady=20)
        button_mod.grid(row=3, column=0, padx=20, pady=20)
        button_sele.grid(row=4, column=0, padx=20, pady=20)

    def addUser(self):
        self.addpage.grid(row=0, column=0)
        self.delepage.grid_forget()
        self.modpage.grid_forget()
        self.selepage.grid_forget()

    def deleUser(self):
        self.addpage.grid_forget()
        self.delepage.grid(row=0, column=0)
        self.modpage.grid_forget()
        self.selepage.grid_forget()

    def modUser(self):
        self.addpage.grid_forget()
        self.delepage.grid_forget()
        self.modpage.grid(row=0, column=0)
        self.selepage.grid_forget()

    def seleUser(self):
        self.addpage.grid_forget()
        self.delepage.grid_forget()
        self.modpage.grid_forget()
        self.selepage.grid(row=0, column=0)

# ----------------------------------------- 关于 -----------------------------------------
class AboutUsFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='机器视觉柔性加工辅助系统', width=50, font=("宋体", 16, "bold")).grid(row=0, column=0, padx=0, pady=10)
        us_frame = LabelFrame(self, width=700, height=200, text='关于作者', font=("宋体", 10))
        us_frame.grid(row=1, column=0, padx=10, pady=10)
        us_frame.grid_propagate(0)

        author_info = '系统架构：赵鹏辉  数据库设计：张智辉\n\n算法设计：赵鹏辉  软件测试：  黄铮涵\n\n界面设计：赵鹏辉'
        Label(us_frame, text=author_info, justify=LEFT, font=("宋体", 12)).grid(row=0, column=0, padx=180, pady=40)

        help_frame = LabelFrame(self, width=700, height=200, text='使用帮助', font=("宋体", 10))
        help_frame.grid(row=2, column=0, padx=10, pady=10)
        help_frame.grid_propagate(0)

        help_info = '使用前请先调整好配置，图像识别成功率取决于像素高低、选用方法是否恰当、内容干扰度\n\n' \
                    '多少等因素。本系统适应于服装等低精确度生产过程中的柔性加工处理，目前版本的精确度\n\n' \
                    '在厘米级别，后续对图像识别、处理算法进行优化升级后可达毫米级。系统可以与机械设备\n\n' \
                    '连接，辅助传统加工器具自动识别加工内容，提高生产效率。\n\n' \
                    '                                  —— 2018/5/10 机器视觉柔性加工辅助系统 开发组'

        Label(help_frame, text=help_info, justify=LEFT, font=("宋体", 12)).grid(row=0, column=0, padx=20, pady=20)

        Label(self, width=90, text='版本(beta)1.5   Copyright：DreamChaserTeam  2014-2018  designer_email:PHZhao@stu.suda.edu.cn').grid(row=3, column=0, padx=10, pady=50)
