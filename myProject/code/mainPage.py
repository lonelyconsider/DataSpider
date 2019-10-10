# -*- coding: utf-8 -*-
import tkinter
import sqlEngine as se
import salaryAnalysis
import wordAnalysis
import mySpider
import educationAnalysis
import scaleAnalysis
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from sqlalchemy.orm import sessionmaker


class MainPage(object):
    def __init__(self):
        self.df = ''
        self.time_code = ''
        self.number_listbox = 0

        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()

        self.root = tkinter.Tk()
        self.root.title('主界面')
        self.root.resizable(0, 0)

        # window size and center
        self.window_width = 1200
        self.window_height = 680
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.x = (self.screen_width - self.window_width) / 2
        self.y = (self.screen_height - self.window_height) / 2 - 40
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, self.x, self.y))

        # frame
        # 菜单
        self.menu = Frame(self.root, height=700, width=295, bg='white')
        # 栏目（右上）
        # self.index = Frame(self.root,height=700,width=700)
        # 主要功能（右下）
        self.func = Frame(self.root,height = 700,width = 600)

        # canvas
        self.canvas = Canvas(self.menu, width=295, height=100, bd=0, bg='white')
        # self.path = str(os.path.abspath(""))
        self.im = Image.open('..\image\dog_menu.jpg')
        self.img = ImageTk.PhotoImage(self.im)
        self.image = self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        self.text = self.canvas.create_text((125, 70), text='昵称：年轻的哈士奇', anchor='w', fill='black', font=('黑体', 12))

        self.bt_user_management = Button(self.menu, text='使用说明', height=1, width=20, font='等线,14', bg='white', bd=1,
                                         command=self.show_helper)
        self.bt_text_analysis = Button(self.menu, text='薪资层次分析', height=1, width=20, font='等线,14', bg='white', bd=1,
                                       command=self.salary_analysis)
        self.bt_helper = Button(self.menu, text='教育程度分析', height=1, width=20, font='等线,14', bg='white', bd=1,
                                command=self.education_analysis)
        self.bt_info_import = Button(self.menu, text='任职要求关键字分析', height=1, width=20, font='等线,14', bg='white', bd=1,
                                     command=self.word_analysis)
        self.bt_about_us = Button(self.menu, text='职位分析', height=1, width=20, font='等线,14', bg='white', bd=1)
        self.bt_scale_analysis = Button(self.menu, text='企业规模分析', height=1, width=20, font='等线,14', bg='white', bd=1,
                                        command=self.scale_analysis)
        self.bt_easy_collect = ttk.Button(self.func, text='分类采集', command=self.my_spider)
        self.bt_custom_collect = ttk.Button(self.func, text='显示结果', command=self.displayInfo)

        # add a title label
        self.lp_title = Label(self.func,text='招聘信息的数据采集与分析', font=("Arial Black", 19), fg='black', bd=3, width=70,
                              bg='#F0FFFF', height=3, anchor='w')

        # notebook
        self.tabControl = ttk.Notebook(self.func, height=700, width=600)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='主页')      # Add the tab
        # set canvas
        self.canvas.grid(column=0, row=0, sticky=NW, padx=5, pady=0)
        # listbox && Scrollbar
        self.display_info = tkinter.Listbox(self.func, width=122, height=20, selectmode=BROWSE)
        # set button
        self.bt_user_management.grid(column=0, row=1, sticky=NW, padx=60, pady=20)
        self.bt_text_analysis.grid(column=0, row=2, sticky=NW, padx=60, pady=20)
        self.bt_info_import.grid(column=0, row=3, sticky=NW, padx=60, pady=20)
        self.bt_helper.grid(column=0, row=4, sticky=NW, padx=60, pady=20)
        self.bt_scale_analysis.grid(column=0, row=5, sticky=NW, padx=60, pady=20)
        # set listbox
        self.display_info.grid(column=0, row=1, sticky=NW, padx=20, pady=20)

        self.bt_easy_collect.grid(column=0, row=2, sticky=NW, padx=260, pady=40)
        self.bt_custom_collect.grid(column=0, row=2, sticky=NW, padx=540, pady=40)

        # set label
        self.lp_title.grid(column=0, row=0, sticky=NW, padx=0, pady=0)

        # set frame
        self.menu.grid(column=0, row=0, sticky=NW, padx=0, pady=0)
        self.func.grid(column=1, row=0, sticky=NW, padx=0, pady=0)

        self.menu.grid_propagate(0)

    def show_result(self):
        pass

    def scale_analysis(self):
        scaleAnalysis.ScaleAnalysis()
        self.root.update()

    def education_analysis(self):
        educationAnalysis.EducationAnalysis()
        self.root.update()

    def salary_analysis(self):
        salaryAnalysis.SalaryAnalysis()
        self.root.update()

    def word_analysis(self):
        wordAnalysis.WordAnalysis()
        self.root.update()

    def my_spider(self):
        my = mySpider.Spider()
        self.time_code = my.timeCode
        self.root.update()

    def displayInfo(self):
        if self.time_code == '':
            self.display_info.delete(0, END)
            self.display_info.insert(END, 'NOTHING！')
            self.display_info.insert(END, '你还没有启动爬虫程序！')
            self.display_info.update()
            self.root.update()
        else:
            self.df = self.session.execute("select * from dao.recruit_information where time_code = '{0}'".format(str(self.time_code)))  #
            self.display_info.delete(0, END)
            for i in self.df:
                record = '职位:'+i[0]+'    公司:'+i[1]+'      工作地点:'+i[4]+'      薪资:'+str(i[3])+'      详情页:'+i[7]
                self.display_info.insert(END, record)
            self.display_info.update()
            self.root.update()

    def show_helper(self):
        self.display_info.delete(0, END)
        self.display_info.insert(END, '********************************************************************************'
                                      '*使用说明******************************************************************'
                                      '***************')
        self.display_info.insert(END, '')
        self.display_info.insert(END, '薪资水平分析：以柱状图展示各城市各地区的各薪资段职位分布情况')
        self.display_info.insert(END, '')
        self.display_info.insert(END, '任职要求分析：以词云展示各职位要求的重心')
        self.display_info.insert(END, '')
        self.display_info.insert(END, '教育程度分析：以饼图展示各教育程度职位数的分布情况')
        self.display_info.insert(END, '')
        self.display_info.insert(END, '企业规模分析：以折线图展示企业规模的职位数分布情况')
        self.display_info.insert(END, '')
        self.display_info.insert(END, '')
        self.display_info.itemconfig(0, fg='black')
        self.display_info.update()


if __name__ == '__main__':
    m = MainPage()
    m.root.mainloop()
