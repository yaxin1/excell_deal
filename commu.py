#coding=utf-8
from tkinter import *
import tkinter.messagebox

def xz():
    answer=tkinter.messagebox.askokcancel('结果','请做出选择')
    if answer:
        lb.config(text='已确认')
    else:
        lb.config(text='已取消')

root=Tk()
root.title('请选择')
root.geometry('320x320')

lb=Label(root,text='请选择确定或取消')
lb.place(relx=0.2,rely=0.5)

lb.pack()
btn=Button(root,text='弹出对话框了',command=xz)
btn.pack()
root.mainloop()