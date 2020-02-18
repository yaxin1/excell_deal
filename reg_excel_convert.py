# coding=utf-8
import os
import re
import sys

import xlrd

# 设置路径
path = sys.argv[1]

# 打开execl
workbook = xlrd.open_workbook(path)

# 输出Excel文件中所有sheet的名字
sheetNames = workbook.sheet_names()
print(sheetNames)

pageAddr = ['0x00', '0xA1', '0xB2', '0xC3', '0xD4', '0xE5', '0xF6']
if len(sheetNames) < 7:
    pageAddr = pageAddr[0:len(sheetNames)]
else:
    pageAddr = pageAddr[0:7]


# 根据sheet索引或者名称获取sheet内容
# Data_sheet = workbook.sheets()[0]  # 通过索引获取
# Data_sheet = workbook.sheet_by_index(0)  # 通过索引获取
# Data_sheet = workbook.sheet_by_name(u'名称')  # 通过名称获取
class Data:
    regName = ''
    addr = ''
    bit_st = ''
    bits = ''
    dec = ''
    rw = ''
    description = ''


def getRowData(sheet, row):
    d = Data()

    d.regName = sheet.row(row)[1].value
    d.addr = re.findall(r'0x([\d\w]+)', sheet.row(row)[0].value)
    if d.addr == []:
        d.addr = ''
    else:
        d.addr = d.addr[0]

    if sheet.cell(row, 4).ctype == 2 and sheet.row(row)[4].value % 1 == 0.0:  # ctype为2且为浮点
        d.bit_st = str(int(sheet.row(row)[4].value))
    else:
        d.bit_st = sheet.row(row)[4].value
    if sheet.cell(row, 3).ctype == 2 and sheet.row(row)[3].value % 1 == 0.0:  # ctype为2且为浮点
        d.bits = str(int(sheet.row(row)[3].value))
    else:
        d.bits = sheet.row(row)[3].value
    if sheet.cell(row, 6).ctype == 2 and sheet.row(row)[6].value % 1 == 0.0:  # ctype为2且为浮点
        d.dec = str(int(sheet.row(row)[6].value))
    else:
        d.dec = str(sheet.row(row)[6].value) if sheet.row(row)[6].value != '' else "0"

    d.rw = sheet.row(row)[5].value
    d.description = ','.join(sheet.row(row)[8].value.split('\n'))

    return d


def getBitRange(string):
    if '[' in string:
        if len(re.findall(r'([\d]+)', string)) == 2:
            return re.findall(r'([\d]+)', string)
        elif len(re.findall(r'([\d]+)', string)) == 1:
            l = re.findall(r'([\d]+)', string)
            l.append(l[0])
            return l
    else:
        return None


def countBitsNumber(string):
    bits = getBitRange(string)
    return int(bits[0]) - int(bits[1]) + 1 if bits else int(string)


def getTxtLineData(line):
    d = Data()

    d.regName, d.addr, d.bit_st, d.bits, d.dec, d.rw, d.description = line.split('\t')

    return d


def lineRangeWithSameReg(row, lines):
    if len(lines) < 2 or row > len(lines) - 2:
        return range(row, row)
    row_idx = row
    while getTxtLineData(lines[row_idx + 1]).regName == getTxtLineData(lines[row]).regName:
        row_idx += 1
        if row_idx == len(lines) - 1:
            return range(row, row_idx + 1)

    return range(row, row_idx + 1)


def findSplitedRegInfo(row, lines):
    row_list = [row]
    bits = countBitsNumber(getTxtLineData(lines[row]).bits)
    for row_idx in range(row + 1, len(lines)):
        if getTxtLineData(lines[row_idx]).regName == getTxtLineData(lines[row]).regName:
            bits += countBitsNumber(getTxtLineData(lines[row_idx]).bits)
            row_list.append(row_idx)

    return {getTxtLineData(lines[row]).regName: bits, getTxtLineData(lines[row]).regName + '_span': row_list}


def writeTxtLine(f, line):
    f.write('\t'.join([line.regName, line.addr, line.bit_st, line.bits, line.dec, line.rw, line.description]))


def name_generator():
    i = 1
    while True:
        yield ''.join(['_', str(i)])
        i += 1


with open(path + '.tmp', 'w+') as f:
    # f.write('#name    addr_st    bit_st    bits    Default (DEC)    coding    \n')
    curAddr = ''
    for sheet, page in zip(sheetNames, pageAddr):
        Data_sheet = workbook.sheet_by_name(sheet)
        rowNum = Data_sheet.nrows  # sheet行数
        colNum = Data_sheet.ncols  # sheet列数
        for row in range(rowNum):
            v = getRowData(Data_sheet, row)
            if v.addr != '':
                curAddr = v.addr
            if v.regName != '' and v.addr == '' and curAddr != '':
                f.write('\t'.join([v.regName, page + curAddr, v.bit_st, v.bits, v.dec, v.rw, v.description]) + '\n')
            else:
                continue

