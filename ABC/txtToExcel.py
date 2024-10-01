
import openpyxl #需要的模块
"""
:文本转换成xls的函数
:param filename txt文本文件名称、
:param xlsname 表示转换后的excel文件名
"""
def trans(filename,xlsname):
    # filename='./instance/Mk03.txt'
    # xlsname='MK03.xlsx'
    #
    f = open(filename)
    xls = openpyxl.Workbook()

    # 获取被激活的 worksheet
    ws = xls.active
    x = 0
    lines=[]
    line=f.readline()
    print(line)
    # 获取文本信息
    while True:

        line = list(map(int,f.readline().split()))
        if not line:
            break
        line.insert(0,x)
        x+=1
        lines.append(line)
    # del lines[0]
    print(lines)
    # 添加首行信息
    max_width=0
    for line in lines:
        max_width=max(max_width,len(line))

    first_line = list(i for i in range(0,max_width,1))
    first_line.insert(0,-1)
    first_line.pop()
    lines.insert(0,first_line)
    for line in lines:
        ws.append(line)

    ws.cell(column=1, row=1).value=None
    f.close()
    xls.save(xlsname)  # 保存xls文件

if __name__ == '__main__':
    # for i in range(4,11):
    #     if(i<10):
    #         filename = './instance/Mk0{}.txt'.format(i)
    #         xlsname = './excels/MK0{}.xlsx'.format(i)
    #     else:
    #         filename = './instance/Mk{}.txt'.format(i)
    #         xlsname = './excels/MK{}.xlsx'.format(i)
    #     trans(filename,xlsname)
    trans('./instance/kacem1010.txt','./excels/kacem1010.xlsx')