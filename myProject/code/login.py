# -*- coding:utf-8 -*-
import tkinter
import sqlEngine as se  # u-d meaning user-defined
import mainPage  # u-d
import signUp  # u-d
import forgetPassword  # u-d
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from PIL import Image, ImageTk
from sqlalchemy.orm import sessionmaker
# @Login
# create on 2018/5/19
# by leslie


class Login(object):
    # create login object
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('登录界面')
        self.root.resizable(0, 0)

        # window size and center
        self.window_width = 900
        self.window_height = 380
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.x = (self.screen_width - self.window_width) / 2
        self.y = (self.screen_height - self.window_height) / 2
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, self.x, self.y))

        # make a frame
        self.f1 = Frame(self.root)

        # insert image
        self.canvas = Canvas(self.root, width=500, height=350)
        # self.path = str(os.path.abspath(""))
        self.im = Image.open('..\image\dog_login.jpg')
        self.img = ImageTk.PhotoImage(self.im)
        self.image = self.canvas.create_image(0, 5, image=self.img, anchor='nw')

        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="white")

        # add label_title JDog Data Get
        self.lp_title = ttk.Label(self.f1, text='招聘信息的采集与分析', font=("微软雅黑", 18), style="BW.TLabel")

        # add copyright_label
        self.copyright_label = ttk.Label(self.root, text='Leslie@copyright', font=('幼圆', 12))

        # insert user name
        self.r1 = ttk.Label(self.f1, text='用户名', font=('微软雅黑', 13))
        self.user_name = ttk.Entry(self.f1, width=20, font=('微软雅黑', 13))

        # insert password
        self.r2 = ttk.Label(self.f1, text='密码', font=('微软雅黑', 13))
        self.password = ttk.Entry(self.f1, width=20, show='●', font=('微软雅黑', 13))

        self.style.configure("BW.TLabel", foreground="black", font=('微软雅黑', 10), bd=0)
        # register label
        self.register = ttk.Button(self.f1, text='注册账号', style="BW.TLabel", command=self.sign_up)

        # forget password
        self.forget = ttk.Button(self.f1, text='忘记密码', style="BW.TLabel", command=self.forget_password)

        # login in
        self.login = ttk.Button(self.f1, text='登录', width=10, command=self.login_in)

        # ...
        self.initUi()

    # create ui
    def initUi(self):
        self.canvas.grid(column=0, row=0, sticky=N)
        self.lp_title.grid(column=0, row=0, sticky=NW, padx=70, pady=70)
        self.r1.grid(column=0, row=0, sticky=NW, padx=60, pady=160)
        self.user_name.grid(column=0, row=0, sticky=NW, padx=130, pady=160)
        self.r2.grid(column=0, row=0, sticky=NW,padx=60, pady=215)
        self.password.grid(column=0, row=0, sticky=NW, padx=130, pady=215)
        self.register.grid(column=0, row=0, sticky=NW, padx=150, pady=255)
        self.forget.grid(column=0, row=0, sticky=NW, padx=260, pady=255)
        self.login.grid(column=0, row=0, sticky=NW, padx=150, pady=320)
        self.copyright_label.grid(column=0, row=0, sticky=SW, padx=5, pady=355)
        self.f1.grid(column=1, row=0, sticky=N, padx=5, pady=0)
        self.root.mainloop()

    # main page
    def login_in(self):
        # 获取输入的用户信息
        user_name = self.user_name.get()
        password = self.password.get()

        # 获取用户表信息
        engine = se.sql_engine()
        sess = sessionmaker(bind=engine)
        session = sess()
        info = session.execute('select user_name,password from dao.user_information')

        # 临时变量
        x = True

        for i in info:
            if user_name == i[0] and password == i[1]:
                # 登陆成功
                showinfo(title='登陆成功', message='欢迎进入招聘信息的采集与分析系统！')
                x = False
                break
        if x:
            showinfo(title='登录失败', message='请核对你的用户名和密码！')
        else:
            self.root.destroy()
            mainPage.MainPage()

    # sign up
    def sign_up(self):
        signUp.Sign()
        self.root.update()

    # find back the password by e mail
    def forget_password(self):
        forgetPassword.ForgetPassword()
        self.root.update()


if __name__ == '__main__':
    Login()
