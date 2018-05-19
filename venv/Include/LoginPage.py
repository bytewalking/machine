# -*- coding: utf8 -*-
from Tkinter import *
from tkMessageBox import *
from MainPage import *
import sqlite3

class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.sign_pic = None
        self.exit_pic = None
        self.logo_image = None
        self.bm = None
        self.root.geometry('%dx%d+%d+%d' % (800, 600, (screenwidth - 800)/2, (screenheight - 600)/2))  # 设置窗口大小
        self.root.iconbitmap(os.getcwd()+"/img/vision.ico")
        self.root.resizable(False, False)
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):

        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, columnspan=3, pady=50)
        self.logo_image = PhotoImage(file=os.getcwd()+"/img/logo_main.gif")
        logo_pic = Label(self.page, width=420, height=60, image=self.logo_image)
        logo_pic.grid(row=1, columnspan=3, pady=30)

        Label(self.page, text='工号: ').grid(row=2, pady=10, padx=20, sticky=E)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, columnspan=2, sticky=W)
        Label(self.page, text='密码: ').grid(row=3, pady=10, padx=20, sticky=E)
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, columnspan=2, sticky=W)

        sign_button = Canvas(self.page, width=70, height=70)
        sign_button.grid(row=4, pady=10, sticky=E)
        self.sign_pic = PhotoImage(file=os.getcwd()+"/img/sign_in_icon.gif")
        sign_button.create_image(35, 35, image=self.sign_pic)
        sign_button.bind('<ButtonPress-1>', self.loginCheck)

        exit_button = Canvas(self.page, width=70, height=70)
        exit_button.grid(row=4, column=2, sticky=W)
        self.exit_pic = PhotoImage(file=os.getcwd()+"/img/exit_icon.gif")
        exit_button.create_image(35, 35, image=self.exit_pic)
        exit_button.bind('<ButtonPress-1>', self.exit_event)

        Label(self.page, text='版本(beta)1.5   Copyright：DreamChaserTeam  2014-2018', width=60).grid(row=5, column=0, columnspan=3, pady=140)

    def loginCheck(self, event):
        name = self.username.get()
        secret = self.password.get()

        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('select * from user where name=? and password=?', (name, secret))
        values = cursor.fetchall()

        if values == []:
            showinfo(title='错误', message='账号或密码错误！')
        else:
            self.page.destroy()
            MainPage(self.root)

    def exit_event(self, event):
        self.page.quit()