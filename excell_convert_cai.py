#coding=utf-8
import xlrd
import re

path="/Users/caiyaxin/Desktop/Caiyaxin_Work/4x10G_V4/4x10G_V4/titan_v4_regmap_0210"

work_book=xlrd.open_workbook(path+'.xlsm')
sheet=work_book.sheet_by_index(0)
print(sheet.nrows)

class Data():
    name=''
    addr=''
    bit_st=''
    bits=''
    Dec=''
    rw=''
    description=''
def getRowData(sheet,row):
    d=Data()

    if row>24:
        curAddr=re.findall(r'0x([\d\w]+)',sheet.row(row)[0].value)
        #print(curAddr)
        if curAddr!=[]:
            d.addr=curAddr[0]
            d.name=''
            #print(d.addr)
        else:
            d.addr=''
            d.name=sheet.row(row)[1].value
            #print(d.name)
            d.bit_st=str(int(sheet.row(row)[4].value))
            d.bits=str(sheet.row(row)[3].value)
            d.rw=sheet.row(row)[5].value
            d.Dec=str(sheet.row(row)[6].value) if str(sheet.row(row)[6].value)!='' else '0'
            d.description=','.join(sheet.row(row)[8].value.split('\n'))
    return d


with open(path+'.txt','w+') as f:
    curAddr=''
    Data_sheet=work_book.sheet_by_name('public')
    rowNum=Data_sheet.nrows
    colNum=Data_sheet.ncols
    print(rowNum)
    print(colNum)
    for row in range(rowNum):
        v = getRowData(Data_sheet, row)
        if row==1:
            f.write('\t'.join(['#name','addr_st','bit_st','bits','Default','coding','description'])+'\n')
        else:
            if v.addr!='':
                curAddr=v.addr
        #f.write('end'+'\n')
        #f.write('\t'.join([v.name, '0x00' + str(v.addr), v.bit_st, v.bits, v.Dec, v.rw, v.description]) + '\n')
        #print(v.addr)
            if v.name!='' and v.addr==''and curAddr!='':
                f.write('\t'.join([v.name,'0x00'+curAddr,v.bit_st,v.bits,v.Dec,v.rw,v.description])+'\n')


