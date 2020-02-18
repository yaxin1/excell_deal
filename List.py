#coding=utf-8
from tkinter import *

root=Tk()
root.title('列表框实验')
root.geometry('700x500')

fram1=Frame(root,relief=RAISED)
fram1.place(relx=0.05)

fram2=Frame(root,relief=GROOVE)
fram2.place(relx=0.5)

Lstbox1=Listbox(fram1)
Lstbox1.pack()

entry=Entry(fram2)
entry.pack()

def ini():
    Lstbox1.delete(0,END)
    list_items=['语文','数学','化学','语文','外语']
    for item in list_items:
        Lstbox1.insert(END,item)

def ins():
    if entry.get()!='':
        if Lstbox1.curselection()==():
           Lstbox1.insert(Lstbox1.size(),entry.get())
        else:
            Lstbox1.insert(Lstbox1.curselection(),entry.get())
def updat():
    if entry.get()!='' and Lstbox1.curselection()!='':
        selected=Lstbox1.curselection()[0]
        Lstbox1.delete(selected)
        Lstbox1.insert(selected,entry.get())
def dele():
    if Lstbox1.curselection()!=():
        Lstbox1.delete(Lstbox1.curselection())
def clr():
    Lstbox1.delete(0,END)


btn1=Button(fram2,text='初始化',command=ini)
btn1.pack(fill=X)

btn2=Button(fram2,text='添加',command=ins)
btn2.pack(fill=X)

btn3=Button(fram2,text='插入',command=ins)
btn3.pack(fill=X)

btn4=Button(fram2,text='修改',command=updat)
btn4.pack(fill=X)

btn5=Button(fram2,text='删除',command=dele)
btn5.pack(fill=X)

btn6=Button(fram2,text='清空',command=clr)
btn6.pack(fill=X)

root.mainloop()