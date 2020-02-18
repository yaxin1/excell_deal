#coding=utf-8
from tkinter import *

def Mysel():
    dic={0:'甲',1:'乙',2:'丙'}
    print(var.get())
    s='您选择了'+dic.get(var.get())+'项'
    lb.config(text=s)

Radionbutton1=Tk()
Radionbutton1.title('Radiobutton')
Radionbutton1.geometry('500x500')
lb=Label(Radionbutton1)
lb.pack()

var=IntVar()
rd1=Radiobutton(Radionbutton1,text='甲',variable=var,value=0,command=Mysel)
rd1.pack()

rd2=Radiobutton(Radionbutton1,text='乙',variable=var,value=1,command=Mysel)
rd2.pack()

rd3=Radiobutton(Radionbutton1,text='丙',variable=var,value=2,command=Mysel)
rd3.pack()

# lb1=Label(Radionbutton1,text='您选择了乙项')
# lb1.place(relx=0.1,rely=0.0,relwidth=0.3,relheight=0.2)

Radionbutton1.mainloop()
