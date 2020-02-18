#coding=utf-8
from tkinter import *
import math
def run1():
    a=float(inp1.get())
    b=float(inp2.get())
    s='%0.2f+%0.2f=%0.2f\n'%(a,b,a+b)
    txt.insert(END,s)
    inp1.delete(0,END)
    inp2.delete(0,END)
def run2(x,y):
    a=float(x)
    b=float(y)
    s='%0.2f+%0.2f=%0.2f\n'%(a,b,a+b)
    txt.insert(END, s)
    inp1.delete(0, END)
    inp2.delete(0, END)

add_tools=Tk()
add_tools.title('简单加法器')
add_tools.geometry('500x500')

lb1=Label(add_tools,text='请输入两个数，按下面两个按钮之一进行加法',bg='#d3fbfb',fg='Red',font=('黑体',15),relief=RIDGE)
lb1.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.1)
inp1=Entry(add_tools)
inp1.place(relx=0.1,rely=0.2,relwidth=0.3,relheight=0.1)
inp2=Entry(add_tools)
inp2.place(relx=0.6,rely=0.2,relwidth=0.3,relheight=0.1)

btn1=Button(add_tools,text='加法',command=run1)
btn1.place(relx=0.1,rely=0.4,relwidth=0.3,relheight=0.1)

btn2=Button(add_tools,text='加法2',command=lambda: run2(inp1.get(),inp2.get()))
btn2.place(relx=0.6,rely=0.4,relwidth=0.3,relheight=0.1)

txt=Text(add_tools)
txt.place(rely=0.6,relheight=0.4)

add_tools.mainloop()

