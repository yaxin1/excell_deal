#coding=utf-8

from tkinter.ttk import *
from tkinter import *

def calc(event):
    a=float(t1.get())
    b=float(t2.get())
    dic={0:a+b,1:a-b,2:a*b,3:a/b}
    print(comb.current())
    c=dic[comb.current()]
    lb1.config(text=str(c))


root=Tk()
root.title('四则运算')
root.geometry('320x320')

t1=Entry(root)
t1.place(relx=0.1,rely=0.1,relwidth=0.2,relheight=0.1)

t2=Entry(root)
t2.place(relx=0.5,rely=0.1,relwidth=0.2,relheight=0.1)

var=StringVar()

comb=Combobox(root,textvariable=var,values=['加','减','乘','除'])
comb.place(relx=0.1,rely=0.5,relwidth=0.2)
comb.bind('<<ComboboxSelected>>',calc)

lb1=Label(root,text='结果',font='red')
lb1.place(relx=0.2,rely=0.7,relwidth=0.2,relheight=0.2)

root.mainloop()