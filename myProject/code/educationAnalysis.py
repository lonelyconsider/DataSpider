import matplotlib.pyplot as plt
import sqlEngine as se
from sqlalchemy.orm import sessionmaker
import pandas as pd
import seaborn as sns


class EducationAnalysis(object):
    def __init__(self):
        # 从数据库提数据出来
        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()
        self.items = self.session.execute('select education from dao.recruit_information')
        self.data = {}
        self.education_list = ['不限', '高中', '中专', '大专', '本科']
        self.number_list = []
        self.education = {'不限': [], '高中': [], '中专': [], '大专': [], '本科': []}
        for item in self.items:
            if item[0] == '不限':
                self.education['不限'].append(item[0])
            if item[0] == '高中':
                self.education['高中'].append(item[0])
            if item[0] == '中专':
                self.education['中专'].append(item[0])
            if item[0] == '大专':
                self.education['大专'].append(item[0])
            if item[0] == '本科':
                self.education['本科'].append(item[0])
            else:
                continue
        self.number_list.append(len(self.education['不限']))
        self.number_list.append(len(self.education['高中']))
        self.number_list.append(len(self.education['中专']))
        self.number_list.append(len(self.education['大专']))
        self.number_list.append(len(self.education['本科']))

        self.data['学历'] = self.education_list
        self.data['数目'] = self.number_list
        # 最终数据源
        self.data = pd.DataFrame(self.data)
        # 绘制饼图
        self.myPie(self.data)

    # 要求传入一个DataFrame
    def myPie(self, data):
        sns.set_style("whitegrid")
        labels = 'unlimited', 'senior', 'technical secondary', 'junior college', 'regular college'
        fracs = data['数目']
        explode = [0, 0, 0, 0, 0.05]
        plt.axes(aspect=1)  # 设置这个图形就是圆的，否则就是椭圆
        plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
                shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                )
        plt.title('Education Background Analysis', fontsize=30, verticalalignment='bottom')
        # plt.style.use("ggplot")
        plt.show()


# if __name__ == '__main__':
#     EducationAnalysis()