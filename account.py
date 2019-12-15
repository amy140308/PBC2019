import datetime

def register(userAccount):

    username = input("username:")
    while True:
        # 檢查ID使否重複
        for i in range(len(userAccount)):
            if username == userAccount[i][0]:
                print("ID重複")
                username = input()
            else:
                break
        break
    password=input("password")

    # 成立登入時間
    login_time = datetime.datetime.today()

    # 初始帳戶有10000元
    # 建立帳號至list
    userAccount.append([username, password, 10000, login_time])

    # 使用者資料建檔(csv檔)
    #with open("userInformation.csv", "a", newline='') as f:
        #writer=csv.writer(f)
        #writer.writerow([username, password, start_money])
        #f.close()
        
    return userAccount