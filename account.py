import datetime
import csv


class UserAccount():


    def __init__(self, username, password):
        self.username = LoginPage.var_usr_name
        self.password = Login.var_usr_pwd


    # 帳號註冊
    def register(self):

        username = input("username:")
        userinformation = []
        with open("userInformation.csv", newline = '') as f:
            rows = csv.reader(f)
            for row in rows:
                userinformation.append(row)
        # 檢查ID使否重複
        while True:
            for i in range(len(userinformation)):
                if username == userinformation[i][0]:
                    tk.MessageBox.showWarning(text="ID重複")
                    username = input("username: ")
                else:
                    break
            break
        password=input("password: ")

        # 成立登入時間
        login_time = datetime.datetime.today()

        # 初始帳戶有10000元
        start_money = 10000

        # 使用者資料建檔(csv檔)
        with open("userInformation.csv", "a", newline='') as f:
            writer=csv.writer(f)
            writer.writerow([username, password, start_money, login_time])
            f.close()


    def login(self):
        check = 0
        ID_num = 0
        username = input("username: ")
        userinformation = []
        with open("userInformation.csv", newline = '') as f:
            rows = csv.reader(f)
            for row in rows:
                userinformation.append(row)
        # 檢查是否有此帳號
        for i in range(len(userinformation)):
            if username == userinformation[i][0]:
                check += 1
                ID_num = i
                user_password = userAccount[i][1]
        if check > 0:
            password = input()
            # 檢查密碼是否正確
            while True:
                if password == user_password:
                    return ID_num
                else:
                    tk.MessageBox.showWarning(text="密碼錯誤")
                    password = input()
        else:
            tk.MessageBox.showWarning(text="查無此帳號")


    # 登入當下要做的事
    # def login_duty():
        # 判斷最近下注有沒有算清了?
        # 算清楚比賽結果
        # 召喚交易
        # 下注：結算
        # 判斷今日登入時間是否與最後登入時間相符
        # 每日登入自動新增1,000元(與上次登入的日期不一樣)
        # 更新最後登入時間


    # 檢查帳戶餘額
    def check_balance(self):
        # 顯示帳戶餘額
        print(userbalance) 
        # 餘額是零的時候，顯示明天才能再繼續下注
        if self.balance == 0:
            tk.MessageBox.showWarning(text="You don't have enough money.")


    # 最近一筆交易結果
    # def recent_bet():
        # 當日所有賽事的交易紀錄
        # 盈虧

    # 歷史交易結果
    # def history_bet():
        # 總營虧
        # 最近十筆交易紀錄
        # 日期
        # 每一場賽事名稱
        # 下注的規則
        # 投注金額
        # 賺賠
        # 帳戶餘額