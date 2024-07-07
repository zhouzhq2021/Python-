from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import socket
import json
import sys
import re
server_address = ('localhost', 5001)
class LoginPage(Tk):
    def __init__(self):
        super().__init__()
        self.__root()
        self.label_head = self.__label_head()
        self.input_accountID = self.__input_accountID()
        self.input_pwd = self.__input_pwd()
        self.label_accountID = self.__label_accountID()
        self.label_pwd = self.__label_pwd()
        self.button_login = self.__button_login()
        self.label_hint = self.__label_hint()
    def __root(self):
        self.title("足球赛事管理系统V1.0")
        # Set the window size and center
        width = 621
        height = 353
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
    def __label_head(self):
        label = Label(self, text="欢迎来到足球赛事管理系统！",
                      font=("Arial", 10, "bold"), anchor="center")
        label.place(x=70, y=30, width=482, height=37)
        return label
    def __input_accountID(self):
        global var_account_id
        var_account_id = StringVar()
        accountID = Entry(self, textvariable=var_account_id)
        accountID.place(x=266, y=150, width=221, height=31)
        return accountID
    def __input_pwd(self):
        global var_password
        var_password = StringVar()
        pwd = Entry(self, textvariable=var_password, show="*")
        pwd.place(x=266, y=220, width=221, height=31)
        return pwd
    def __label_accountID(self):
        label = Label(self, text="用户ID", anchor="center")
        label.place(x=132, y=150, width=87, height=31)
        return label
    def __label_pwd(self):
        label = Label(self, text="密码", anchor="center")
        label.place(x=132, y=220, width=87, height=31)
        return label
    def __button_login(self):
        btn = Button(self, text="登陆", command=self.log_in)
        btn.place(x=270, y=300, width=81, height=33)
        return btn
    def __label_hint(self):
        label = Label(self, text="请先登录", anchor="center")
        label.place(x=220, y=90, width=163, height=24)
        return label
    def log_in(self):
        account_id = var_account_id.get()  # Gets the id and password entered by the user
        pwd = var_password.get()
        if account_id == "" or pwd == "":
            tkinter.messagebox.showerror(title="注意",
                                         message='输入错误！')
            sock.send("false".encode())
        else:
            # Send login data to the server and receive data processed by the server.
            data = ["l", account_id, pwd]
            sock.send(json.dumps(data).encode())
            response = json.loads(sock.recv(1024))
            if response[0] == "null":  # If the user is not in the server's database, the user is guided to register.
                is_signup = tkinter.messagebox.askyesno(title="注册", message='您还没有注册, '
                                                                                      '请先注册')
                if is_signup:
                    self.sign_up()
                else:
                    pass
            elif response[0] == "false":
                tkinter.messagebox.showerror(title="注意", message='密码错误，请重试！')
                sock.send("false".encode())
            elif response[0] == "true":
                # If the user in the database is set as an administrator,
                # the administrator interface is entered; otherwise, the normal user interface is entered.
                if response[1] == 1:
                    tkinter.messagebox.showinfo(title='欢迎', message='Welcome:' + account_id)
                    self.quit()
                    self.destroy()
                    win = AdminInterface()
                    win.mainloop()
                else:
                    tkinter.messagebox.showinfo(title='欢迎', message='Welcome:' + account_id)
                    self.quit()
                    self.destroy()
                    win = MainInterface()
                    win.mainloop()
            else:
                pass
    # Generate a registration interface through the Toplevel component
    def sign_up(self):
        def loads_new_user():  # Design a function that interacts with the server to send the registration information
            ni = new_id.get()  # to the server to complete the registration
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            if np != npf:
                tkinter.messagebox.showerror(title="注意",
                                             message='账户或密码错误。')
                sock.send("false".encode())
            else:
                # The system requires the password length of the user registration to be 6 or greater
                if len(np) < 6:
                    tkinter.messagebox.showerror(title="注意",
                                                 message='密码太短了，密码不少于6个字符')
                    sock.send("false".encode())
                else:
                    # Send data to the server side and receive data back from the server.
                    data = ["s", ni, np]
                    sock.send(json.dumps(data).encode())
                    response = json.loads(sock.recv(1024))
                    if response[0] == "true":
                        tkinter.messagebox.showinfo('欢迎', '注册成功')
                        root_sign_up.destroy()
        # The newly generated interface is named root_sign_up,and displayed in the center of screen.
        root_sign_up = Toplevel(self)
        width = 500
        height = 350
        screenwidth = root_sign_up.winfo_screenwidth()
        screenheight = root_sign_up.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root_sign_up.geometry(geometry)
        root_sign_up.resizable(width=False, height=False)
        root_sign_up.title('注册')
        new_id = StringVar()
        Label(root_sign_up, text='用户ID').place(x=90, y=60, width=83, height=31)
        Entry(root_sign_up, textvariable=new_id).place(x=210, y=60, width=214, height=31)
        new_pwd = StringVar()
        Label(root_sign_up, text='密码').place(x=90, y=130, width=83, height=31)
        Entry(root_sign_up, textvariable=new_pwd, show='*').place(x=210, y=130, width=214, height=31)
        new_pwd_confirm = StringVar()
        Label(root_sign_up, text='确认密码').place(x=90, y=200, width=83, height=31)
        Entry(root_sign_up, textvariable=new_pwd_confirm, show='*').place(x=210, y=200, width=214, height=31)
        bt_sign_up = Button(root_sign_up, text='确认注册', command=loads_new_user)
        bt_sign_up.place(x=195, y=280, width=132, height=36)
