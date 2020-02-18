#coding=utf-8
from tkinter import *
import time
mygui=Tk()
mygui.title('寄存器形式转换')
mygui.geometry('550x550')
var=StringVar()

lb=Label(mygui,textvariable=var,bg='#d3fbfb',fg='blue',font=('黑体',60),width=20,height=2,relief=RIDGE)
def gettime():
    var.set(time.strftime('%H:%M:%S')) #获取当前的时间并转化为字符串
    #lb.configure(text=timestr)
    mygui.after(1000,gettime)

mymenu=Menu()
mymenu.add_command(label='open')
mymenu.add_command(label='add')
mymenu.add_command(label='delect')

mygui.config(menu=mymenu)

text=Text(width=20,height=2)
btn=Button()
btn['text']='登陆名字'
li=['C','python','phy','html','SQL','java']
movie=['CSS','jQuery','Bootstrap']
listb=Listbox(mygui)
listb2=Listbox(mygui)

for item in li:
    listb.insert(0,item)
for item in movie:
    listb2.insert(0,item)

btn.pack()
text.pack()
lb.pack()
gettime()
listb.pack()
listb2.pack()
mygui.mainloop()