# coding=utf-8

import xlrd
import re

path="/Users/caiyaxin/Desktop/Caiyaxin_Work/4x10G_V4/4x10G_V4/titan_v4_regmap_0210.xlsm"

path2="/Users/caiyaxin/Desktop/Caiyaxin_Work/4x10G_V4/4x10G_V4/titan_v4_reg1"
path3="/Users/caiyaxin/Desktop/Caiyaxin_Work/4x10G_V4/4x10G_V4/titan_v4_tmp"
work_book=xlrd.open_workbook(path)
print(work_book.sheet_names())
sheet=work_book.sheet_by_index(0)

print(sheet.name)
print(sheet.nrows)
print(sheet.ncols)
#print(sheet.row_slice(25,start_colx=0,end_colx=12))
#print(sheet.row_types(25))
#print(sheet.row_values(25))
#print(sheet.cell(25,0).value)
#print(sheet.cell(28,4).ctype)
#print(sheet.cell_value(25,0))
#print(sheet.row(25)[0])
#print(sheet.col(0))
#print(sheet.col(0)[25])
#print(sheet.cell_type(25,0))
#print(xlrd.cellname(25,0))
#print(xlrd.cellnameabs(25,0))
#print(xlrd.colname(3))

class Data:
    name=''
    addr_st=''
    bit_st=''
    bits=''
    Default=''
    coding=''
    description=''
def getRowData(sheet1,row1):
    d=Data()
    d.name=sheet1.row(row1)[1].value
    d.addr_st=re.findall(r'0x([\d\w]+)',sheet1.row(row1)[0].value)
    if d.addr_st==[]:
        d.addr_st=''
    else:
        d.addr_st=d.addr_st[0]

    if sheet1.cell(row, 4).ctype == 2 and sheet1.row(row1)[4].value % 1 == 0.0:  # ctype为2且为浮点
        d.bit_st = str(int(sheet1.row(row1)[4].value))
    else:
        d.bit_st = sheet1.row(row1)[4].value
    if sheet1.cell(row, 3).ctype == 2 and sheet1.row(row1)[3].value % 1 == 0.0:  # ctype为2且为浮点
        d.bits = str(int(sheet1.row(row1)[3].value))
    else:
        d.bits = sheet1.row(row1)[3].value
    if sheet1.cell(row, 6).ctype == 2 and sheet1.row(row1)[6].value % 1 == 0.0:  # ctype为2且为浮点
        d.Default = str(int(sheet1.row(row1)[6].value))
    else:
        d.Default = sheet1.row(row1)[6].value if sheet1.row(row1)[6].value!='' else "0"

    d.coding = sheet1.row(row1)[5].value
    d.description=','.join(sheet.row(row)[8].value.split('\n'))

    return d
def getTxtLineData(line):
    d = Data()

    d.name, d.addr_st, d.bit_st, d.bits, d.Default, d.coding, d.description = line.split('\t')

    return d
def lineRangeWithSameReg(row,lines):
    if len(lines)<2 or row>len(lines)-2:
        return range(row,row)
    row_idx=row
    while getTxtLineData(lines[row_idx+1]).name==getTxtLineData(lines[row]).name:
        row_idx+=1
        if row_idx==len(lines)-1:
            return range(row,row_idx+1)

    return range(row,row_idx+1)
def getBitRange(string):
    if '[' in string:
        r=re.findall(r'([\d]+)',string)
        if len(r)==2:

            return r
        elif len(r)==1:
            l=r
            l.append(l[0])
            return l
    else:
        return None

def countBitsNumber(string):
    bits=getBitRange(string)
    return int(bits[0])-int(bits[1])+1 if bits else int(string)
def writeTxtLine(f,line):
    f.write('\t'.join([line.name,line.addr_st,line.bit_st,line.bits,line.Default,line.coding,line.description]))

def findSplitedRegInfo(row,lines):
    row_list=[row]
    bits=countBitsNumber(getTxtLineData(lines[row]).bits)
    for row_idx in range(row+1,len(lines)):
        if getTxtLineData(lines[row_idx]).name==getTxtLineData(lines[row]).name:
            bits+=countBitsNumber(getTxtLineData(lines[row_idx]).bits)
            row_list.append(row_idx)

    return {getTxtLineData(lines[row]).name:bits,getTxtLineData(lines[row]).name+'_span':row_list}

def name_generater():
    i=1
    while True:
        yield ''.join(['_',str(i)])
        i+=1

