# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from tkinter import ttk
import re
import csv
import requests
import uuid
import sqlEngine as se
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from sqlalchemy.orm import sessionmaker
from tkinter.messagebox import *


class Spider(object):
    def __init__(self):
        self.df = [[]]
        self.timeCode = uuid.uuid1()
        self.engine = se.sql_engine()
        self.sess = sessionmaker(bind=self.engine)
        self.session = self.sess()

        self.list = ['不限']
        self.root = tkinter.Tk()
        self.root.title('启动程序')
        self.root.resizable(0, 0)

        # window size and center
        self.window_width = 600
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
        self.lp_keyword = ttk.Label(self.root, text='关键字:')
        self.lp_pages = ttk.Label(self.root, text='页数:')
        # 文本框
        self.keyword = ttk.Entry(self.root, width=12)
        self.pages = ttk.Entry(self.root, width=12)

        self.number = StringVar()
        self.cityChosen = ttk.Combobox(self.root, textvariable=self.number, width=10, state='readonly')
        self.cityChosen['values'] = ('北京', '上海', '广州', '深圳', '天津', '武汉', '西安', '成都', '大连', '长春', '沈阳', '南京',
                                     '济南', '青岛', '杭州', '苏州', '无锡', '宁波', '重庆', '郑州', '长沙', '福州', '厦门', '哈尔滨',
                                     '石家庄', '合肥', '惠州', '马鞍山')
        self.cityChosen.current(0)
        self.cityChosen.bind('<<ComboboxSelected>>', self.change)

        self.regionChosen = ttk.Combobox(self.root, width=10, state='readonly')
        # self.regionChosen['values'] = ('不限', '嘉定', '杨浦', '浦东新区', '青浦', '黄浦', '闸北', '崇明县', '静安', '虹口', '长宁', '普陀', '闵行', '徐汇', '金山', '宝山', '松江', '奉贤')
        # self.regionChosen.current(0)

        self.now_info = Listbox(self.root, width=58, height=3, selectmode=SINGLE)
        self.start = ttk.Button(self.root, width=10, text='开始采集', command=self.start_spider)
        '''
        布置控件
        '''
        self.lp_city.grid(column=0, row=0, sticky=NW, padx=100, pady=12)
        self.lp_region.grid(column=0, row=0, sticky=NW, padx=310, pady=12)
        self.lp_keyword.grid(column=0, row=1, sticky=NW, padx=100, pady=12)
        self.lp_pages.grid(column=0, row=1, sticky=NW, padx=310, pady=12)

        #
        self.cityChosen.grid(column=0, row=0, sticky=NW, padx=170, pady=10)
        self.regionChosen.grid(column=0, row=0, sticky=NW, padx=380, pady=10)
        self.keyword.grid(column=0, row=1, sticky=NW, padx=170, pady=10)
        self.pages.grid(column=0, row=1, sticky=NW, padx=380, pady=10)

        #
        self.now_info.grid(column=0, row=2, sticky=NW, padx=90, pady=10)
        self.start.grid(column=0, row=3, sticky=NW, padx=250, pady=10)

    def change(self, event):
        region = self.session.execute("select region from dao.region_information where city = '{0}'".format(self.cityChosen.get()))
        for i in region:
            self.list.append(i[0])
        self.regionChosen['values'] = tuple(self.list)
        self.regionChosen.update()
        self.root.update()
        self.list = ['不限']

    def start_spider(self):
        v_city = self.cityChosen.get()
        regionCode = 0
        region = ''
        sg = ''

        if self.regionChosen.get() == '不限':
            regionCode = ''
        else:
            region = self.regionChosen.get()
            items = self.session.execute("select region_code from dao.region_information where region = '{0}'".format(self.regionChosen.get()))
            for i in items:
                regionCode = i[0]
        keyword = self.keyword.get()
        if self.pages.get() == '':
            showinfo(title='提示', message='请填写页数!')
        else:
            pages = int(self.pages.get())+1
            self.main(v_city, keyword, regionCode, pages, sg, region, self.timeCode)
            self.root.destroy()

    def get_one_page(self, city, keyword, region, page, sg):

        # 获取网页html内容并返回

        paras = {
            'jl': city,  # 搜索城市
            'kw': keyword,  # 搜索关键词
            # 'fl': 530,
            'isadv': 0,  # 是否打开更详细搜索选项
            'isfilter': 1,  # 是否对结果过滤
            'sm': 0,
            're': region,  # region的缩写，地区，2005代表海淀
            'sg': sg,
            'p': page  # 页数
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/63.0.3239.132 Safari/537.36',
            'Host': 'sou.zhaopin.com',
            'Referer': 'https://www.zhaopin.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'
        try:
            # 获取网页内容，返回html数据
            response = requests.get(url, params=paras, headers=headers)
            print(response.url)
            # 通过状态码判断是否获取成功
            if response.status_code == 200:
                return response.text
            return None
        except RequestException as e:
            return None

    def parse_one_page(self, html):
        # 解析HTML代码，提取有用信息并返回
        # 正则表达式进行解析
        pattern = re.compile('<td class="zwmc".*?href="(.*?)" target="_blank">(.*?)</a>.*?'  # 匹配职位详情地址和职位名称
                             '<td class="gsmc">.*? target="_blank">(.*?)</a>.*?'  # 匹配公司名称
                             '<td class="zwyx">(.*?)</td>', re.S)  # 匹配工作地点
        # 匹配所有符合条件的内容
        items = re.findall(pattern, html)
        for item in items:
            job_name = item[1]
            job_name = job_name.replace('<b>', '')
            job_name = job_name.replace('</b>', '')

            salary_average = 0
            temp = item[3]
            if temp != '面议':
                idx = temp.find('-')
                # 求平均工资
                try:
                    salary_average = (int(temp[0:idx]) + int(temp[idx + 1:])) // 2
                except:
                    salary_average = 0
            yield {
                'job': job_name,
                'job_url': item[0],
                'company': item[2],
                'salary': salary_average
            }

    # 获取工作地点
    def getLocation(self, html):
        items = re.findall(r'<td class="gzdd">(.*?)</td>', html)
        for item in items:
            location = ''
            location = item[0]
            yield {
                'location': location
            }

    # 获取动态sg
    def getSg(self, html):
        '''
        针对智联招聘的反爬虫设置的动态码，解决方法
        '''
        sg = ''
        # 正则表达式进行解析
        pattern = re.compile('<div class="pagesDown".*?sg=(.*?)&', re.S)

        # 匹配所有符合条件的内容
        items = re.findall(pattern, html)

        for item in items:
            sg = item
        return sg

    def get_detail_page(self, url):

        # 获取职位详情页html内容并返回

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Host': 'jobs.zhaopin.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        try:
            # 获取网页内容，返回html数据
            response = requests.get(url, headers=headers)
            # 通过状态码判断是否获取成功
            if response.status_code == 200:
                return response.text
            return None
        except RequestException as e:
            return None

    def get_job_detail(self, html):
        requirement = ''
        # 使用BeautifulSoup进行数据筛选
        soup = BeautifulSoup(html, 'html.parser')
        # 找到<ul class="terminal-ul clearfix">标签
        for ul in soup.find_all('ul', class_='terminal-ul clearfix'):
            # 该标签共有8个子标签，分别为：
            # 职位月薪|工作地点|发布日期|工作性质|工作经验|最低学历|招聘人数|职位类别
            lis = ul.find_all('strong')
            # 工作经验
            years = lis[4].get_text()
            # 最低学历
            education = lis[5].get_text()
        # 筛选任职要求
        for terminalpage in soup.find_all('div', class_='terminalpage-main clearfix'):
            for box in terminalpage.find_all('div', class_='tab-cont-box'):
                cont = box.find_all('div', class_='tab-inner-cont')[0]
                ps = cont.find_all('p')
                # "立即申请"按钮也是个p标签，将其排除
                for i in range(len(ps) - 1):
                    requirement += ps[i].get_text().replace("\n", "").strip()  # 去掉换行符和空格

        # 筛选公司规模，该标签内有四个或五个<li>标签，但是第一个就是公司规模
        scale = soup.find(class_='terminal-ul clearfix terminal-company mt20').find_all('li')[0].strong.get_text()
        return {'years': years, 'education': education, 'requirement': requirement, 'scale': scale}

    def write_txt_file(self, path, txt):
        '''
        写入txt文本
        '''
        with open(path, 'a', encoding='gb18030', newline='') as f:
            f.write(txt)

    def write_csv_file(self, path, headers, rows):
        '''
        将表头和行写入csv文件
        '''
        # 加入encoding防止中文写入报错
        # newline参数防止每写入一行都多一个空行
        with open(path, 'a', encoding='gb18030', newline='') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

    def write_csv_headers(self, path, headers):
        '''
        写入表头
        '''
        with open(path, 'a', encoding='gb18030', newline='') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()

    def write_csv_rows(self, path, headers, rows):
        '''
        写入行
        '''
        with open(path, 'a', encoding='gb18030', newline='') as f:
            f_csv = csv.DictWriter(f, headers)
            # 如果写入数据为字典，则写入一行，否则写入多行
            if type(rows) == type({}):
                f_csv.writerow(rows)
            else:
                f_csv.writerows(rows)

    def main(self, city, keyword, regionCode, pages, sg, region, time_code):
        # 主函数
        csv_filename = 'zl_' + city + '_' + region + '_' + keyword + '.csv'
        txt_filename = 'zl_' + city + '_' + region + '_' + keyword + '.txt'
        headers = ['job', 'years', 'education', 'salary', 'company', 'scale', 'job_url']
        salaries = []
        self.write_csv_headers(r'F:\Graduation Project\myProject\result file' + '\\' + csv_filename, headers)
        for i in range(1, pages):
            recordNumber = 0
            # 获取该页中所有职位信息，写入csv文件
            job_dict = {}
            # 返回一个response.text
            html = self.get_one_page(city, keyword, regionCode, i, sg)
            # 解析response.text,返回一个发生器
            try:
                items = self.parse_one_page(html)
            except:
                continue
            for item in items:
                # 获取详细信息，返回一个response.text
                try:
                    # item['job_url']是一个字符串
                    d_html_2 = self.get_detail_page(item['job_url'])
                    # 返回字典{'years': years, 'education': education, 'requirement': requirement, 'scale': scale}
                    job_detail = self.get_job_detail(d_html_2)
                    # 规模
                    job_dict['scale'] = job_detail.get('scale')
                    # 工作经验
                    job_dict['years'] = job_detail.get('years')
                    # 学历
                    job_dict['education'] = job_detail.get('education')
                    # 职位
                    job_dict['job'] = item.get('job')
                    # 薪水
                    job_dict['salary'] = item.get('salary')
                    # 公司名
                    job_dict['company'] = item.get('company')
                    # 详情页面链接
                    job_dict['job_url'] = item.get('job_url')

                    # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
                    pattern = re.compile(r'[一-龥]+')
                    filterdata = re.findall(pattern, job_detail.get('requirement'))

                    self.write_txt_file(r'F:\Graduation Project\myProject\result file' + '\\' + txt_filename,
                                   ''.join(filterdata))
                    self.write_csv_rows(r'F:\Graduation Project\myProject\result file' + '\\' + csv_filename, headers,
                                   job_dict)
                    # 将数据存入数据库
                    job = job_dict['job']
                    if len(job) > 200:
                        try:
                            job = re.findall(r'(.*?)&.*?', job)
                            job = job[0]
                        except:
                            continue
                    company = job_dict['company']
                    years = job_dict['years']
                    salary = job_dict['salary']
                    # location = list(job_dict['location'])
                    education = job_dict['education']
                    scale = job_dict['scale']
                    job_url = job_dict['job_url']
                    job_requirement = r'F:\Graduation Project\myProject\result file' + '\\' + txt_filename
                    if region == '不限':
                        location = city
                    else:
                        location = city + '-' + region
                    d_time_code = str(time_code)
                    sql = "insert into dao.recruit_information (job_name,company,experience,salary,location," \
                          "education,scale,job_url,keyword,job_requirement,time_code)" \
                          "values('{0}','{1}','{2}',{3},'{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(job, company,
                            years, salary, location, education,scale,job_url,keyword, job_requirement, d_time_code)
                    self.session.execute(sql)
                    self.session.commit()

                    # 显示进度
                    self.now_info.delete(0, END)
                    # 进度框显示第几页
                    self.now_info.insert(END, '第 {0} 页'.format(i))
                    # 构造记录
                    recordNumber += 1
                    recordNumberStr = 'No.'+str(recordNumber)+'  '
                    record = recordNumberStr + job + '     ' + company
                    self.now_info.insert(END, record)
                    self.now_info.insert(END, '请耐心等待！')
                    self.now_info.update()
                except:
                    continue

            # 获取动态码
            sg = self.getSg(html)
        showinfo(title='提示', message='数据爬取完毕！')
