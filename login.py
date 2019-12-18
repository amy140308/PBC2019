import tkinter 
LoginPage

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller=controller
        self.configure(width=250, height=700)
        self.pack(side=BOTTOM, expand=TRUE)
        self.canvas=tk.Canvas(self, height=1000, width=500, bg="plum2") 
        # self.img=Image.open("NBALogo.gif")
        # self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        # self.img=ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.pack(fill=BOTH,expand=Y)
        self.canvas.configure(bg="misty rose")

        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self.canvas, text="使用者名稱：", font=f1)
        self.l2=tk.Label(self.canvas, text="密碼：", font=f1)
        self.l1.pack(side=TOP, fill=X, padx=10, pady=10)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self.canvas, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side=TOP,padx=20, pady=10) #fill=X

        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self.canvas, textvariable=self.var_usr_pwd, show="*") 
        self.entry_usr_pwd.pack(side=TOP, padx=10, pady=10)
        # 以下login command之後要寫成判斷式並用configure結合
        self.btn_login=tk.Button(self.canvas, text="Log in", font=f1, command=self.usr_login)
        self.btn_login.pack(side=RIGHT, padx=10, pady=10)
        self.btn_signup=tk.Button(self.canvas, text="Sign up", font=f1, command=self.usr_signup)
        self.btn_signup.pack(side=RIGHT, padx=10, pady=10)

    
    def usr_login(self):
        check = 0
        user_password = 0
        # 讀取csv檔中的使用者資料至list
        userinformation = []
        with open("userInformation.csv", newline = '') as f:
            rows = csv.reader(f)
            for row in rows:
                userinformation.append(row)
        # 檢查是否有此帳號
        username=self.entry_usr_name.get()
        for i in range(len(userinformation)):
            if username == userinformation[i][0]:
                check += 1
                user_password = userinformation[i][1]
        # 帳號存在
        # 輸入密碼並檢查密碼是否正確
        if check > 0:
            # 輸入密碼
            password=self.entry_usr_pwd.get()
            # 檢查密碼是否正確
            if password == user_password:
                # 這行危險
                app=self.SportsLottery()
                app.mainloop()
                self.destroy()
            else:
                tk.messagebox.showwarning("Warning", "密碼錯誤")
                password=self.entry_usr_pwd.get()
        # 如果沒有此帳號跳出提示訊息
        else:
            tk.messagebox.showwarning("Warning", "查無此帳號")
    
    def usr_signup(self):
        # 讀取csv檔中的使用者資料至list
        userinformation = []
        with open("userInformation.csv", newline = '') as f:
            rows = csv.reader(f)
            for row in rows:
                userinformation.append(row)
        # 檢查ID使否重複
        # ID重複跳出提示訊息
        check=0
        username=self.entry_usr_name.get()
        for i in range(len(userinformation)):
            if username == userinformation[i][0]:
                check+=1
                username=self.entry_usr_name.get()     
        if check==0:
            # 輸入密碼
            password=self.entry_usr_pwd.get()
            # 成立登入時間
            login_time = datetime.datetime.today()
            # 初始帳戶有10000元
            start_money = 10000
            # 使用者資料建檔(寫入csv檔)
            with open("userInformation.csv", "a+", newline='') as f:
                writer=csv.writer(f)
                writer.writerow([username, password, start_money, login_time])
                f.close()
            self.destroy()
        else:
            tk.messagebox.showwarning("Warning", "使用者名稱重複")
        
    
