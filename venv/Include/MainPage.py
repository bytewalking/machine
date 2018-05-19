# -*- coding:utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk
from view import *

class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (800, 600))# 设置窗口大小
        self.root.iconbitmap('D:/workspace/Python/machine/venv/Include/img/vision.ico')
        self.root.resizable(False, False)
        self.createPage()

    def createPage(self):
        self.inputPage = InputFrame(self.root)  # 创建不同Frame
        self.queryPage = QueryFrame(self.root)
        self.countPage = CountFrame(self.root)
        self.aboutPage = AboutFrame(self.root)
        self.xycheckPage = CheckFrame(self.root)
        self.learnPage = LearnFrame(self.root)
        self.aboutusPage = AboutUsFrame(self.root)
        self.inputPage.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='主页面', command=self.inputData)
        menubar.add_command(label='系统设置', command=self.queryData)
        menubar.add_command(label='摄像头设置', command=self.countData)
        menubar.add_command(label='坐标校准', command=self.xyCheck)
        menubar.add_command(label='机器学习设置', command=self.learnfram)
        menubar.add_command(label='用户管理', command=self.aboutDisp)
        menubar.add_command(label='关于&帮助', command=self.aboutUs)
        self.root['menu'] = menubar  # 设置菜单栏

    def inputData(self):
        self.inputPage.pack()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack_forget()
        self.learnPage.pack_forget()

    def queryData(self):
        self.inputPage.pack_forget()
        self.queryPage.pack()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack_forget()
        self.learnPage.pack_forget()

    def countData(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack_forget()
        self.learnPage.pack_forget()

    def aboutDisp(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack_forget()
        self.learnPage.pack_forget()

    def xyCheck(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack()
        self.aboutusPage.pack_forget()
        self.learnPage.pack_forget()

    def learnfram(self):
        self.learnPage.pack()
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack_forget()

    def aboutUs(self):
        self.inputPage.pack_forget()
        self.queryPage.pack_forget()
        self.countPage.pack_forget()
        self.aboutPage.pack_forget()
        self.xycheckPage.pack_forget()
        self.aboutusPage.pack()
        self.learnPage.pack_forget()
