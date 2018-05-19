#coding=utf-8
from Tkinter import *
import PIL

def change():
    pass

top = Tk()
bm = PhotoImage(file="D:/workspace/Python/machine/venv/Include/img/logo.gif")
label = Canvas(top,  width=60, height=60)
label.create_image(30, 30, image=bm)
label.pack()
button = Button(top, text="changepicture", command=change)
button.pack()
top.mainloop()