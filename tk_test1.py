#coding=utf-8

from tkinter import *
import time
import datetime

tk_test1=Tk()
tk_test1.title=('显示时间')
tk_test1.geometry=('500x500')

def gettime():
    s=str(datetime.datetime.now())+'\n'
    txt.insert(END,s)
    tk_test1.after(1000,gettime)

txt=Text(tk_test1)

txt.pack()
gettime()
tk_test1.mainloop()
