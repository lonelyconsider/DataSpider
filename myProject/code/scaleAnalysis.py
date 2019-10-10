# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sqlEngine as se
from sqlalchemy.orm import sessionmaker
import pandas as pd
import seaborn as sns


class ScaleAnalysis(object):
    def __init__(self):
        # 从数据库提数据出来
        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()
        self.items = self.session.execute('select scale from dao.recruit_information')
        self.data = {}
        self.scale = []
        for item in self.items:
            temp = item[0]
            if temp == '20人以下':
                temp = '<20'
            if temp == '保密':
                temp = 'unknown'
            if temp == '10000人以上':
                temp = '>10000'
            if temp == '1000-9999人':
                temp = '1000-9999'
            if temp == '100-499人':
                temp = '100-499'
            if temp == '20-99人':
                temp = '20-99'
            if temp == '500-999人':
                temp = '500-999'
            self.scale.append(temp)
        self.data['Scale'] = self.scale

        # 最终数据源
        self.data = pd.DataFrame(self.data)

        # 绘制折线图
        self.myLineChart(self.data)

    # 要求传入一个DataFrame
    def myLineChart(self, data):
        sns.set_style("whitegrid")
        var = data.groupby('Scale').Scale.count()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('Enterprise Scale')
        ax.set_ylabel('Number Of Position')
        ax.set_title('Enterprise Sales Analysis')
        var.plot(kind='line')
        plt.show()


# if __name__ == '__main__':
# ScaleAnalysis()