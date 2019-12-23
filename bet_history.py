import datetime
import csv

# 抓使用者的資訊
# 全部的使用者資訊
user_information = []
# 抓到同帳號名使用者的資訊
user_info=[]
with open("userInformation.csv", "r", newline = '') as f:
    rows = csv.reader(f)
    for row in rows:
        if row[0] == username:
            for j in range(len(row)):
                user_info.append(row[j])
            break


# 登入當下要做的事
def login_duty():
    # 上次登入時間
    usr_login_time=user_info[3]
    # 最後登入時間
    login_time=datetime.datetime.today()
    # 判斷今日登入時間是否與最後登入時間相符
    # 每日登入自動新增1,000元(與上次登入的日期不一樣)
    diff=login_time-usr_login_time
    if diff.days>0:
        user_info[2]+=1000
    # 判斷最近下注有沒有算清
    # 算清楚比賽結果
    game_result=[]
    # "data.csv" 
    with open( "/Users/yangqingwen/Downloads/data.csv", 'r', encoding='utf-8') as rf:
        rows=csv.reader(rf)
        for row in rows:
            game_result.append(row)
    for i in range(4, len(user_info)):
        if user_info[i][8]=='未結算':
            for j in range(len(game_result)):
                if game_result[j][0]==user_info[i][0] and game_result[j][2]==user_info[i][1] and game_result[j][3]==user_info[i][2]:
                    total_point=int(game_result[j][4])+int(game_result[j][5])
                    if user_info[i][4]=='不讓分':
                        if int(game_result[j][4])>int(game_result[j][5]):
                            if user_info[i][5]==user_info[i][1]:
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'
                        else:
                            if user_info[i][5]==user_info[i][2]:
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'
                    elif user_info[i][4]=='單雙(總分)':
                        if total_point%2==1:
                            if user_info[i][5]=='單':
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'
                        else:
                            if user_info[i][5]=='雙':
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'
                    elif user_info[i][4]=='大小(總分)':
                        direction=user_info[i][5].split('/')
                        bs=direction[0]
                        point=float(direction[1])
                        if total_point>point:
                            if bs=='大':
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'
                        else:
                            if bs=='小':
                                earn=10*user_info[i][7]*user_info[i][6]
                                user_info[2]+=earn
                                user_info[i][9]+=earn
                                user_info[i][8]=='賺'
                            else:
                                user_info[i][8]=='賠'

#下注格式
# ['時間', 'A隊', 'B隊', '地點', '賭法', '方向', '賠率', '下幾注(一注十元)', '狀態', '盈虧', '下注時間']
# 不讓分
#[2019-12-06, 太陽,鵜鶘, 地點, 不讓分, 隊名,... ]
# 單雙
#[2019-12-06, 太陽,鵜鶘, 地點, 單雙(總分), 單,... ]
# 大小
#[2019-12-06, 太陽,鵜鶘, 地點, 大小(總分), 大/x,...]

'''
# 歷史交易結果
def history_bet():
    pass
    for i in range(len(user_info)-1, 3, -1)
        # 下注日期
        user_info[i][10]
        # 比賽資訊(時間 隊名 地點)
        user_info[i][0], user_info[i][1], user_info[i][2], user_info[i][3]
        # 下注資訊(賭法 方向 賠率 下幾注 狀態)
        user_info[i][4], user_info[i][5], user_info[i][6], user_info[i][7], user_info[i][8]
    # 總盈虧
    total_profit=0
    for i in range(4, len(user_info)):
        total_profit+=user_info[i][9]
'''