# coding=utf-8\
from Tkinter import *
import DBFunction
from tkMessageBox import *

class addPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.importPrice = StringVar()
        self.sellPrice = StringVar()
        self.deductPrice = StringVar()
        self.userid = StringVar()
        self.username = StringVar()
        self.userpass = StringVar()

        self.createPage()

    def createPage(self):

        cem_frame = Frame(self, width=585, height=540, bg='white')
        cem_frame.grid()
        px = 2
        py = 10
        Label(cem_frame, width=83, bg='white').grid(row=0, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='添加用户', width=30, font=("宋体", 18, "bold")).grid(row=1, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='工号',  width=10).grid(row=2, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userid).grid(row=2, column=1, padx=px, pady=py, sticky=W)
        Label(cem_frame, bg='white', text='姓名',  width=10).grid(row=3, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.username).grid(row=3, column=1, padx=px, pady=py, sticky=W)
        Label(cem_frame, bg='white', text='密码',  width=10).grid(row=4, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userpass).grid(row=4, column=1, padx=px, pady=py, sticky=W)
        Button(cem_frame, text='提交添加', width=30, command=self.addclick).grid(row=5, column=0, columnspan=2, pady=py)

    def addclick(self):
        uid = int(self.userid.get())
        uname = self.username.get()
        upass = self.userpass.get()
        try:
            DBFunction.addUser(uid, uname, upass)
            showinfo(title='成功', message='用户添加成功！')
        except Exception:
            showinfo(title='失败', message='用户添加失败，主键已存在！')

class delePage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.userid = StringVar()
        self.createPage()

    def createPage(self):
        cem_frame = Frame(self, width=585, height=540, bg='white')
        cem_frame.grid()
        px = 2
        py = 10
        Label(cem_frame, width=83, bg='white').grid(row=0, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='删除用户', width=30, font=("宋体", 18, "bold")).grid(row=1, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='工号', width=10).grid(row=2, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userid).grid(row=2, column=1, padx=px, pady=py, sticky=W)
        Button(cem_frame, text='提交删除', width=30, command=self.deleclick).grid(row=3, column=0, columnspan=2, pady=py)

    def deleclick(self):
        uid = int(self.userid.get())
        print DBFunction.seleUser(uid)
        if DBFunction.seleUser(uid)==[]:
            showinfo(title='失败', message='删除失败，用户不存在！')
        else :
            DBFunction.deleUser(uid)
            showinfo(title='成功', message='删除成功！')


class modPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.userid = StringVar()
        self.username = StringVar()
        self.userpass = StringVar()
        self.createPage()

    def createPage(self):
        cem_frame = Frame(self, width=585, height=540, bg='white')
        cem_frame.grid()
        px = 2
        py = 10
        Label(cem_frame, width=83, bg='white').grid(row=0, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='修改用户', width=30, font=("宋体", 18, "bold")).grid(row=1, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='工号', width=10).grid(row=2, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userid).grid(row=2, column=1, padx=px, pady=py, sticky=W)
        Label(cem_frame, bg='white', text='姓名', width=10).grid(row=3, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.username).grid(row=3, column=1, padx=px, pady=py, sticky=W)
        Label(cem_frame, bg='white', text='密码', width=10).grid(row=4, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userpass).grid(row=4, column=1, padx=px, pady=py, sticky=W)
        Button(cem_frame, text='提交修改', width=30, command=self.modclick).grid(row=5, column=0, columnspan=2, pady=py)

    def modclick(self):
        uid = int(self.userid.get())
        uname = self.username.get()
        upass = self.userpass.get()
        try:
            DBFunction.modUser(uid, uname, upass)
            showinfo(title='成功', message='修改成功！')
        except Exception:
            showinfo(title='失败', message='修改失败！工号不存在')

class selePage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.userid = StringVar()
        self.text_result = Text()
        self.text_result
        self.createPage()

    def createPage(self):
        def seleclick():
            uid = int(self.userid.get())
            msgcontent = DBFunction.seleUser(uid)
            result = '工号：', msgcontent[0][0], '姓名：', msgcontent[0][1]
            text_result.insert(END, result)

        cem_frame = Frame(self, width=585, height=540, bg='white')
        cem_frame.grid()
        px = 2
        py = 10
        Label(cem_frame, width=83, bg='white').grid(row=0, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='查询用户', width=30, font=("宋体", 18, "bold")).grid(row=1, column=0, columnspan=2, padx=0, pady=30)
        Label(cem_frame, bg='white', text='工号', width=10).grid(row=2, column=0, pady=py, sticky=E)
        Entry(cem_frame, textvariable=self.userid).grid(row=2, column=1, padx=px, pady=py, sticky=W)
        Button(cem_frame, text='提交查询', width=30, command=seleclick).grid(row=3, column=0, columnspan=2, pady=py)

        text_result = Text(cem_frame, height=10, width=30)
        text_result.grid(row=4, column=0, columnspan=2, pady=20)