class MainInterface(Tk):
    def __init__(self):
        super().__init__()
        self.__root()
        self.label_flag = self.__label_flag()
        self.label_hint = self.__label_hint()
        self.button_quit = self.__button_quit()
        self.button_show_all = self.__button_show_all()
        self.input_info = self.__input_info()
        self.button_query = self.__button_query()
        self.label_hint2 = self.__label_hint2()
        self.label_hint3 = self.__label_hint3()
    def __root(self):
        self.title("足球赛事管理系统V1.0")
        # Set the window size and center
        width = 581
        height = 340
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
    def __label_flag(self):
        label = Label(self, text="普通用户", font=("Arial", 10, "bold"), anchor="center")
        label.place(x=20, y=20, width=93, height=39)
        return label
    def __label_hint(self):
        label = Label(self, text="请输入你要查询的赛事的相关信息：",
                      font=("Arial", 10, "bold"), anchor="center")
        label.place(x=78, y=60, width=455, height=39)
        return label
    def __button_quit(self):
        btn = Button(self, text="退出系统", command=lambda: self.quit())
        btn.place(x=490, y=300, width=79, height=29)
        return btn
    def __button_show_all(self):
        btn = Button(self, text="显示全部", command=lambda: self.query_style(1, "show_all"))
        btn.place(x=370, y=240, width=82, height=43)
        return btn
    def __input_info(self):
        global var_info
        var_info = StringVar()
        info = Entry(self, textvariable=var_info)
        info.place(x=210, y=180, width=182, height=30)
        return info
    def __button_query(self):
        btn = Button(self, text="查询", command=lambda: self.query_style(0, var_info.get()))
        btn.place(x=150, y=240, width=82, height=43)
        return btn
    def __label_hint2(self):
        label = Label(self, text='点击 "显示全部" 获取所有比赛信息', anchor="center")
        label.place(x=150, y=140, width=293, height=24)
        return label
    def __label_hint3(self):
        label = Label(self, text='比如: "Argentina","November","2:1"', anchor='center')
        label.place(x=170, y=100, width=257, height=27)
        return label
    def query_style(self, flag, info):
        try:
            info = str(info)
            if bool(info):
                pat1 = "[0-9]+:[0-9]+"  # 根据比分进行查询，如2:1
                pat2 = "\D"  # 根据team名称或者月份进行查询，如November
                if re.search(pat1, info.strip()) or re.search(pat2, info.strip()) or info.isdigit():
                    sock.send(json.dumps(["q", flag, info]).encode())
                    # Concatenate long messages sent by the server
                    total_data = bytes()
                    while True:
                        data = sock.recv(1024)
                        total_data += data
                        if len(data) < 1024:
                            break
                    response = json.loads(total_data)
                    if not bool(response):
                        tkinter.messagebox.showerror(title="注意", message="无结果")
                    else:
                        # Sets the header field and header width
                        columns = {"ID": 38, "Date": 140, "Time": 58, "Team1": 90, "Points": 64, "Team2": 90,
                                   "Status": 77,
                                   "Penalty Kick": 80}
                        response_show = Toplevel(self)
                        response_show.title('结果')
                        width = 688
                        height = 380
                        screenwidth = response_show.winfo_screenwidth()
                        screenheight = response_show.winfo_screenheight()
                        geometry = '%dx%d+%d+%d' % (
                            width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                        response_show.geometry(geometry)
                        # Initialize the table:Table is based on Treeview, tkinter itself does not have a table.
                        tk_table = Treeview(response_show, show="headings", columns=list(columns))
                        for text, width in columns.items():
                            tk_table.heading(text, text=text, anchor='center')
                            tk_table.column(text, anchor='center', width=width,
                                            stretch=False)  # No automatic stretching
                        tk_table.place(x=20, y=40, width=651, height=313)
                        vbar = Scrollbar(tk_table)
                        tk_table.configure(yscrollcommand=vbar.set)
                        vbar.config(command=tk_table.yview)
                        vbar.place(x=656, y=40, width=15, height=313)
                        # 对查询信息进行导入
                        for i in response:
                            tk_table.insert("", "end", values=tuple(i))
                else:
                    tkinter.messagebox.showerror(title="注意", message="无效输入，请检查你的输入信息")
                    sock.send("false".encode())
            else:
                tkinter.messagebox.showerror(title="注意", message="无效输入，请检查你的输入信息")
                sock.send("false".encode())
        except EXCEPTION:
            tkinter.messagebox.showerror(title="注意", message="错误！请重启系统")
class AdminInterface(Tk):
    def __init__(self):
        super().__init__()
        self.__root()
        self.label_flag = self.__label_flag()
        self.button_quit = self.__button_quit()
        self.input_info = self.__input_info()
        self.label_info = self.__label_info()
        self.button_query = self.__button_query()
        self.table_show_race = self.__table_show_race()
        self.button_delete = self.__button_delete()
        self.button_add = self.__button_add()
        self.button_modify = self.__button_modify()
    def __root(self):
        self.title("足球赛事管理系统")
        # Set the window size and center
        width = 688
        height = 409
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
    def __label_flag(self):
        label = Label(self, text="管理员", font=("Arial", 10, "bold"), anchor="center")
        label.place(x=20, y=20, width=91, height=31)
        return label
    def __button_quit(self):
        btn = Button(self, text="退出系统", command=lambda: self.quit())
        btn.place(x=600, y=370, width=80, height=33)
        return btn
    def __input_info(self):
        global var_info2
        var_info2 = StringVar()
        info2 = Entry(self, textvariable=var_info2)
        info2.place(x=330, y=40, width=159, height=24)
        return info2
    def __label_info(self):
        label = Label(self, text="关键词查询:", font=("Arial", 10, "bold"), anchor="center")
        label.place(x=150, y=40, width=147, height=24)
        return label
    def __button_query(self):
        btn = Button(self, text="查询", command=lambda: self.query_style(var_info2.get()))
        btn.place(x=530, y=40, width=53, height=26)
        return btn
    def __table_show_race(self):
        # Sets the header field and header width
        columns = {"ID": 38, "Date": 140, "Time": 58, "Team1": 90, "Points": 64, "Team2": 90, "Status": 77,
                   "Penalty Kick": 80}
        # Initialize the table:Table is based on Treeview, tkinter itself does not have a table.
        tk_table = Treeview(self, show="headings", columns=list(columns))
        for text, width in columns.items():
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # No automatic stretching
        tk_table.place(x=20, y=90, width=648, height=239)
        vbar = Scrollbar(self)
        tk_table.configure(yscrollcommand=vbar.set)
        vbar.config(command=tk_table.yview)
        vbar.place(x=653, y=90, width=15, height=239)
        data = schedule_print()  # Call schedule_print() to get all the matches in the database
        for i in data:
            tk_table.insert("", "end", values=i)
        return tk_table
    def __button_delete(self):
        btn = Button(self, text="删除", command=lambda: self.modify_style(["d"]))
        btn.place(x=130, y=350, width=54, height=34)
        return btn
    def __button_add(self):
        btn = Button(self, text="添加", command=lambda: self.modify_style(["a"]))
        btn.place(x=290, y=350, width=54, height=34)
        return btn
    def __button_modify(self):
        btn = Button(self, text="修改", command=lambda: self.modify_style(["m"]))
        btn.place(x=450, y=350, width=54, height=34)
        return btn
    def modify_style(self, info):
        oper = info[0]
        try:
            if oper == "d":
                def delete_race():
                    di = delete_id.get()
                    if bool(di) and di.isdigit():
                        sock.send(json.dumps(["m", "d", int(di)]).encode())
                        response = json.loads(sock.recv(1024))
                        if response[0] == "true":
                            tkinter.messagebox.showinfo(title="注意",
                                                        message='成功！重新启动系统即可看到更新的信息。')
                            root_delete.destroy()
                            sock.send("false".encode())
                        elif response[0] == "false":
                            tkinter.messagebox.showerror(title="注意",
                                                         message="您输入的比赛 ID 不存在，无法删除。")
                            sock.send("false".encode())
                    else:
                        tkinter.messagebox.showerror(title="注意",
                                                     message='无结果，请检测你的输入。')
                        sock.send("false".encode())

                root_delete = Toplevel(self)
                width = 400
                height = 200
                screenwidth = root_delete.winfo_screenwidth()
                screenheight = root_delete.winfo_screenheight()
                geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                root_delete.geometry(geometry)
                root_delete.resizable(width=False, height=False)
                root_delete.title('Delete')
                delete_id = StringVar()
                label1 = Label(root_delete, text='请输入您要删除的比赛的 ID 编号：',
                               anchor="center")
                label1.place(x=30, y=20, width=357, height=32)
                entry1 = Entry(root_delete, textvariable=delete_id)
                entry1.place(x=90, y=80, width=228, height=30)

                bt_delete = Button(root_delete, text='确认删除', command=delete_race)
                bt_delete.place(x=145, y=150, width=100, height=32)
            elif oper == "a":
                def add_race():
                    month = var_input1.get()
                    day = var_input2.get()
                    time = var_input3.get()
                    team1 = var_input4.get()
                    score1 = var_input5.get()
                    score2 = var_input6.get()
                    team2 = var_input7.get()
                    status = var_input8.get()
                    penalty_kick = var_input9.get()
                    # 与服务器进行数据交互
                    data = [month, int(day), time, team1, int(score1), int(score2), team2, status, penalty_kick]
                    sock.send(json.dumps(["m", "a", data]).encode())
                    total_data = bytes()
                    while True:
                        data = sock.recv(1024)
                        total_data += data
                        if len(data) < 1024:
                            break
                    response = json.loads(total_data)
                    if response[0] == "true":
                        tkinter.messagebox.showinfo(title="注意",
                                                    message='成功！重新启动系统即可看到更新的信息。')
                        sock.send("false".encode())
                        root_add.destroy()
                    elif response[0] == "false":
                        tkinter.messagebox.showerror(title="注意", message=response[1])
                        sock.send("false".encode())
                root_add = Toplevel(self)
                width = 440
                height = 408
                screenwidth = root_add.winfo_screenwidth()
                screenheight = root_add.winfo_screenheight()
                geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                root_add.geometry(geometry)
                root_add.resizable(width=False, height=False)
                root_add.title = "Add"
                var_input1 = StringVar()
                var_input2 = StringVar()
                var_input3 = StringVar()
                var_input4 = StringVar()
                var_input5 = StringVar()
                var_input6 = StringVar()
                var_input7 = StringVar()
                var_input8 = StringVar()
                var_input9 = StringVar()
                label1 = Label(root_add, text="Month", anchor="center")
                label1.place(x=70, y=30, width=64, height=30)
                ipt1 = Entry(root_add, textvariable=var_input1)
                ipt1.place(x=170, y=30, width=158, height=30)
                label2 = Label(root_add, text="Day", anchor="center")
                label2.place(x=70, y=70, width=64, height=30)
                ipt2 = Entry(root_add, textvariable=var_input2)
                ipt2.place(x=170, y=70, width=158, height=30)
                label3 = Label(root_add, text="Time", anchor="center")
                label3.place(x=70, y=110, width=64, height=30)
                ipt3 = Entry(root_add, textvariable=var_input3)
                ipt3.place(x=170, y=110, width=158, height=30)
                label4 = Label(root_add, text="Team1", anchor="center")
                label4.place(x=70, y=150, width=64, height=30)
                ipt4 = Entry(root_add, textvariable=var_input4)
                ipt4.place(x=170, y=150, width=158, height=30)
                label5 = Label(root_add, text="Score of Team1", anchor="center")
                label5.place(x=40, y=190, width=99, height=30)
                ipt5 = Entry(root_add, textvariable=var_input5)
                ipt5.place(x=170, y=190, width=158, height=30)
                label6 = Label(root_add, text="Score of Team2", anchor="center")
                label6.place(x=40, y=230, width=99, height=30)
                ipt6 = Entry(root_add, textvariable=var_input6)
                ipt6.place(x=170, y=230, width=158, height=30)
                label7 = Label(root_add, text="Team2", anchor="center")
                label7.place(x=60, y=270, width=64, height=30)
                ipt7 = Entry(root_add, textvariable=var_input7)
                ipt7.place(x=170, y=270, width=158, height=30)
                label8 = Label(root_add, text="Status", anchor="center")
                label8.place(x=60, y=310, width=64, height=30)
                cb = Combobox(root_add, state="readonly", textvariable=var_input8)
                cb['values'] = ("Ended", "Not Started")
                cb.place(x=170, y=310, width=158, height=30)
                label9 = Label(root_add, text="Penalty Kick", anchor="center")
                label9.place(x=50, y=350, width=88, height=30)
                ipt9 = Entry(root_add, textvariable=var_input9)
                ipt9.place(x=170, y=350, width=158, height=30)
                btn1 = Button(root_add, text="Confirm", command=add_race)
                btn1.place(x=364, y=320, width=66, height=35)
            elif oper == "m":
                def modify():
                    id = var_input_id.get()
                    month = var_input1.get()
                    day = var_input2.get()
                    time = var_input3.get()
                    team1 = var_input4.get()
                    score1 = var_input5.get()
                    score2 = var_input6.get()
                    team2 = var_input7.get()
                    status = var_input8.get()
                    penalty_kick = var_input9.get()
                    if bool(id) and id.isdigit():
                        data = [int(id), month, int(day), time, team1, int(score1), int(score2), team2, status,
                                penalty_kick]
                        sock.send(json.dumps(["m", "m", data]).encode())
                        response = json.loads(sock.recv(1024))
                        # The information returned from the database is processed
                        if response[0] == "true":
                            tkinter.messagebox.showinfo(title="注意",
                                                        message='成功！重新启动系统即可看到更新的信息。')
                            sock.send("false".encode())
                            root_modify.destroy()
                        elif response[0] == "false":
                            tkinter.messagebox.showerror(title="注意",
                                                         message="您输入的比赛 ID 不存在，无法修改。")
                            sock.send("false".encode())
                    else:
                        tkinter.messagebox.showerror(title="注意",
                                                     message="ID 不能为空，请检查输入内容。")
                        sock.send("false".encode())
                root_modify = Toplevel(self)
                width = 559
                height = 478
                screenwidth = root_modify.winfo_screenwidth()
                screenheight = root_modify.winfo_screenheight()
                geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                root_modify.geometry(geometry)
                root_modify.resizable(width=False, height=False)
                root_modify.title = "Modify"
                var_input1 = StringVar()
                var_input2 = StringVar()
                var_input3 = StringVar()
                var_input4 = StringVar()
                var_input5 = StringVar()
                var_input6 = StringVar()
                var_input7 = StringVar()
                var_input8 = StringVar()
                var_input9 = StringVar()
                var_input_id = StringVar()
                label_id = Label(root_modify, text="ID", anchor="center")
                label_id.place(x=120, y=50, width=64, height=30)
                ipt_id = Entry(root_modify, textvariable=var_input_id)
                ipt_id.place(x=260, y=50, width=158, height=30)
                label1 = Label(root_modify, text="Month", anchor="center")
                label1.place(x=120, y=90, width=64, height=30)
                ipt1 = Entry(root_modify, textvariable=var_input1)
                ipt1.place(x=260, y=90, width=158, height=30)
                label2 = Label(root_modify, text="Day", anchor="center")
                label2.place(x=120, y=130, width=64, height=30)
                ipt2 = Entry(root_modify, textvariable=var_input2)
                ipt2.place(x=260, y=130, width=158, height=30)
                label3 = Label(root_modify, text="Time", anchor="center")
                label3.place(x=120, y=170, width=64, height=30)
                ipt3 = Entry(root_modify, textvariable=var_input3)
                ipt3.place(x=260, y=170, width=158, height=30)
                label4 = Label(root_modify, text="Team1", anchor="center")
                label4.place(x=120, y=210, width=64, height=30)
                ipt4 = Entry(root_modify, textvariable=var_input4)
                ipt4.place(x=260, y=210, width=158, height=30)
                label5 = Label(root_modify, text="Score of Team1", anchor="center")
                label5.place(x=100, y=250, width=99, height=30)
                ipt5 = Entry(root_modify, textvariable=var_input5)
                ipt5.place(x=260, y=250, width=158, height=30)
                label6 = Label(root_modify, text="Score of Team2", anchor="center")
                label6.place(x=100, y=290, width=99, height=30)
                ipt6 = Entry(root_modify, textvariable=var_input6)
                ipt6.place(x=260, y=290, width=158, height=30)
                label7 = Label(root_modify, text="Team2", anchor="center")
                label7.place(x=120, y=330, width=64, height=30)
                ipt7 = Entry(root_modify, textvariable=var_input7)
                ipt7.place(x=260, y=330, width=158, height=30)
                label8 = Label(root_modify, text="Status", anchor="center")
                label8.place(x=120, y=370, width=64, height=30)
                cb = Combobox(root_modify, state="readonly", textvariable=var_input8)
                cb['values'] = ("Ended", "Not Started")
                cb.place(x=260, y=370, width=160, height=30)
                label9 = Label(root_modify, text="Penalty Kick", anchor="center")
                label9.place(x=110, y=410, width=88, height=30)
                ipt9 = Entry(root_modify, textvariable=var_input9)
                ipt9.place(x=260, y=410, width=158, height=30)
                btn1 = Button(root_modify, text="Confirm", command=modify)
                btn1.place(x=480, y=370, width=66, height=35)
            else:
                sock.send("false".encode())
        except EXCEPTION:
            tkinter.messagebox.showerror(title="错误", message="出现错误，请重启系统。")
            sys.exit()
    def query_style(self, info):
        try:
            info = str(info)
            if bool(info):
                pat1 = "[0-9]+:[0-9]+"
                pat2 = "\D"
                if re.search(pat1, info.strip()) or re.search(pat2, info.strip()) or info.isdigit():
                    sock.send(json.dumps(["q", 0, info]).encode())
                    total_data = bytes()
                    while True:
                        data = sock.recv(1024)
                        total_data += data
                        if len(data) < 1024:
                            break
                    response = json.loads(total_data)
                    if not bool(response):
                        tkinter.messagebox.showerror(title="注意", message="无结果")
                    else:
                        # Sets the header field and header width
                        columns = {"ID": 38, "Date": 140, "Time": 58, "Team1": 90, "Points": 64, "Team2": 90,
                                   "Status": 77,
                                   "Penalty Kick": 80}
                        response_show = Toplevel(self)
                        response_show.title('结果')
                        width = 688
                        height = 380
                        screenwidth = response_show.winfo_screenwidth()
                        screenheight = response_show.winfo_screenheight()
                        geometry = '%dx%d+%d+%d' % (
                            width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                        response_show.geometry(geometry)
                        tk_table = Treeview(response_show, show="headings", columns=list(columns))
                        for text, width in columns.items():
                            tk_table.heading(text, text=text, anchor='center')
                            tk_table.column(text, anchor='center', width=width,
                                            stretch=False)  # No automatic stretching
                        tk_table.place(x=20, y=40, width=651, height=313)
                        vbar = Scrollbar(tk_table)
                        tk_table.configure(yscrollcommand=vbar.set)
                        vbar.config(command=tk_table.yview)
                        vbar.place(x=656, y=40, width=15, height=313)
                        for i in response:
                            tk_table.insert("", "end", values=tuple(i))
                else:
                    tkinter.messagebox.showerror(title="注意", message="查询无效，请检查输入内容")
                    sock.send("false".encode())
            else:
                tkinter.messagebox.showerror(title="注意", message="查询无效，请检查输入内容")
                sock.send("false".encode())
        except EXCEPTION:
            tkinter.messagebox.showerror(title="注意", message="错误！请重新启动系统")
def schedule_print():
    sock.send(json.dumps(["p"]).encode())
    total_data = bytes()
    while True:
        data = sock.recv(1024)
        total_data += data
        if len(data) < 1024:
            break
    return json.loads(total_data)
def quit():
    sock.close()
    sys.exit()
if __name__ == '__main__':
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect_ex(server_address)
            check_response = sock.recv(1024)
            print("Receive from server:" + check_response.decode())
            window = LoginPage()
            window.mainloop()
    except ConnectionAbortedError:
        sock.send(json.dumps(["d"]).encode())
        quit()
        tkinter.messagebox.showerror(title="错误",
                                     message="与服务器的连接中断，请重新启动系统。")
        window.destroy()
    except ConnectionResetError:
        sock.send(json.dumps(["d"]).encode())
        quit()
        tkinter.messagebox.showerror(title="错误",
                                     message="与服务器的连接中断，请重新启动系统。")
        window.destroy()
    except EOFError as err:
        sock.send(json.dumps(["d"]).encode())
        quit()
        tkinter.messagebox.showerror(title="错误", message=str(err))
        window.destroy()
