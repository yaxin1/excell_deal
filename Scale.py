#coding=utf-8

from tkinter import *
#from tkinter.ttk import *

def show(event):
    s='滑块的取值为'+str(var.get())
    lb.config(text=s)

root=Tk()
root.title('滑块实验')
root.geometry('320x320')
lb=Label(root,text='')
#lb.place(relx=0.2,rely=0.0)
lb.pack()

var=DoubleVar()
scl=Scale(root,orient=HORIZONTAL,length=200,from_=1.0,to=5.0,label='请拖动滑块',tickinterval=1.0)
scl.bind('<ButtonRelease-1>',show)
scl.pack()

lb=Label(root,text='')
#lb.place(relx=0.2,rely=0.0)
lb.pack()

root.mainloop()