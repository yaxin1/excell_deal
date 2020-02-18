#coding=utf-8

from tkinter import *
from tkinter.simpledialog import *

def xz():
    s=askstring('请输入','请输入一串文字')
    lb.config(text=s)

root=Tk()
root.title('请输入')
root.geometry('320x320')

lb=Label(root,text='')
lb.place(relx=0.01,rely=0.01)
btn=Button(root,text='弹出对话框',command=xz)
btn.pack()

root.mainloop()