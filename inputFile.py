#coding=utf-8

from tkinter import *
import tkinter.filedialog

def xz():
    filename=tkinter.filedialog.askopenfile()
    if filename!='':
        lb.config(text='您选的文件是'+filename)
    else:
        lb.config(text='您没有选择任何文件')

root=Tk()
root.title('请输入')
root.geometry('320x320')
lb=Label(root,text='',)
lb.pack()

btn=Button(root,text='弹出文件选择对话框',command=xz)
btn.pack()

root.mainloop()