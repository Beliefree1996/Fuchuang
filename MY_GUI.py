from tkinter import *
import tkinter.filedialog
import docx
import hashlib
import time

LOG_LINE_NUM = 0


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("MD5转换器")  # 窗口名
        self.init_window_name.geometry('1080x680+10+10')                         #1080x680为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.resizable(width=False, height=False)                    # 设置窗口是否可以变化高和宽
        # self.init_window_name["bg"] = "pink"85
        # #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha", 0.9)                          #虚化，值越小虚化程度越高 标签
        # 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据", font="12")
        self.init_data_label.grid(row=0, column=0, padx=20, sticky=W)
        self.result_data_label = Label(self.init_window_name, text="输出结果", font="12")
        self.result_data_label.grid(row=0, column=12, padx=20, sticky=W)
        self.log_label = Label(self.init_window_name,
                               text="日志", font="12")
        self.log_label.grid(row=12, column=12, padx=20, sticky=W)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=70, height=49)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=15, columnspan=10, padx=20, pady=5)
        self.result_data_Text = Text(self.init_window_name, width=60, height=35)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=6, columnspan=10, padx=20, pady=5)
        self.log_data_Text = Text(self.init_window_name, width=60, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=12, rowspan=3, columnspan=10, padx=20, pady=5)
        # 选择文件按钮
        self.load_text_button = Button(self.init_window_name, text="选择文件", bg="lightblue", width=10,
                                       command=self.load_text)
        self.load_text_button.grid(row=1, column=11)
        # self.load_text_button.pack(expand=10)
        # 转换按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=3, column=11)
        # 清空按钮
        self.clear_button = Button(self.init_window_name, text='清空', bg='red', width=8,
                                   command=self.text_delete)
        self.clear_button.grid(row=5, column=11)

    # 读取文件
    def load_text(self):
        filenames = tkinter.filedialog.askopenfilenames()
        string_filename = ''
        if len(filenames) != 0:
            self.init_data_Text.delete(1.0, END)
            for i in range(0, len(filenames)):
                string_filename += str(filenames[i])
            print(string_filename)
            point_place = string_filename.find('.')
            print(string_filename[point_place+1:])
            file_format = string_filename[point_place+1:]   # 文件格式
            if file_format == 'txt':    # TXT文件
                file_object = open(string_filename, 'r')
                try:
                    textrow = 1.0
                    for line in file_object:
                        # line = line.strip('\n')
                        self.init_data_Text.insert(textrow, line)
                        textrow += textrow + 1
                finally:
                    file_object.close()
                    self.write_log_to_Text("INFO: Reading file succeeded")
            elif file_format == 'docx':     # DOCX文件
                file_object = docx.Document(string_filename)
                textrow = 1.0
                for paragraph in file_object.paragraphs:
                    self.init_data_Text.insert(textrow, paragraph.text+'\n')
                    textrow += textrow + 1
                self.write_log_to_Text("INFO: Reading file succeeded")
            else:
                self.write_log_to_Text("INFO: Does not support reading this type of file")
        else:
            print("您没有选择任何文件！")
            self.write_log_to_Text("INFO: You have not selected any files")

    # 清空输入框
    def text_delete(self):
        self.init_data_Text.delete(1.0, END)
        self.write_log_to_Text("INFO: Clear input box data")

    # 功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        # print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                # print(myMd5_Digest)
                # 输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
                self.write_log_to_Text("INFO: String to MD5 success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR: String to MD5 failed")

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
