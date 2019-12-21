# -*- coding: UTF-8 -*-
from tkinter import *
import pandas as pd
import tkinter.filedialog
root = Tk()
string_filename = ""

def xz():
    filenames = tkinter.filedialog.askopenfilenames()
    global string_filename
    if len(filenames) != 0:
        for i in range(0,len(filenames)):
            string_filename += str(filenames[i])
            # print(string_filename)
        lb.config(text = "您选择的文件是："+string_filename)
        btn1 = Button(root, text="开始提取", command=lambda: tiqu(string_filename))
        btn1.pack()
    else:
        lb.config(text = "您没有选择任何文件！")

def tiqu(string_filename1):
    global string_filename
    print(string_filename1)
    rf = pd.read_excel(string_filename1)
    # 读取第10列
    data_rf = rf.ix[0:, 10].values
    # 除去空数据
    data_df = pd.DataFrame(data_rf)
    data_df.dropna(inplace=True)

    # 写入excel
    pstart = string_filename1.index('.')
    address = string_filename1[0:pstart]
    address = address + "_extract.xlsx"
    writer = pd.ExcelWriter(address)
    data_df.to_excel(writer, index=False, header=False)
    writer.save()

    # # 读取第11列
    data_rf1 = rf.ix[1:, 11].values
    # 除去空数据并分割出号码;
    number = []
    for index in range(len(data_rf1)):
        data_str = str(data_rf1[index])
        if data_str.count(';') == 1:
            mobile = data_str.replace(';', '')
            number.append(mobile)
        elif data_str.count(';') == 2:
            pstart = data_str.index(';')
            mobile1 = data_str[0:pstart]
            number.append(mobile1)
            mobile2 = data_str[pstart + 1:-1]
            number.append(mobile2)
        elif data_str.count(';') == 3:
            pstart = data_str.index(';')
            mobile3 = data_str[0:pstart]
            number.append(mobile3)
            mobile4 = data_str[pstart + 1:]
            pstart = mobile4.index(';')
            mobile5 = mobile4[0:pstart]
            number.append(mobile5)
            mobile6 = mobile4[pstart + 1:-1]
            number.append(mobile6)
    # for index in range(len(number)):
    data_df1 = pd.DataFrame(number)
    data_df1.dropna(inplace=True)
    # 写入excel
    s_sum = data_df1.shape[0]
    data_df1.to_excel(writer, index=False, header=False, startrow=s_sum)
    writer.save()
    lb.config(text="提取完成！")
    string_filename = ''

lb = Label(root,text = '')
lb.pack()
btn = Button(root, text="选择文件", command=xz)
btn.pack(expand = 10)
root.title('号码提取器')
# center_window(root, 300, 240)
root.maxsize(600, 400)
root.minsize(300, 240)
root.mainloop()