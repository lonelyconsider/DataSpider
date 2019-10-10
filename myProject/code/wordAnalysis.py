# -*- coding:utf-8 -*-
# 分析平均薪资水平

import tkinter
import numpy
import jieba
import pandas as pd
import matplotlib.pyplot as plt
import sqlEngine as se
from tkinter import *
from sqlalchemy.orm import sessionmaker
from tkinter import ttk
from imageio import imread
from wordcloud import WordCloud, ImageColorGenerator


class WordAnalysis(object):
    def __init__(self):
        self.df = {}
        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()

        self.list = ['不限']
        self.root = tkinter.Tk()
        self.root.title('任职要求关键词分析')
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
        self.cityChosen['values'] = ('上海', '北京', '广州', '深圳', '杭州', '苏州', '南京', '合肥', '成都', '厦门', '西安')
        self.cityChosen.current(0)
        self.cityChosen.bind('<<ComboboxSelected>>', self.change)
        self.regionChosen = ttk.Combobox(self.root, width=13, state='readonly')
        self.regionChosen['values'] = ('不限', '嘉定', '杨浦', '浦东新区', '青浦', '黄浦', '闸北', '崇明县', '静安', '虹口',
                                       '长宁', '普陀', '闵行', '徐汇', '金山', '宝山', '松江', '奉贤')
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
        location = city + '-' + region
        data = ''
        # 从数据库中查出数据
        if region == '不限':
            if position == '不限':
                items = self.session.execute(
                    "select distinct job_requirement from dao.recruit_information where location like '{0}%'".format(city))
            else:
                items = self.session.execute("select distinct job_requirement from dao.recruit_information where  "
                                             "keyword = '{0}' and location like '{1}%'".format(position, city))
        elif position == '不限':
            items = self.session.execute(
                "select distinct job_requirement from dao.recruit_information where location = '{0}'".format(location))
        else:
            items = self.session.execute("select distinct job_requirement from dao.recruit_information where location "
                                         "= '{0}' and keyword = '{1}'".format(location, position))

        for item in items:
            item = item[0]
            content = self.read_txt_file(str(item))
            data = data + content
        # 返回一个list
        mytext_list = []
        segment = jieba.lcut(data)
        for i in segment:
            if len(i) < 3:
                mytext_list.append(i)
            else:
                continue
        words_df = pd.DataFrame({'segment': mytext_list})

        stopwords = pd.read_csv("F:\Graduation Project\myProject\stopwords\stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf-8')
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

        words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
        words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

        # 设置词云属性
        color_mask = imread('F:\Graduation Project\myProject\image\\background.jfif')
        wordcloud = WordCloud(font_path="simhei.ttf",   # 设置字体可以显示中文
                              background_color="white",       # 背景颜色
                              max_words=100,                  # 词云显示的最大词数
                              mask=color_mask,                # 设置背景图片
                              max_font_size=100,              # 字体最大值
                              random_state=42,
                              width=1000, height=860, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,
                              )                                  # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离

        # 生成词云, 可以用generate输入全部文本,也可以我们计算好词频后使用generate_from_frequencies函数
        word_frequence = {x[0]:x[1]for x in words_stat.head(100).values}
        word_frequence_dict = {}
        for key in word_frequence:
            word_frequence_dict[key] = word_frequence[key]

        wordcloud.generate_from_frequencies(word_frequence_dict)
        # # 从背景图片生成颜色值
        image_colors = ImageColorGenerator(color_mask)
        # # 重新上色
        wordcloud.recolor(color_func=image_colors)
        # # 保存图片
        wordcloud.to_file('F:\Graduation Project\myProject\\result image\output{0}.png'.format(str(numpy.random.random())))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        self.root.update()

    def read_txt_file(self, path):
        '''
        读取txt文本
        '''
        with open(path, 'r', encoding='gb18030', newline='') as f:
            return f.read()


if __name__ == '__main__':
    w = WordAnalysis()
    w.root.mainloop()
