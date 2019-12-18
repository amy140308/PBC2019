import tkinter as tk
import csv
import datetime
import tkinter.font as tkFont
import tkinter.messagebox 

class LoginPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("300x300")
        self.title("運彩模擬器：登入")
        self.configure(bg="misty rose")
       
        # self.img=Image.open("NBALogo.gif")
        # self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        # self.img=ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)
    
        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self, text="使用者名稱：", font=f1)
        self.l2=tk.Label(self, text="密碼：", font=f1)
        self.l1.pack(side="top", fill="x", padx=10, pady=10)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side="top",padx=20, pady=10) #fill=X

        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self, textvariable=self.var_usr_pwd) #show="*" 
        self.entry_usr_pwd.pack(side="top", padx=10, pady=10)
        # 以下login command之後要寫成判斷式並用configure結合
        self.btn_login=tk.Button(self, text="登入", font=f1, command=self.usr_login)
        self.btn_login.pack(side="right", padx=10, pady=10)
        self.btn_signup=tk.Button(self, text="註冊", font=f1, command=self.usr_signup)
        self.btn_signup.pack(side="right", padx=10, pady=10)

    
    def usr_login(self):
        check = 0
        user_password = 0
        # 讀取csv檔中的使用者資料至list
        filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
        userinformation = []
        try:
            with open("userInformation.csv", "r", newline = '') as f:
                rows = csv.reader(f)
                for row in rows:
                    userinformation.append(row)
        except:
           pass
        # 檢查是否有此帳號
        username=self.entry_usr_name.get()
        password=self.entry_usr_pwd.get()
        for i in range(len(userinformation)):
            if username == userinformation[i][0]:
                check += 1
                user_password = userinformation[i][1]
        # 帳號存在
        # 輸入密碼並檢查密碼是否正確
        if check > 0:
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
        try:
            # r必須打開已有的文件
            filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
            userinformation = []
            with open("userInformation.csv", "r", newline = '') as f:
                rows = csv.reader(f)
                for row in rows:
                    userinformation.append(row)
        except:
            pass 
        # 檢查ID是否重複
        # ID重複跳出提示訊息
        check=0
        username=self.entry_usr_name.get()
        password=self.entry_usr_pwd.get()
        usernameList=[]
        for i in range(len(userinformation)):
            usernameList.append(userinformation[i][0])
        if username in usernameList:
            tk.messagebox.showwarning("Warning", "帳號名已被註冊")
            self.entry_usr_name.delete(0, "end")
            self.entry_usr_pwd.delete(0, "end")
        else:
            # 成立登入時間
            login_time = datetime.datetime.today()
            # 初始帳戶有10000元
            start_money = 10000
            # 使用者資料建檔(寫入csv檔)
            filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
            with open("userInformation.csv", "a+", newline='') as f:
                writer=csv.writer(f)
                writer.writerow([username, password, start_money, login_time])
                f.close()
            self.entry_usr_name.delete(0, "end")
            self.entry_usr_pwd.delete(0,"end")
            tk.messagebox.showinfo("Info", "User successfully registered.\nPlease log in.")
                  
app=LoginPage()
app.mainloop()
        