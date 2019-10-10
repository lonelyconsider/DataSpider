# -*- coding:utf-8 -*-
import tkinter
import uuid
import login
import sqlEngine as se # 自定义
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlalchemy.orm import sessionmaker


class Sign(object):
    def __init__(self):
        # calculator
        self.i = 0

        self.si = tkinter.Tk()
        # self.si.wm_attributes("-topmost", 1)
        self.si.title('注册')
        self.si.resizable(0, 0)

        # window size and center
        self.window_width = 450
        self.window_height = 500
        self.screen_height = self.si.winfo_screenheight()
        self.screen_width = self.si.winfo_screenwidth()
        self.x = (self.screen_width - self.window_width) / 2 + 200
        self.y = (self.screen_height - self.window_height) / 2
        self.si.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, self.x, self.y))

        self.f = Frame(self.si)
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black")
        # title_label
        self.lp_title = ttk.Label(self.f, text='用户注册', font=("微软雅黑", 22), style="BW.TLabel")

        # insert user name
        self.lp_user_name = ttk.Label(self.f, text='用 户 名：', font=('黑体', 12))
        self.user_name = ttk.Entry(self.f, width=20, font=('黑体', 12))

        # insert password
        self.lp_password = ttk.Label(self.f, text='密    码：', font=('黑体', 12))
        self.password = ttk.Entry(self.f, width=20, show='●', font=('黑体', 12))

        # check password
        self.lp_check_password = ttk.Label(self.f, text='确认密码：', font=('黑体', 12))
        self.check_password = ttk.Entry(self.f, width=20, show='●', font=('黑体', 12))

        # E mail,for find back password function
        self.lp_e_mail = ttk.Label(self.f, text='邮    箱：', font=('黑体', 12))
        self.e_mail = ttk.Entry(self.f, width=20, font=('黑体', 12))

        # the button of sign in
        self.b_sign_in = ttk.Button(self.f, text='注册', width=10, command=self.sign_in)

        # 放置标签
        self.lp_title.grid(column=0, row=0, sticky=NW, padx=168, pady=60)
        self.lp_user_name.grid(column=0, row=1, sticky=NW, padx=95, pady=0)
        self.lp_password.grid(column=0, row=2, sticky=NW, padx=95, pady=15)
        self.lp_check_password.grid(column=0, row=3, sticky=NW, padx=95, pady=10)
        self.lp_e_mail.grid(column=0, row=4, sticky=NW, padx=95, pady=10)

        # 放置文本框
        self.user_name.grid(column=0, row=1, sticky=NW, padx=180, pady=0)
        self.password.grid(column=0, row=2, sticky=NW, padx=180, pady=15)
        self.check_password.grid(column=0, row=3, sticky=NW, padx=180, pady=10)
        self.e_mail.grid(column=0, row=4, sticky=NW, padx=180, pady=10)

        # 放置按钮
        self.b_sign_in.grid(column=0, row=5, sticky=NW, padx=180, pady=40)

        # 放置框架
        self.f.grid(column=0, row=0, sticky=NW)

    def sign_in(self):
        # 获取输入的值 v代表value
        v_user_name = self.user_name.get()
        v_password = self.password.get()
        v_check_password = self.check_password.get()
        v_e_mail = self.e_mail.get()

        # 提示
        if v_user_name == '':
            msg_u = '用户名不为空！\n'
        else:
            msg_u = ''
            self.i += 1
        if v_password == '':
            msg_p = '密码不为空！\n'
        else:
            msg_p = ''
            self.i += 1
        if v_check_password == '':
            msg_cp = '确认密码不为空！\n'
        else:
            msg_cp = ''
            self.i += 1
        if v_e_mail == '':
            msg_e = '邮箱不为空!\n'
        else:
            msg_e = ''
            self.i += 1
        if v_password != '' and v_check_password != '' and v_password != v_check_password:
            msg_ck = '确认密码输入有误！'
        else:
            msg_ck = ''
            self.i += 1

        if self.i == 5:
            # 条件控制
            con = False
            # 创建会话
            engine = se.sql_engine()
            sess = sessionmaker(bind=engine)
            session = sess()
            # 读取用户信息表
            names = session.execute('select user_name from dao.user_information')
            for name in names:
                name = name[0]
                if v_user_name == name:
                    con = True
                    break
                else:
                    continue
            if con:
                 showinfo(title='提示', message='用户已存在！')
            else:
                # 将用户信息存入数据库
                try:
                    user_id = uuid.uuid1()
                    session.execute("insert into dao.user_information (user_name,password,e_mail,user_id) values "
                                    "('{0}','{1}','{2}','{3}')".format(v_user_name, v_password, v_e_mail, user_id))
                    session.commit()
                    showinfo(title='提示', message='注册成功！')
                    self.i = 0
                    self.si.destroy()
                except:
                    showinfo(title='提示', message='输入格式有误！')
                    self.si.update()
                    self.i = 0
            self.i = 0
        else:
            showinfo(title='提示', message=msg_u+msg_p+msg_cp+msg_e+msg_ck)
            self.i = 0