with open(path3+'.txt',"w+") as f:
    curAddr=''
    Data_sheet=work_book.sheet_by_name('public')
    rowNum=Data_sheet.nrows
    colNum=Data_sheet.ncols
    for row in range(rowNum):
        v=getRowData(Data_sheet,row)
        if row==1:
            f.write('\t'.join(['#name','addr_st','bit_st','bits','Default','coding','description'])+'\n')
        else:
            if v.addr_st!='':
                curAddr=v.addr_st
            if v.name!='' and v.addr_st=='' and curAddr!='':
                f.write('\t'.join([v.name,'0x00'+curAddr,v.bit_st,v.bits,v.Default,v.coding,v.description])+'\n')
            else:
                continue

with open(path3+'.txt','r') as f1:
    regValue = {}
    lines = f1.readlines()
    #print(len(lines))

    for row in range(1, len(lines)):
        line = getTxtLineData(lines[row])

        if line.addr_st in regValue.keys():
            #print(line.addr_st)
            #print( regValue.keys())
            regValue[line.addr_st] += int(line.Default) * pow(2, int(line.bit_st))
        else:
            regValue[line.addr_st] = int(line.Default) * pow(2, int(line.bit_st))

with open(path3+'.txt','r') as f1,open (path2+'.txt','w+') as f2:
    rng=range(-1,0)
    regInfo={}
    lines=f1.readlines()
    combo_reg=[]
    for row in range(0,len(lines)):
        if row in rng:continue
        line=getTxtLineData(lines[row])
        if getBitRange(line.bits)==None:
            f2.write(lines[row])
        else:
             reg_name=getTxtLineData(lines[row]).name

             rng=lineRangeWithSameReg(row,lines)
             #print(rng)

             if len(rng)>1 and (getBitRange(line.bits)[1]=='0' or int(getBitRange(line.bits)[0])<int(
                     getBitRange(getTxtLineData(lines[row+1]).bits)[1])):

                 # print(reg_name,getBitRange(line.bits)[1],getBitRange(line.bits)[0],
                 #       getBitRange(getTxtLineData(lines[row+1]).bits)[1])
                 bits=0
                 for r in rng:
                     # print(r)
                     # print(getTxtLineData(lines[r]).bits)
                     bits+=countBitsNumber(getTxtLineData(lines[r]).bits)
                     #print(bits)
                 line.bits=str(bits)
                 writeTxtLine(f2,line)

            #     if reg_name in combo_reg and int (getBitRange(getTxtLineData(lines[row]).bits)[0])<int(
            #             getBitRange(getTxtLineData(lines[row+1]).bits)[1]):
            #         line.name+='_high'
            #     writeTxtLine(f2,line)
             else:
                 if len(rng)==1:

                     # bits1=countBitsNumber(getTxtLineData(lines[row]).bits)
                     # line.bits=str(bits1)
                     #writeTxtLine(f2,line)
                     # print(regInfo.keys())
                     if line.name not in regInfo.keys():
                         regInfo.update(findSplitedRegInfo(row,lines))
                     high_mid_low=regInfo[line.name]/(int(getBitRange(line.bits)[0])+1)
                     if high_mid_low==regInfo[line.name]/8:
                         reg_suffix=['_low']
                     elif high_mid_low==1:
                         reg_suffix=['_high']
                     else:
                         reg_suffix=['_mid']

                 elif len(rng)==3:
                     reg_suffix=['_high','_mid','_low']
                 elif len(rng)==2:
                     reg_suffix=['_high','_low']
                 elif len(rng)>3:
                     print('reg splits into too many pieces:',line.name)
                     n=name_generater()
                     reg_suffix=[]
                     for i in rng:
                         reg_suffix.append(n.__next__())
                 for r,reg_suffix in zip(rng,reg_suffix):
                     l=getTxtLineData(lines[r])
                     l.bits=str(int(getBitRange(l.bits)[0])-int(getBitRange(l.bits)[1])+1)
                     l.name=l.name+reg_suffix
                     writeTxtLine(f2,l)
            # if reg_name not in combo_reg:
            #     combo_reg.append(getTxtLineData(lines[row]).name)
    #print (regInfo)
    f2.write('end\n')
    f2.write('\t'.join(['address','value','rw'])+'\n')
    for k in sorted(regValue.keys()):
        f2.write(k+'\t'+hex(regValue[k])+'\n')
    f2.write('end'+'\n'+'\t'.join(['control','sets'])+'\n'+'\t'.join(['i2c_address','0xF0'])+
             '\n'+'\t'.join(['chip_name','PhxR8104'])+'\n'+'end')



