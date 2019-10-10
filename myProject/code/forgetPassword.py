# -*- coding:utf-8 -*-
import tkinter
import sqlEngine as se # u-d
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlalchemy.orm import sessionmaker


class ForgetPassword(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('重置密码')
        self.root.resizable(0, 0)

        # window size and center
        self.window_width = 450
        self.window_height = 300
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.x = (self.screen_width - self.window_width) / 2 + 200
        self.y = (self.screen_height - self.window_height) / 2
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, self.x, self.y))

        # label
        self.lp_user_name = ttk.Label(self.root, text='用 户 名：', font=('黑体', 12))
        self.lp_e_mail = ttk.Label(self.root, text='邮    箱：', font=('黑体', 12))
        self.lp_new_password = ttk.Label(self.root, text='新 密 码：', font=('黑体', 12))
        self.lp_check_password = ttk.Label(self.root, text='确认密码：', font=('黑体', 12))

        # entry
        self.user_name = ttk.Entry(self.root, width=20, font=('黑体', 12))
        self.e_mail = ttk.Entry(self.root, width=20, font=('黑体', 12))
        self.new_password = ttk.Entry(self.root, width=20, font=('黑体', 12), show='●')
        self.check_password = ttk.Entry(self.root, width=20, font=('黑体', 12), show='●')

        # button
        self.b_reset = ttk.Button(self.root, text='确认修改', width=10,command=self.forget_password)

        # layout manager
        self.lp_user_name.grid(column=0, row=0, sticky=NW, padx=90, pady=40)
        self.lp_e_mail.grid(column=0, row=0, sticky=NW, padx=90, pady=80)
        self.lp_new_password.grid(column=0, row=0, sticky=NW, padx=90, pady=120)
        self.lp_check_password.grid(column=0, row=0, sticky=NW, padx=90, pady=160)
        #
        self.user_name.grid(column=0,row=0,sticky=NW, padx=180, pady=40)
        self.e_mail.grid(column=0,row=0,sticky=NW, padx=180, pady=80)
        self.new_password.grid(column=0,row=0,sticky=NW, padx=180, pady=120)
        self.check_password.grid(column=0,row=0,sticky=NW, padx=180, pady=160)

        self.b_reset.grid(column=0,row=0,sticky=NW,padx=180,pady=240)

    def forget_password(self):
        # 获取输入的值 v代表value
        v_user_name = self.user_name.get()
        v_e_mail = self.e_mail.get()
        v_new_password = self.new_password.get()
        v_check_password = self.check_password.get()

        # 创建session对象
        engine = se.sql_engine()
        sess = sessionmaker(bind=engine)
        session = sess()

        if v_user_name != '' and v_e_mail != '' and v_new_password != '' and v_check_password != '':
            # 检查用户名与邮箱是否匹配
            emails = session.execute("select e_mail from dao.user_information where user_name='{0}'".format(v_user_name))
            if v_e_mail == emails.first()[0]:
                if v_new_password == v_check_password:
                    session.execute("update dao.user_information set password = '{0}' where user_name = '{1}'".format(v_new_password,v_user_name))
                    session.commit()
                    showinfo(title='提示', message='密码重置成功！')
                    self.root.destroy()
            else:
                showinfo(title='提示', message='信息输入有误！')
        else:
            showinfo(title='提示', message='请确认你的信息完整！')

