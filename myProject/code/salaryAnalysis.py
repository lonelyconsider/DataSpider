# -*- coding:utf-8 -*-
# 分析平均薪资水平
import tkinter
import matplotlib.pyplot as plt
import sqlEngine as se
from sqlalchemy.orm import sessionmaker
from tkinter import *
import pandas as pd
import seaborn as sns
import numpy as np
from tkinter import ttk


class SalaryAnalysis(object):
    def __init__(self):
        self.df = {}
        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()

        self.list = ['不限']
        self.root = tkinter.Tk()
        self.root.title('薪资分析')
        self.root.resizable(0, 0)

        # window size and center
        self.window_width = 400
        self.window_height = 250
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.x = (self.screen_width - self.window_width) / 2
        self.y = (self.screen_height - self.window_height) / 2
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, self.x, self.y))

        '''
        创建控件
        '''
        # label
        self.lp_city = ttk.Label(self.root, text='选择城市:')
        self.lp_region = ttk.Label(self.root, text='选择地区:')
        self.lp_keyword = ttk.Label(self.root, text='职位类型:')

        self.number = StringVar()
        self.cityChosen = ttk.Combobox(self.root, textvariable=self.number, width=13, state='readonly')
        self.cityChosen['values'] = ('北京', '上海', '广州', '深圳', '天津', '武汉', '西安', '成都', '大连', '长春', '沈阳', '南京',
                                     '济南', '青岛', '杭州', '苏州', '无锡', '宁波', '重庆', '郑州', '长沙', '福州', '厦门', '哈尔滨',
                                     '石家庄', '合肥', '惠州', '马鞍山')
        self.cityChosen.current(0)
        self.cityChosen.bind('<<ComboboxSelected>>', self.change)
        self.regionChosen = ttk.Combobox(self.root, width=13, state='readonly')
        self.regionChosen['values'] = ('不限', '嘉定', '杨浦', '浦东新区', '青浦', '黄浦', '闸北', '崇明县', '静安', '虹口', '长宁', '普陀', '闵行', '徐汇', '金山', '宝山', '松江', '奉贤')
        self.regionChosen.current(0)

        self.keyword = ttk.Combobox(self.root, width=13, state='readonly')
        self.position = self.session.execute("select distinct keyword from dao.recruit_information")
        self.position_list = ['不限']
        for i in self.position:
            self.position_list.append(i[0])
        self.keyword['values'] = tuple(self.position_list)
        self.keyword.current(0)
        self.start = ttk.Button(self.root, width=10, text='开始', command=self.analysis)
        '''
        布置控件
        '''
        self.lp_city.grid(column=0, row=0, sticky=NW, padx=100, pady=12)
        self.lp_region.grid(column=0, row=1, sticky=NW, padx=100, pady=12)
        self.lp_keyword.grid(column=0, row=2, sticky=NW, padx=100, pady=12)

        #
        self.cityChosen.grid(column=0, row=0, sticky=NW, padx=170, pady=10)
        self.regionChosen.grid(column=0, row=1, sticky=NW, padx=170, pady=10)
        self.keyword.grid(column=0, row=2, sticky=NW, padx=170, pady=10)

        #
        self.start.grid(column=0, row=3, sticky=NW, padx=160, pady=40)

    def change(self, event):
        region = self.session.execute("select region from dao.region_information where city = '{0}'".format(self.cityChosen.get()))
        for i in region:
            self.list.append(i[0])
        self.regionChosen['values'] = tuple(self.list)
        self.regionChosen.update()
        self.root.update()
        self.list = ['不限']

    def analysis(self):
        city = self.cityChosen.get()
        region = self.regionChosen.get()
        position = self.keyword.get()
        location = city+'-'+region
        '''
        准备数据
        '''
        self.df = {'less than 2k': [], '2k~4k': [], '4k~6k': [], '6k~8k': [], '8k~10k': [], '10k~12k': [], '12k~14k': [],
                   '14k~16k': [], '16k~18k': [], '18k~20k': [], '20k~22k': [], '22k~24k': [], 'more than 24k': []}
        salary_rank = ['less than 2k', '2k~4k', '4k~6k', '6k~8k', '8k~10k', '10k~12k', '12k~14k', '14k~16k', '16k~18k',
                       '18k~20k', '20k~22k', '22k~24k', 'more than 24k']
        rank_number = []
        data = {}
        # 从数据库中查出数据
        if region == '不限':
            if position == '不限':
                items = self.session.execute("select salary from dao.recruit_information where location like '{0}%'".format(city))
            else:
                items = self.session.execute("select salary from dao.recruit_information where  keyword = '{0}'"
                                             " and location like '{1}%'".format(position, city))
        elif position == '不限':
            items = self.session.execute("select salary from dao.recruit_information where location = '{0}'".format(location))
        else:
            items = self.session.execute("select salary from dao.recruit_information where location = '{0}' and "
                                         "keyword = '{1}'".format(location, position))

        for item in items:
            if item[0] <= 2000:
                self.df['less than 2k'].append(item[0])
            elif item[0] <= 4000:
                self.df['2k~4k'].append(item[0])
            elif item[0] <= 6000:
                self.df['4k~6k'].append(item[0])
            elif item[0] <= 8000:
                self.df['6k~8k'].append(item[0])
            elif item[0] <= 10000:
                self.df['8k~10k'].append(item[0])
            elif item[0] <= 12000:
                self.df['10k~12k'].append(item[0])
            elif item[0] <= 14000:
                self.df['12k~14k'].append(item[0])
            elif item[0] <= 16000:
                self.df['14k~16k'].append(item[0])
            elif item[0] <= 18000:
                self.df['16k~18k'].append(item[0])
            elif item[0] <= 20000:
                self.df['18k~20k'].append(item[0])
            elif item[0] <= 22000:
                self.df['20k~22k'].append(item[0])
            elif item[0] <= 24000:
                self.df['22k~24k'].append(item[0])
            else:
                self.df['more than 24k'].append(item[0])
        self.df['less than 2k'] = len(self.df['less than 2k'])
        self.df['2k~4k'] = len(self.df['2k~4k'])
        self.df['4k~6k'] = len(self.df['4k~6k'])
        self.df['6k~8k'] = len(self.df['6k~8k'])
        self.df['8k~10k'] = len(self.df['8k~10k'])
        self.df['10k~12k'] = len(self.df['10k~12k'])
        self.df['12k~14k'] = len(self.df['12k~14k'])
        self.df['14k~16k'] = len(self.df['14k~16k'])
        self.df['16k~18k'] = len(self.df['16k~18k'])
        self.df['18k~20k'] = len(self.df['18k~20k'])
        self.df['20k~22k'] = len(self.df['20k~22k'])
        self.df['22k~24k'] = len(self.df['22k~24k'])
        self.df['more than 24k'] = len(self.df['more than 24k'])

        rank_number.append(self.df['less than 2k'])
        rank_number.append(self.df['2k~4k'])
        rank_number.append(self.df['4k~6k'])
        rank_number.append(self.df['6k~8k'])
        rank_number.append(self.df['8k~10k'])
        rank_number.append(self.df['10k~12k'])
        rank_number.append(self.df['12k~14k'])
        rank_number.append(self.df['14k~16k'])
        rank_number.append(self.df['16k~18k'])
        rank_number.append(self.df['18k~20k'])
        rank_number.append(self.df['20k~22k'])
        rank_number.append(self.df['22k~24k'])
        rank_number.append(self.df['more than 24k'])
        data['Salary Rank'] = salary_rank
        data['Number'] = rank_number
        # print(self.df)
        data = pd.DataFrame(data)
        # time.sleep(0.5)
        self.my_bar_seaborn(data)
        # self.draw_bar(data['rank'], data['number'])

    def draw_bar(self, labels, quants):
        width = 0.4
        ind = np.linspace(0.5, 9.5, 10)
        # make a square figure
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        # Bar Plot
        ax.bar(labels, quants, width, color='green')
        # Set the ticks on x-axis
        ax.set_xticks(ind)
        ax.set_xticklabels(labels)
        # labels
        ax.set_xlabel('Salary Rank')
        ax.set_ylabel('Number')
        # title
        ax.set_title('Salary Analysis', bbox={'facecolor': '0.8', 'pad': 5})
        plt.grid(True)
        plt.show()
        plt.close()

    def my_bar_seaborn(self, data):
        sns.set_style("whitegrid")
        ax = sns.barplot(x='Salary Rank', y='Number', data=data, ci=0)
        ax.set_title('Salary Analysis', bbox={'facecolor': '0.8', 'pad': 5})
        plt.show()
