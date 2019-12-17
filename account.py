import datetime
import csv


class UserAccount():

    def __init__(self, username, password, historyrecords=[]):
        self.username = LoginPage.var_usr_name
        self.password = LoginPage.var_usr_pwd
        self.historyrecords= 

    # 使用者註冊
    def register(self):

        # 讀取csv檔中的使用者資料至list
        """ 
        這段寫出來的csv是會永久存在的嗎？還是會被覆寫？
        """
        userinformation = []
        with open("userInformation.csv", "a", newline = '') as f:
            rows = csv.reader(f)
            for row in rows:
                userinformation.append(row)
        # 檢查ID使否重複
        # ID重複跳出提示訊息
        # 再次輸入ID
        while True:
            for i in range(len(userinformation)):
                if username == userinformation[i][0]:
                    tk.MessageBox.showWarning(text="ID重複")  # 這個部分是我隨便打的，之後再修
                else:
                    break
            break

        # 成立登入時間
        self.login_time = datetime.datetime.today()
        # 初始帳戶有10000元
        self.start_money = 10000

        # 使用者資料建檔(寫入csv檔)
        with open("userInformation.csv", "a", newline='') as f:
            writer=csv.writer(f)
            writer.writerow([self.username, self.password, self.start_money, self.login_time])
            f.close()

    # 使用者登入
    def login(self):
        check = 0
        # 這個使用者在list中的編號 
        ID_num = 0

        # 輸入使用者名稱
        username = input("username: ")

        # 讀取csv檔中的使用者資料至list
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
        # 帳號存在
        # 輸入密碼並檢查密碼是否正確
        if check > 0:
            # 輸入密碼
            password = input()
            # 檢查密碼是否正確
            while True:
                if password == user_password:
                    return ID_num
                    # 進到登入後的畫面
                else:
                    tk.MessageBox.showWarning(text="密碼錯誤")
                    password = input()
        # 如果沒有此帳號跳出提示訊息
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