with open(path + '.tmp', 'r') as f1:
    regValue = {}
    lines = f1.readlines()

    for row in range(1, len(lines)):
        line = getTxtLineData(lines[row])
        if line.addr in regValue.keys():
            regValue[line.addr] += int(line.dec) * pow(2, int(line.bit_st))
        else:
            regValue[line.addr] = int(line.dec) * pow(2, int(line.bit_st))

# sys.exit(1)
with open(path + '.tmp', 'r') as f1, open(path + '.txt', 'w+') as f2:
    rng = range(-1, 0)
    regInfo = {}
    lines = f1.readlines()
    combo_reg = []

    for row in range(0, len(lines)):
        if row in rng: continue
        line = getTxtLineData(lines[row])
        if getBitRange(line.bits) == None:
            f2.write(lines[row])
        else:
            reg_name = getTxtLineData(lines[row]).regName

            rng = lineRangeWithSameReg(row, lines)

            if len(rng) > 1 and (getBitRange(line.bits)[1] == '0' or int(getBitRange(line.bits)[0]) < int(
                    getBitRange(getTxtLineData(lines[row + 1]).bits)[1])):
                print(reg_name, getBitRange(line.bits)[1], getBitRange(line.bits)[0],
                      getBitRange(getTxtLineData(lines[row + 1]).bits)[1])
                bits = 0
                for r in rng:
                    bits += countBitsNumber(getTxtLineData(lines[r]).bits)
                line.bits = str(bits)
                if reg_name in combo_reg and int(getBitRange(getTxtLineData(lines[row]).bits)[0]) < int(
                        getBitRange(getTxtLineData(lines[row + 1]).bits)[1]):
                    line.regName += '_high'
                writeTxtLine(f2, line)
            else:
                if len(rng) == 1:
                    if line.regName not in regInfo.keys():
                        regInfo.update(findSplitedRegInfo(row, lines))
                    high_mid_low = regInfo[line.regName] / (int(getBitRange(line.bits)[0]) + 1)
                    if high_mid_low == regInfo[line.regName] / 8:
                        reg_suffix = ['_low']
                    elif high_mid_low == 1:
                        reg_suffix = ['_high']
                    else:
                        reg_suffix = ['_mid']
                elif len(rng) == 3:
                    reg_suffix = ['_high', '_mid', '_low']
                elif len(rng) == 2:
                    reg_suffix = ['_high', '_low']
                elif len(rng) > 3:
                    print('Reg splits into too many pieces :', line.regName)
                    n = name_generator()
                    reg_suffix = []
                    for i in rng:
                        reg_suffix.append(n.__next__())
                for r, suffix in zip(rng, reg_suffix):
                    l = getTxtLineData(lines[r])
                    l.bits = str(int(getBitRange(l.bits)[0]) - int(getBitRange(l.bits)[1]) + 1)
                    l.regName = l.regName + suffix
                    writeTxtLine(f2, l)

            if reg_name not in combo_reg:
                combo_reg.append(getTxtLineData(lines[row]).regName)

    print(regInfo)
    f2.write('end\naddress    value    rw\n')
    for k in sorted(regValue.keys()):
        f2.write(k + '\t' + hex(regValue[k]) + '\n')

    f2.write("""end
control    sets
i2c_address    0xF0
chip_name    atlas
end""")

os.remove(path + '.tmp')

# 获取所有单元格的内容
# list = []
# for i in range(rowNum):
# rowlist = []
# for j in range(colNum):
# rowlist.append(Data_sheet.cell_value(i, j))
# list.append(rowlist)
# 输出所有单元格的内容
# for i in range(rowNum):
# for j in range(colNum):
# print(list[i][j], '\t\t', end="")
# print()

# 获取整行和整列的值（列表）
# rows = Data_sheet.row_values(6)  # 获取第一行内容
# cols = Data_sheet.col_values(0)  # 获取第二列内容
# print (rows)
# print (cols)

# 获取单元格内容
# cell_A1 = Data_sheet.cell(0, 0).value
# cell_B1 = Data_sheet.row(0)[1].value  # 使用行索引
# cell_C1 = Data_sheet.cell(0, 2).value
# cell_D2 = Data_sheet.col(3)[1].value  # 使用列索引
# print(cell_A1, cell_B1, cell_C1, cell_D2)

# 获取单元格内容的数据类型
# ctype:0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
# print('cell(0,0)数据类型:', Data_sheet.cell(0, 0).ctype)
# print('cell(1,0)数据类型:', Data_sheet.cell(1, 0).ctype)
# print('cell(1,1)数据类型:', Data_sheet.cell(1, 1).ctype)
# print('cell(1,2)数据类型:', Data_sheet.cell(1, 2).ctype)

# 获取单元格内容为日期的数据
# date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(1,0),workbook.datemode)
# print(type(date_value), date_value)
# print('%d:%d:%d' % (date_value[0:3]))
