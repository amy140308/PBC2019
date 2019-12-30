import tkinter as tk
import webbrowser
import tkinter.font as tkFont
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image, ImageTk
import io 
from io import BytesIO
import ssl
from selenium import webdriver
import datetime
from selenium.webdriver.chrome.options import Options
import time as t
import csv
import tkinter.messagebox 
import copy
import pandas as pd
import ast

"""
Final
"""
driverpath ='/usr/local/bin/chromedriver'
#'/usr/local/bin/chromedriver'
#'chromedriver.exe'

datapath = "/Users/yangqingwen/Downloads/data.csv" 
#  "/Users/yangqingwen/Downloads/data.csv" 
# 'C:\\co-work\\data.csv'

teampath = "/Users/yangqingwen/Desktop/PBC2019/team.csv" 
# "/Users/yangqingwen/Desktop/PBC2019/team.csv" 
# "C:\\co-work\\team.csv"

infopath = "/Users/yangqingwen/Desktop/PBC2019/userInformation.csv"
# "/Users/yangqingwen/Desktop/PBC2019/userInformation.csv"
# C:\\co-work\\userInformation.csv


Logo_road_list = ["/Users/yangqingwen/Desktop/team_logo/ATL_logo.png","/Users/yangqingwen/Desktop/team_logo/BKN_logo.png","/Users/yangqingwen/Desktop/team_logo/BOS_logo.png","/Users/yangqingwen/Desktop/team_logo/CHA_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/CHI_logo.png","/Users/yangqingwen/Desktop/team_logo/CLE_logo.png","/Users/yangqingwen/Desktop/team_logo/DAL_logo.png","/Users/yangqingwen/Desktop/team_logo/DEN_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/DET_logo.png","/Users/yangqingwen/Desktop/team_logo/GSW_logo.png","/Users/yangqingwen/Desktop/team_logo/HOU_logo.png","/Users/yangqingwen/Desktop/team_logo/IND_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/LAC_logo.png","/Users/yangqingwen/Desktop/team_logo/LAL_logo.png","/Users/yangqingwen/Desktop/team_logo/MEM_logo.png","/Users/yangqingwen/Desktop/team_logo/MIA_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/MIL_logo.png","/Users/yangqingwen/Desktop/team_logo/MIN_logo.png","/Users/yangqingwen/Desktop/team_logo/NOP_logo.png","/Users/yangqingwen/Desktop/team_logo/NYK_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/OKC_logo.png","/Users/yangqingwen/Desktop/team_logo/ORL_logo.png","/Users/yangqingwen/Desktop/team_logo/PHI_logo.png","/Users/yangqingwen/Desktop/team_logo/PHX_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/POR_logo.png","/Users/yangqingwen/Desktop/team_logo/SAC_logo.png","/Users/yangqingwen/Desktop/team_logo/SAS_logo.png","/Users/yangqingwen/Desktop/team_logo/TOR_logo.png",
                    "/Users/yangqingwen/Desktop/team_logo/UTA_logo.png","/Users/yangqingwen/Desktop/team_logo/WAS_logo.png"]
"""
Logo_road_list = ["C:\\logo\\ATL_logo.png","C:\\logo\\BKN_logo.png","C:\\logo\\BOS_logo.png","C:\\logo\\CHA_logo.png",
                    "C:\\logo\\CHI_logo.png","C:\\logo\\CLE_logo.png","C:\\logo\\DAL_logo.png","C:\\logo\\DEN_logo.png",
                    "C:\\logo\\DET_logo.png","C:\\logo\\GSW_logo.png","C:\\logo\\HOU_logo.png","C:\\logo\\IND_logo.png",
                    "C:\\logo\\LAC_logo.png","C:\\logo\\LAL_logo.png","C:\\logo\\MEM_logo.png","C:\\logo\\MIA_logo.png",
                    "C:\\logo\\MIL_logo.png","C:\\logo\\MIN_logo.png","C:\\logo\\NOP_logo.png","C:\\logo\\NYK_logo.png",
                    "C:\\logo\\OKC_logo.png","C:\\logo\\ORL_logo.png","C:\\logo\\PHI_logo.png","C:\\logo\\PHX_logo.png",
                    "C:\\logo\\POR_logo.png","C:\\logo\\SAC_logo.png","C:\\logo\\SAS_logo.png","C:\\logo\\TOR_logo.png",
                    "C:\\logo\\UTA_logo.png","C:\\logo\\WAS_logo.png"]
"""

"""五個爬蟲跟四個頁面有關係"""

# 抓news
class news():
    def __init__(self):
        response = requests.get("https://nba.udn.com/nba/cate/6754/6780")
        soup = BeautifulSoup(response.text, 'html.parser')
        attr = {'id' : 'news_list_body'}
        news_tag = soup.find_all('div', attrs = attr)
        for i in news_tag:
            self.pa = str(i)
        self.data = list()

    def get_news(self):
        count = 0
        hend = 0
        tend = 0
        tiend = 0
        pend = 0
        piend = 0
        
        while count < 3:
            tmp = list()
            hstart = self.pa.find('/nba/story/', hend)
            hend = self.pa.find('">', hstart)
            href = 'https://nba.udn.com' + self.pa[hstart:hend]

            tstart = self.pa.find('<h3>', tend)
            tend = self.pa.find('</h3>', tstart)
            title = self.pa[tstart + 4:tend]

            tistart = self.pa.find('h24">', tiend)
            tiend = self.pa.find('</b>', tistart)
            time = self.pa[tistart + 5:tiend]

            pstart = self.pa.find('<p>', pend)
            pend = self.pa.find('</p>', pstart)
            p = self.pa[pstart + 3:pend]

            pistart = self.pa.find('data-src', piend)
            piend = self.pa.find('/><', pistart)
            html = self.pa[pistart + 10:piend - 1]

            count += 1
            tmp.append(title)
            tmp.append(time)
            tmp.append(p)
            tmp.append(href)
            tmp.append(html)
            self.data.append(tmp)

        return self.data

news = news()
final_n = news.get_news()

# 抓wounded
class wounded():
    '''
    抓NBA傷兵情報
    def get_news() 不用input
    return: 一則新聞一個list[標題, 時間, 簡短內文, 新聞超連結網址, 圖片鏈結]
            三個list裝在一個二維list裡面回傳
    '''

    def __init__(self):
        response = requests.get("https://nba.udn.com/nba/cate/6754/6779")
        soup = BeautifulSoup(response.text, 'html.parser')
        attr = {'id' : 'news_list_body'}
        news_tag = soup.find_all('div', attrs = attr)

        for i in news_tag:
            self.pa = str(i)

        self.data = list()

    def get_news(self):
        count = 0
        tend = 0
        tiend = 0
        pend = 0
        hend = 0
        piend = 0
        
        while count < 3:
            tstart = self.pa.find('<h3>', tend)
            tend = self.pa.find('</h3>', tstart)
            title = self.pa[tstart + 4:tend]

            tistart = self.pa.find('h24">', tiend)
            tiend = self.pa.find('</b>', tistart)
            time = self.pa[tistart + 5:tiend]

            pstart = self.pa.find('<p>', pend)
            pend = self.pa.find('</p>', pstart)
            p = self.pa[pstart + 3:pend]
            
            hstart = self.pa.find('/nba/story/', hend)
            hend = self.pa.find('">', hstart)
            href = 'https://nba.udn.com' + self.pa[hstart:hend]

            pistart = self.pa.find('data-src', piend)
            piend = self.pa.find('/><', pistart)
            html = self.pa[pistart + 10:piend - 1]

            count += 1
            self.data.append([title, time, p, href, html])

        return self.data

wounded = wounded()
final_w = wounded.get_news()

# 抓賽事頁面（不會跳瀏覽器）
"""(有改日期)"""
class bet():
    '''
    抓明日的比賽資訊(for 下注)
    用的driver是google chrome
    def get_data() 不用input
    return: 一場比賽一個list[時間, 客隊, 主隊, 場地]
            list數量不定, 視當天比賽場數, 全數包裝在一個二維list裡面回傳
    '''

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 瀏覽器不提供視覺化頁面
        chrome_options.add_argument('--disable-gpu')  # 規避bug
        driver = webdriver.Chrome(executable_path = driverpath, options=chrome_options)
        # executable_path = '/usr/local/bin/chromedriver'
        # executable_path = 'chromedriver.exe'
        driver.get('https://tw.global.nba.com/schedule/#!/7')
        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, 'html.parser')
        attr = {'data-ng-repeat' : 'date in group.dates'}
        bet_tag = soup.find_all('tbody', attrs = attr)

        try:
            for tag in bet_tag:
                date = tag.find('h6').string.strip()
                m_end = date.find('月')
                month = int(date[:m_end])
                d_end = date.find('日')
                day = int(date[m_end + 2 : d_end])
                # diff = datetime.timedelta(days=1)
                today = datetime.date.today()
                # today = datetime.date.today() + diff
                year = today.year
                d = datetime.datetime(year, month, day)
                if d == datetime.datetime(year, today.month, today.day + 1):
                    self.data = tag.find_all('tr')
                    break
        except:
            pass

    def get_data(self):

        data_list = list()
        try:
            for i in self.data:
                p = str(i)  # 因為soup抓不到'bo-hide'標籤的資訊，所以手動用字串分析的方式
                start = p.find('<span bo-hide')
                if start == -1:  # 如果找不到該tag就跳過
                    continue
                end = p.find('</span>', start)
                time = p[start + 62: end - 1]

                team = i.find_all('a', limit = 2)  # 前兩個<a>放的是客隊跟主隊的隊名
                team_list = list()
                for j in team:
                    team_list.append(j.get_text())
                away = team_list[0]
                home = team_list[1]

                attr_s = {'bo-text' : 'game.profile.arenaName'}  # 場地資訊
                arena = i.find('td', attrs = attr_s).string

                data_list.append([time, away, home, arena])
        except:
            pass

        return data_list

bet = bet()
final_g = bet.get_data()
print(final_g)
# 抓歷史資訊
class history():
    '''
    抓2019/12/01以後的歷史比分紀錄
    如果單純建構的話chrome會被打開且不會被關閉
    必須使用
    def update() 不用input
    沒有return 會更新檔案到上次紀錄的地方 或是建立新檔案追溯到2019/12/1
    csv格式：日期, 時間, 客隊, 主隊, 客隊分數, 主隊分數, 場地
    更新完之後chrome會被關閉
    def get_date(date)
    input: date格式須為%Y-%m-%d
    return: 會把選取的日期的資料抓出來, 一場比賽一個list
            全數包裝在一個二維list裡面回傳
    '''

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 瀏覽器不提供視覺化頁面
        chrome_options.add_argument('--disable-gpu')  # 規避bug
        self.driver = webdriver.Chrome( executable_path = driverpath , options=chrome_options)
        self.driver.get('https://tw.global.nba.com/schedule/#!/7')
        

    def update(self):
        stop = False  # 控制什麼時候就不用再按日期回鍵抓資訊
        while not stop:
            t.sleep(1)
            self.driver.find_element_by_xpath('//*[@class="icon-caret-left days"]').click()
            t.sleep(3)  # 按下日期回鍵後等一下下再抓程式碼，免得瀏覽器跑太慢
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            attr = {'data-ng-repeat' : 'date in group.dates'}
            his_tag = soup.find_all('tbody', attrs = attr)
            
            for tag in his_tag:
                date = tag.find('h6').string.strip()
                m_end = date.find('月')
                month = int(date[:m_end])
                d_end = date.find('日')
                day = int(date[m_end + 2 : d_end])
                today = datetime.date.today()
                
                if month <= today.month:
                    year = today.year
                else:  # 如果往回抓的月份比現在大，就代表過了一年了
                    year = today.year + 1
                
                d = datetime.datetime(year, month, day)
                
                
                #  "/Users/yangqingwen/Downloads/data.csv" 
                # 'C:\\co-work\\data.csv'
                wf = open(file=datapath, mode="a+",newline='', encoding="utf-8")
                writer = csv.writer(wf)
                rf = open(file=datapath, mode="r", encoding="utf-8")
                reader = csv.reader(rf)
                
                #print(reader)
                exist = False  # 看這個日期的比賽資訊是不是已經抓過了
                for row in reader:
                    if row[0] == d.strftime('%Y-%m-%d'):
                        exist = True
                        break

                if d < datetime.datetime(2019, 12, 1):  # 紀錄最多抓到2019/12/01
                    stop = True
        
                elif not exist:  # 如果沒抓過的日期就進行更新動作
                    data = tag.find_all('tr')
                    data_list = list()

                    for i in data:
                        p = str(i)  # 因為soup抓不到'bo-hide'標籤的資訊，所以手動用字串分析的方式
                        start = p.find('<span bo-hide')
                        if start == -1:  # 如果找不到該tag就跳過
                            continue
                        end = p.find('</span>', start)
                        time = p[start + 62: end - 1]

                        team = i.find_all('a', limit = 2)  # 前兩個<a>放的是客隊跟主隊的隊名
                        team_list = list()
                        for j in team:
                            team_list.append(j.get_text())
                        away = team_list[0]
                        home = team_list[1]

                        attr_s = {'bo-text' : 'game.profile.arenaName'}  # 場地資訊
                        arena = i.find('td', attrs = attr_s).string

                        attr_t = {'bo-text' : ' game.boxscore.awayScore'}  # 比數
                        away_score = int(i.find('span', attrs = attr_t).string)
                        attr_f = {'bo-text' : ' game.boxscore.homeScore'}
                        home_score = int(i.find('span', attrs = attr_f).string)

                        writer.writerow([d.strftime('%Y-%m-%d'), time, away, home, away_score, home_score, arena])
                else:
                    stop = True  # 因為網頁資訊是從舊的排到新的，所以這一頁如果有人抓過了，就代表前面的抓過了，不用再往回按
        wf.close()
        rf.close()
        self.driver.close()

    def get_data(self, date):
        filepath = datapath
        f = open(file=filepath, mode="r", encoding="utf-8")
        rows = csv.reader(f)
        
        data = list()
        for row in rows:  # 把符合該日期的資料全數抓出
            if row[0] == date:
                data.append(row)
        return data

# 以下為試class的功能
# history = history()
# history.update()

"""這邊開始是隊伍資訊的30個各隊資料"""


"""
12/29抓team.csv的更新版gamebet()
"""

class gamebet():
    """
    def odds 需要輸入雙方隊伍名字
    return 賠率清單，單元數固定
    [['單雙', '單', 1.75, '雙', 1.75],
     ['大小(總分)', '大於X分', 1.75, '小於X分', 1.75],
     ['不讓分', 'A隊名', A賠率, 'B隊名', B賠率]]
    """
    def odds(self, team_name_A, team_name_B):
        
        teamnamedict = {"塞爾蒂克": "波士頓塞爾蒂克", "公牛": "芝加哥公牛", 
                        "老鷹": "亞特蘭大老鷹", "籃網": "布魯克林籃網", 
                        "騎士": "克里夫蘭騎士", "黃蜂": "夏洛特黃蜂", "尼克": "紐約尼克",
                        "活塞": "底特律活塞", "熱火": "邁阿密熱火", "76人": "費城76人",
                        "溜馬": "印第安納溜馬", "魔術": "奧蘭多魔術", "暴龍": "多倫多暴龍", 
                        "公鹿": "密爾瓦基公鹿", "巫師": "華盛頓巫師", "金塊": "丹佛金塊", "勇士": "金州勇士", 
                        "獨行俠": "達拉斯獨行俠", "灰狼": "明尼蘇達灰狼", "快艇": "洛杉磯快艇",
                        "火箭": "休士頓火箭", "雷霆": "奧克拉荷馬城雷霆", "湖人": "洛杉磯湖人", 
                        "灰熊": "曼菲斯灰熊", "拓荒者": "波特蘭拓荒者", "太陽": "鳳凰城太陽", 
                        "鵜鶘": "紐奧良鵜鶘", "爵士": "猶他爵士", "國王": "沙加緬度國王", "馬刺": "聖安東尼奧馬刺"}
        
        team_name_A = teamnamedict[team_name_A]
        team_name_B = teamnamedict[team_name_B]
        
        print("***calculating odds...")
        data_list = []
        
        
        team_file =teampath   #要改
        # "/Users/yangqingwen/Desktop/PBC2019/team.csv" 
        # "C:\\co-work\\team.csv"
        with open(team_file, 'r', encoding='UTF-8') as csvfile:
            rows = csv.reader(csvfile)
            line = 1
            line_team_A = 0
            line_team_B = 0
            
            for row in rows:
                if row[0] == team_name_A:
                    self.win_oddsA = (float(row[4][:(len(row[4])-1)]) / 100)
                    line_team_A = line
                                
                elif row[0] == team_name_B:
                    self.win_oddsB = (float(row[4][:(len(row[4])-1)]) / 100)
                    line_team_B = line

                if line_team_A != 0:
                    if line == (line_team_A + 12):
                        self.score_A = float(row[0])    
                        
                if line_team_B != 0: 
                    if line == (line_team_B + 12):
                        self.score_B = float(row[0])
                    
                line += 1
                
        print(team_name_A, self.win_oddsA, self.score_A)
        print(team_name_B, self.win_oddsB)
        
        
        """
        賠率公式：
        1. 單雙：雙方賠率都是1.75
        2. 大小(總分)：
        3. 不讓分：需判斷勝率/平均總分，決定賠率
        簡易版本：勝率對應好壞狀態，若A好B壞，則A贏；反之則B贏。若A好B好，A壞B壞，則判斷平均得分。
        若平均得分相差小於9分，則判定勝率各半。
        勝率倒數為賠率，Cap最高是3.75倍，最低是1.15倍
        """
        
        #單雙
        data_list.append(['單雙(總分)', '單', 1.75, '雙', 1.75])
        
        #大小
        scoresum = self.score_A + self.score_B
        scoresum = int(scoresum) + 0.5 #確保大小是以.5結尾
        data_list.append(['大小(總分)', ('大/' + str(scoresum)), 1.75,
                          ('小/' + str(scoresum)), 1.75])
        
        #不讓分
        teamA_odds = self.win_oddsA * (1 - self.win_oddsB)
        teamB_odds = self.win_oddsB * (1 - self.win_oddsA)
        
        if abs(self.score_A - self.score_B) <= 9:
            teamA_odds += ((1 - teamA_odds) - teamB_odds) / 2
            teamB_odds += ((1 - teamA_odds) - teamB_odds) / 2 

        elif self.score_A > self.score_B:
            teamA_odds += (1 - teamA_odds - teamB_odds)

        elif self.score_A < self.score_B:
            teamB_odds += (1 - teamA_odds - teamB_odds)
        
        print('win odds:', teamA_odds, teamB_odds)

        if teamA_odds != 0 and teamB_odds != 0: #判斷Cap
            teamA_odds = round((1 / teamA_odds), 2)
            teamB_odds = round((1 / teamB_odds), 2)
            
            teamA_odds = 3.75 if (teamA_odds > 3.75) else teamA_odds
            teamA_odds = 1.15 if (teamA_odds < 1.15) else teamA_odds
            teamB_odds = 3.75 if (teamB_odds > 3.75) else teamB_odds
            teamB_odds = 1.15 if (teamB_odds < 1.15) else teamB_odds
    
        else: #如果有一方勝率為0時，則直接給上下Cap最大賠率
            if teamA_odds == 0:
                teamA_odds = 3.75
                teamB_odds = 1.15
                
            elif teamB_odds == 0:
                teamA_odds = 1.15
                teamB_odds = 3.75
        
        print('bet odds for 不讓分:', teamA_odds, teamB_odds)
        
        data_list.append(['不讓分', team_name_A, teamA_odds, team_name_B, teamB_odds])
        
        return data_list

# 下注回傳 global function
def confirm_bet(bet_list):
        #user_info = ['kevin', '123', 200, 'login', [ [], [], [] ]  ]
        #user_info = [username, password, balance, login time, [ [], [], [] ]  ]
        
        #計算總價金，做成交易紀錄
        bet_sum = 0
        for i in range(len(bet_list)):
            bet_sum += bet_list[i][7] * 10
            bet_list[i].append('未結算')
            bet_list[i].append(- (bet_list[i][7] * 10))
            bet_list[i].append(t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
        
        print("user_info[4]", user_info[4])
        
        # 原本為空集合時
        # if user_info[4] == "":

        user_info[2] = int(user_info[2])
        
        #需要Check Balance的函數
        if user_info[2] < bet_sum:
            tk.messagebox.showwarning("Warning", "帳戶餘額不足，無法投注！")
        
        else:   
            #從帳戶扣取應繳金額
            user_info[2] -= bet_sum
            
            #新增一筆交易資料
            try:
                for i in range(len(bet_list)):
                    user_info[4].append(bet_list[i])
            except:
                pass
        
        print("user_info[4] after", user_info[4])
        return user_info
        
        
# 登入當下要做的事
# global function 
def login_duty():  # user_info是list
    # 上次登入時間
    usr_login_timeStr=user_info[3]
    # 最後登入時間
    login_time=datetime.datetime.now() 
    user_info[3] = login_time
    # print("login_time:"+str(login_time))
    # 判斷今日登入時間是否與最後登入時間相符
    # 每日登入自動新增1,000元(與上次登入的日期不一樣)
    """
    個人資料已修復 待下注
    """
    usr_login_time=datetime.datetime.strptime(usr_login_timeStr, "%Y-%m-%d %H:%M:%S.%f") # 2019-12-24 15:30:00

    diff=login_time-usr_login_time
    if diff.days>0:
        user_info[2]=int(user_info[2])
        user_info[2]+=1000
    
    # 判斷最近下注有沒有算清
    # 算清楚比賽結果
    game_result=[]
    # "/Users/yangqingwen/Downloads/data.csv"
    # "C:\\co-work\\data.csv"
    with open(datapath, 'r', encoding='utf-8') as rf:
        rows=csv.reader(rf)
        for row in rows:
            game_result.append(row)
    
    # 從string轉化成list
    user_info[4] = ast.literal_eval(user_info[4])
    
    if user_info[4] != []:
        for i in range(len(user_info[4])):
            if user_info[4][i][8]=='未結算':
                for j in range(len(game_result)):
                    if game_result[j][0]==user_info[4][i][0] and game_result[j][2]==user_info[4][i][1] and game_result[j][3]==user_info[4][i][2]:
                        total_point=int(game_result[j][4])+int(game_result[j][5])
                        if user_info[4][i][4]=='不讓分':
                            if int(game_result[j][4])>int(game_result[j][5]):
                                if user_info[4][i][5]==user_info[4][i][1]:
                                    user_info[4][i][7]=int(user_info[4][i][7])
                                    user_info[4][i][6]=int(user_info[4][i][6])
                                    user_info[2]=int(user_info[2])
                                    user_info[4][i][9]=int(user_info[4][i][9])
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]='賠'
                            else:
                                if user_info[4][i][5]==user_info[4][i][2]:
                                    user_info[4][i][7]=int(user_info[4][i][7])
                                    user_info[4][i][6]=int(user_info[4][i][6])
                                    user_info[2]=int(user_info[2])
                                    user_info[4][i][9]=int(user_info[4][i][9])
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]=='賠'
                        elif user_info[4][i][4]=='單雙（總分）':
                            if total_point%2==1:
                                if user_info[4][i][5]=='單':
                                    user_info[4][i][7]=int(user_info[4][i][7])
                                    user_info[4][i][6]=int(user_info[4][i][6])
                                    user_info[2]=int(user_info[2])
                                    user_info[4][i][9]=int(user_info[4][i][9])
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]='賠'
                            else:
                                if user_info[4][i][5]=='雙':
                                    user_info[4][i][7]=int(user_info[4][i][7])
                                    user_info[4][i][6]=int(user_info[4][i][6])
                                    user_info[2]=int(user_info[2])
                                    user_info[4][i][9]=int(user_info[4][i][9])
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]=='賠'
                        elif user_info[4][i][4]=='大小（總分）':
                            user_info[4][i][7]=int(user_info[4][i][7])
                            user_info[4][i][6]=int(user_info[4][i][6])
                            user_info[2]=int(user_info[2])
                            user_info[4][i][9]=int(user_info[4][i][9])
                            direction=user_info[4][i][5].split('/')
                            bs=direction[0]
                            point=float(direction[1])
                            if total_point>point:
                                if bs=='大':
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]='賠'
                            else:
                                if bs=='小':
                                    earn=10*user_info[4][i][7]*user_info[4][i][6]
                                    earn = number_float_check(earn)
                                    user_info[2]+=earn
                                    user_info[4][i][9]+=earn
                                    user_info[4][i][8]='賺'
                                else:
                                    user_info[4][i][8]='賠'

def number_float_check(earn):
    if earn != int(earn):
        earn = int(earn)+1
    return earn
    
    
def save_csv(username):
    # 讀檔
    df=pd.read_csv(infopath)

    # 刪除使用者原本在csv檔中的那列
    # username為login後pass進來的使用者名稱
    df=df[df.Username != username]
    df.to_csv(infopath, index = False)
    
    # 把修改後的user_info增加至csv檔中的最後一項
    # usr_list=['123', '123', 10000, '17:53'] 我隨便打的
    add_df=df.append(pd.Series(user_info, index=df.columns), ignore_index=True)


    # 存檔
    # C:\\co-work\\userInformation.csv
    add_df.to_csv(infopath, index = False)



"""前台主程式開始"""


#  SportsLottery相當於開一個主視窗
class SportsLottery(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("300x300")
        self.title("運彩模擬器")
        self.frames = {}

        # container中，堆疊frames，跳轉頁面用
        container = tk.Frame(self, width=500, height=700)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # LoginPage(parent=container, controller=self).grid(row=1, column=0, sticky="nsew")
        
        """要做的事情"""
       

        for page in (NewsPage, TeamPage, PersonalPage, GamePage, HistoryPage, LoginPage): 
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame # 存進dictionary
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            if page_name == "PersonalPage":
                PP=frame
            frame.grid(row=1, column=0, sticky="nsew")
        
        # 預設開啟頁面為登入頁
        self.show_frame("LoginPage")
    
    # 用tkraise決定哪個頁面要顯示在最上面
    def show_frame(self, page_name):
        '''Show a frame for the given page name（跳轉頁面）'''
        frame = self.frames[page_name]
        frame.tkraise()
    def user_info_modify(self):
        self.geometry("1280x680")
        self.resizable(False, False)
        PersonalPage=self.frames["PersonalPage"]
        PersonalPage.modify()


class GradientCanv(tk.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="old lace", color2="misty rose", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = GradientCanv(self,width=300, height=300, color1="lemon chiffon", color2="misty rose", highlightthickness = 0, relief="sunken")
        self.canvas.pack(side="top", fill="both", expand=True)
        # self.img=Image.open("NBALogo.gif")
        # self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        # self.img=ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)
    
        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self.canvas, text="使用者名稱：", font=f1, bg="old lace")
        self.l2=tk.Label(self.canvas, text="密碼：", font=f1, bg="old lace")
        self.l1.pack(side="top", padx=10, pady=20)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self.canvas, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side="top",padx=10, pady=10) 
        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self.canvas, textvariable=self.var_usr_pwd) #show="*" 
        self.entry_usr_pwd.pack(side="top", padx=10, pady=10)
        # 以下login command之後要寫成判斷式並用configure結合
        self.btn_login=tk.Button(self.canvas, text="登入", font=f1, command=self.usr_login)
        self.btn_login.pack(side="right", padx=10, pady=10)
        self.btn_signup=tk.Button(self.canvas, text="註冊", font=f1, command=self.usr_signup)
        self.btn_signup.pack(side="right", padx=10, pady=10)
    
    def usr_login(self):
        # 讀取csv檔中的使用者資料至list

        df=pd.read_csv(infopath)
        user_info_tolist=df.values.tolist()

        # 檢查是否有此帳號
        check=0
        global username
        global password
        username=self.entry_usr_name.get()
        password=self.entry_usr_pwd.get()
        for i in range(len(user_info_tolist)):
            if username == user_info_tolist[i][0]:
                check += 1
                user_password = user_info_tolist[i][1]
        # 帳號存在
        # 輸入密碼並檢查密碼是否正確
        if check > 0:
            # 檢查密碼是否正確
            if password == user_password:
                self.controller.show_frame("NewsPage")
                self.controller.user_info_modify()
            else:
                tk.messagebox.showwarning("Warning", "密碼錯誤")
                self.entry_usr_name.delete(0, "end")
                self.entry_usr_pwd.delete(0, "end")
        # 如果沒有此帳號跳出提示訊息
        else:
            tk.messagebox.showwarning("Warning", "查無此帳號")
    
    def usr_signup(self):
        # 讀取csv檔中的使用者資料至list
        try:
            # r必須打開已有的文件
            df=pd.read_csv(infopath)
            user_info_tolist=df.values.tolist()
        except:
            pass 
        # 檢查ID是否重複
        # ID重複跳出提示訊息
        check=0
        username=self.entry_usr_name.get()
        password=self.entry_usr_pwd.get()
        usernameList=[]
        for i in range(len(user_info_tolist)):
            usernameList.append(user_info_tolist[i][0])
        if username in usernameList:
            tk.messagebox.showwarning("Warning", "帳號名已被註冊")
            self.entry_usr_name.delete(0, "end")
            self.entry_usr_pwd.delete(0, "end")
        else:
            # 成立登入時間
            login_time = datetime.datetime.now()
            # 初始帳戶有10000元
            start_money = 10000
            # 下注紀錄
            bet_history = []
            # 使用者資料建檔(寫入csv檔)
            df=pd.read_csv(infopath)
            start_list=[username, password, start_money, login_time, bet_history]
            add_df=df.append(pd.Series(start_list, index=df.columns), ignore_index=True)
            print(add_df)
            add_df.to_csv(infopath, index=False)
            self.entry_usr_name.delete(0, "end")
            self.entry_usr_pwd.delete(0,"end")
            tk.messagebox.showinfo("Info", "User successfully registered.\nPlease log in.")

# 登入後五個頁面共同的板塊建立方式
def create_common_frames(self, controller):

    self.f1=tk.Frame(self,bg="bisque2",width=500, height=300)# misty rose
    self.f1.pack(side="top", fill="both")
    
    functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
    for function in reversed(functions):
        self.btn=tk.Button(self.f1, height=2, width=12, relief="flat", bg="old lace", fg="sienna4", font="Didot", text=function)
        self.btn.pack(side="right", pady=30, anchor="n")
        btn_txt=self.btn.cget("text")
        if btn_txt == "新聞介紹":
            self.btn.configure(command=lambda: self.controller.show_frame("NewsPage"))
        elif btn_txt == "球隊介紹":
            self.btn.configure(command=lambda: self.controller.show_frame("TeamPage"))
        elif btn_txt == "賽事下注":
            self.btn.configure(command=lambda: self.controller.show_frame("GamePage"))
        elif btn_txt == "歷史資料":
            self.btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
        elif btn_txt == "個人帳戶":
            self.btn.configure(command=lambda: self.controller.show_frame("PersonalPage"))

# NewsPage新聞頁
class NewsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller=controller
        self.configure(bg="old lace",width=1200, height=800)
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        
        self.F2=tk.Frame(self, width=1200, height=500)
        self.F2.pack(side="top", fill="both", expand="TRUE")
        self.FN=tk.Frame(self.F2,bg="AntiqueWhite1",width=200, height=500) #AntiqueWhite1 wheat1
        self.FN.pack(side="left", anchor="w",fill="both", expand=True)
        self.FW=tk.Frame(self.F2, bg="old lace", width=200, height=500)
        self.FW.pack(side="left",fill="both", expand="TRUE")
        
        # 新聞部分
        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl=tk.Label(self.FN, text="最新消息", font=f0, bg="old lace")#"floral white"
        self.TitleLbl.pack(side="top",fill = "x", ipady = 12)
        
        self.Frame_List = []
        # print(final_n)
        # print(final_w)
        def callback1(event):
            webbrowser.open_new(final_n[0][-2])
        def callback2(event):
            webbrowser.open_new(final_n[1][-2])
        def callback3(event):
            webbrowser.open_new(final_n[2][-2])
        i=0
        for one_news in final_n:
            self.every_news_frame = tk.Frame(self.FN, width=50, height=20, bg="AntiqueWhite1")
            self.every_news_frame.pack(side="top", fill="both", anchor="nw", pady=20, padx=10, expand=True)#, expand="TRUE"
            self.Frame_List.append(self.every_news_frame)
            title=one_news[0]
            time=one_news[1]
            intro=one_news[2]
            if 23<=len(intro)<=46:
                intro=intro[:23]+"\n"+intro[24:]
            elif 46<=len(intro):
                intro=intro[:23]+"\n"+intro[24:46]+"\n"+intro[47:]
            image_url=one_news[-1]
            ssl._create_default_https_context = ssl._create_unverified_context
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()
            self.img = Image.open(BytesIO(raw_data))
            self.img=self.img.resize((160, 96), Image.ANTIALIAS) 
            self.img=ImageTk.PhotoImage(self.img)
            
            self.picLabel = tk.Label(self.every_news_frame, image=self.img, cursor="hand2")
            self.picLabel.image = self.img
            self.picLabel.pack(side="left", pady=10, padx=10, anchor="nw") 
            
            f1=tkFont.Font(size=14, family="微軟正黑體")
            f2=tkFont.Font(size=10, family="微軟正黑體")
            
            self.btn=tk.Label(self.every_news_frame, text=title, font=f1, bg="AntiqueWhite1", cursor="hand2")#old lace
            self.btn.pack(side="top", pady=5, padx=10, anchor="w",) # 傷兵：anchor=E
            
            self.btnsmall=tk.Label(self.every_news_frame, text=time+"\n"+intro,font=f2, bg="AntiqueWhite1", justify="left", cursor="hand2") # 傷兵/justify=RIGHT
            self.btnsmall.pack(side="top",pady=2, padx=10, anchor="w") # 傷兵：anchor=E
          
            if  i == 0:
                self.picLabel.bind("<Button-1>", callback1)
                self.btn.bind("<Button-1>", callback1)
                self.btnsmall.bind("<Button-1>", callback1)
            elif i ==1: 
                self.picLabel.bind("<Button-1>", callback2)
                self.btn.bind("<Button-1>", callback2)
                self.btnsmall.bind("<Button-1>", callback2)
            else:
                self.picLabel.bind("<Button-1>", callback3)
                self.btn.bind("<Button-1>", callback3)
                self.btnsmall.bind("<Button-1>", callback3)

            i+=1

        # 傷兵部分
        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl2=tk.Label(self.FW, text="傷兵資訊", font=f0, bg="AntiqueWhite1")
        self.TitleLbl2.pack(side="top",fill = "x", ipady = 12)
        
        self.Frame_List2 = []
        def callback4(event):
            webbrowser.open_new(final_w[0][-2])
        def callback5(event):
            webbrowser.open_new(final_w[1][-2])
        def callback6(event):
            webbrowser.open_new(final_w[2][-2])
        i=0
        for one_wounded in final_w:
            self.every_news_frame = tk.Frame(self.FW, width=50, height=20, bg="old lace")
            self.every_news_frame.pack(side="top", fill="both", anchor="nw", pady=20, padx=10, expand=True)#, expand="TRUE"
            self.Frame_List2.append(self.every_news_frame)
            title=one_wounded[0]
            time=one_wounded[1]
            intro=one_wounded[2]
            if 22<=len(intro)<=44:
                intro=intro[:22]+"\n"+intro[23:]
            elif 44<=len(intro):
                intro=intro[:22]+"\n"+intro[23:44]+"\n"+intro[45:]
            
            image_url=one_wounded[-1]
            ssl._create_default_https_context = ssl._create_unverified_context
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()
            self.img = Image.open(BytesIO(raw_data))
            self.img=self.img.resize((160, 96), Image.ANTIALIAS) 
            self.img=ImageTk.PhotoImage(self.img)
            
            self.picLabel = tk.Label(self.every_news_frame, image=self.img, cursor="hand2")
            self.picLabel.image = self.img
            self.picLabel.pack(side="left", pady=10, padx=10, anchor="nw") 
            
            f1=tkFont.Font(size=14, family="微軟正黑體")
            f2=tkFont.Font(size=10, family="微軟正黑體")
            
            self.btn=tk.Label(self.every_news_frame, text=title, font=f1,bg="old lace",cursor="hand2") #cornsilk2 gray90 
            self.btn.pack(side="top", pady=5, padx=10, anchor="w")
            
            self.btnsmall=tk.Label(self.every_news_frame, text=time+"\n"+intro,font=f2, bg="old lace", justify="left", cursor="hand2") 
            self.btnsmall.pack(side="top",pady=2, padx=10, anchor="w")         
            
            if i == 0: 
                self.btn.bind("<Button-1>", callback4)
                self.btnsmall.bind("<Button-1>", callback4)
                self.picLabel.bind("<Button-1>", callback4)
            elif i == 1:
                self.btn.bind("<Button-1>", callback5)
                self.btnsmall.bind("<Button-1>", callback5)
                self.picLabel.bind("<Button-1>", callback5)
            else: 
                self.btn.bind("<Button-1>", callback6)
                self.btnsmall.bind("<Button-1>", callback6)
                self.picLabel.bind("<Button-1>", callback6)
            i+=1

class TeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "old lace")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        
        self.F2=tk.Frame(self, width=1200, height=600, bg = "old lace")
        self.F2.pack(side="top", fill="both", expand="TRUE")

        """
        self.F2_canvas = tk.Canvas(self, width = 500, height = 600, bg = "old lace", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "old lace", width = 500, height = 600)
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((0,0), window = self.F2, anchor = "nw") 

        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)
        """
        self.createWidgets()
        
    def createWidgets(self):
        # 放賽事
        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl=tk.Label(self.F2, text="球隊介紹", font=f0 ,bg="old lace").pack(side = "top", pady = 15)

        
        # 點按鈕為各隊伍資訊
        def click_team_button(team_name):
            window = tk.Toplevel(self)
            window.title(team_name)
            window.geometry("1100x640")
            window.resizable(False, False)
            
            
            self.container = tk.Frame(window, height=500, width=1000, bg="bisque2")
            self.container.pack(side="top",fill="both", expand=True)
            
            
            """
            # 以下是有container的scrollbar寫法
            self.teamCanv = tk.Canvas(self.container, width=500, height = 2000, highlightthickness=0, bg="bisque2")
            self.teamCanv.pack(side = "top", fill = "both", expand=True)
            teamBar = tk.Scrollbar(self.teamCanv, orient = "vertical", command = self.teamCanv.yview)
            teamBar.pack(side = "right", fill = "y")

            self.scrollableF=tk.Frame(self.teamCanv, bg = "bisque2", width=1000, height = 500)
            self.scrollableF.pack(side = "bottom", fill = "both", anchor="center")
            self.teamCanv.configure(yscrollcommand = teamBar.set)
            self.scrollableF.bind("<Configure>",lambda x: self.teamCanv.configure(scrollregion=self.teamCanv.bbox("all")))
            self.teamCanv.create_window((0, 0), window=self.scrollableF, anchor="nw")
            """
            # 視窗的隊伍資訊
            filepath = teampath
            wf = open(file=filepath, mode="r", encoding="utf-8")
            rows = csv.reader(wf)  
            team_info = []
            players = []
            games = []
            self.Photo_list = []

            count = 0
            for i in rows:
                if i[0] == team_name:
                    count = 1
                    team_info = i
                elif 1 <= count and count <= 5:
                    players.append(i)
                    count += 1
                elif 6 <= count and count <= 11:
                    games.append(i)
                    count += 1
                elif count == 12:
                    games.append(i[0])
                    count += 1
                elif count > 13:
                    break
            wf.close
            
            # 隊伍簡介
            self.Info_frame = tk.Frame(self.container, bg = "old lace",width = 1000, height = 110)
            self.Info_frame.pack(side= "top", anchor="w",fill="both", expand=True)
            InfoLabel_text = "\n"+"隊"+"\n"+"伍"+"\n"+"簡"+"\n"+"介"+"\n"
            self.InfoLabel=tk.Label(self.Info_frame, text=InfoLabel_text, font=("標楷體", 18), bg="bisque2")
            self.InfoLabel.pack(side= "left", anchor="w", ipady = 5, ipadx = 10)
            
            self.Label= tk.Label(self.Info_frame, bg="old lace")            
            self.Label.configure(text="隊伍名稱："+team_info[0]+
                                        "\n"+"教練："+team_info[1]+
                                        "\n"+"分區聯盟："+team_info[2]+
                                        "\n"+"分區排名："+team_info[3]+
                                        "\n"+"勝率："+team_info[4],
                                 justify = "left",
                                 font=("標楷體", 15))
            self.Label.pack(side= "left", anchor="w", ipadx = 30)
            
            # 先發名單
            # 名、姓氏、位置、頭像連結 (五個先發各在一個list，包成2-d list回傳)
            self.FivePlayer_frame = tk.Frame(self.container, bg = "bisque2",width = 1000, height = 110)
            self.FivePlayer_frame.pack(side= "top", anchor="w",fill="both", expand=True)
            PlayerLabel_text = "\n"+"先"+"\n"+"發"+"\n"+"名"+"\n"+"單"+"\n"
            self.PlayerLabel=tk.Label(self.FivePlayer_frame, text=PlayerLabel_text, font=("標楷體", 18), bg="old lace")
            self.PlayerLabel.pack(side= "left", anchor="w", ipady = 10, ipadx = 10)
            
            for i in range(len(players)):
                image_url=players[i][3]
                ssl._create_default_https_context = ssl._create_unverified_context
                self.OnePlayer_frame = tk.Frame(self.FivePlayer_frame, bg =  "bisque2",width = 100, height = 100)
                self.OnePlayer_frame.pack(side= "left", anchor="w", fill="both", expand=True, padx = 20, pady = 2)
                
                try:
                    u = urlopen(image_url)
                    raw_data = u.read()
                    u.close()
                    self.playerPhoto = Image.open(BytesIO(raw_data))
                    self.playerPhoto = self.playerPhoto.resize((130, 95), Image.ANTIALIAS) 
                    self.playerPhoto = ImageTk.PhotoImage(self.playerPhoto)
                    self.Photo_list.append(self.playerPhoto)
                    self.photoLabel = tk.Label(self.OnePlayer_frame, image=self.Photo_list[i],bg = "bisque2")
                    self.photoLabel.pack(side="top", pady=8, anchor="center")   
                except:
                    self.photoLabel = tk.Label(self.OnePlayer_frame, text="No image", bg= "bisque2")
                    self.photoLabel.pack(side="top", pady=8, anchor="center") 
                                
                self.PInfoLabel= tk.Label(self.OnePlayer_frame, bg= "bisque2")
                self.PInfoLabel.pack(side= "top", pady=4)
                self.PInfoLabel.configure(text="球員姓名："+players[i][0]+" "+players[i][1]+"\n"+ "隊中位置："+players[i][2])
            
            # 下場比賽
            self.FutureGame_frame = tk.Frame(self.container, bg="old lace",width = 1000, height = 110)
            self.FutureGame_frame.pack(side= "top", anchor="w",fill="both", expand=True)
            NextGameLabel_text = "\n"+"下"+"\n"+"場"+"\n"+"比"+"\n"+"賽"+"\n"
            self.FGLabel=tk.Label(self.FutureGame_frame, text=NextGameLabel_text, font=("標楷體", 18), bg="bisque2")
            self.FGLabel.pack(side= "left", anchor="w", ipady = 5, ipadx = 10)
            
            self.FG=tk.Label(self.FutureGame_frame, text=games[0][0]+" "+games[0][2]+"   "+team_name+" vs. "+games[0][1], bg="old lace", font=("標楷體", 15))
            self.FG.pack(side= "left", anchor="w", ipadx = 30)
            
            # 近期賽事
            self.RecentGame_frame = tk.Frame(self.container, bg="bisque2",width = 1000, height = 110)
            self.RecentGame_frame.pack(side= "top", anchor="w",fill="both", expand=True)
            RecentGameLabel_text = "\n"+"近"+"\n"+"期"+"\n"+"賽"+"\n"+"事"+"\n"            
            self.RecentGameLabel=tk.Label(self.RecentGame_frame, text=RecentGameLabel_text, font=("標楷體", 18), bg="old lace")
            self.RecentGameLabel.pack(side= "left", anchor="w", ipady = 5, ipadx = 10)
            
            for game in games[1:-2]:
                self.GInfoLabel= tk.Label(self.RecentGame_frame, bg="bisque2")

                if int(game[2])>int(game[3]):
                    result="勝"
                else:
                    result="敗"
                self.GInfoLabel.configure(text=game[0]+" "+result+"\n"+game[2]+" vs. "+game[3]+"\n"+"對手："+game[1], font=("標楷體", 12))
                self.GInfoLabel.pack(side= "left", anchor="w", ipadx = 30)

       
        
        # 打開隊伍資訊
        self.Team_name_List = ["亞特蘭大老鷹", "布魯克林籃網", "波士頓塞爾蒂克", "夏洛特黃蜂", "芝加哥公牛",
                             "克里夫蘭騎士", "達拉斯獨行俠", "丹佛金塊","底特律活塞", "金州勇士", 
                             "休士頓火箭","印第安納溜馬", "洛杉磯快艇", "洛杉磯湖人", "曼菲斯灰熊", 
                             "邁阿密熱火", "密爾瓦基公鹿", "明尼蘇達灰狼", "紐奧良鵜鶘", "紐約尼克",
                             "奧克拉荷馬城雷霆", "奧蘭多魔術", "費城76人","鳳凰城太陽", "波特蘭拓荒者", 
                             "沙加緬度國王","聖安東尼奧馬刺", "多倫多暴龍", "猶他爵士", "華盛頓巫師"] 
        
        # 儲存圖片，避免圖片因為for loop消失
        self.Logo_image_list=[]
        
        # 每五個button排在一個列(一個frame裡面)裡面
        Frame_List = []
        
        
        f0=tkFont.Font(family="微軟正黑體", size=10)
        # 用for loop在隊伍頁面建立button
        for i in range(30):
            
            # 用image抓取png檔並resize
            self.Logo_image = Image.open(Logo_road_list[i])
            self.Logo_image = self.Logo_image.resize((90, 90), Image.ANTIALIAS)
            # 用「ImageTk.PhotoImage」轉換成tk可以讀的樣子
            self.Logo_image = ImageTk.PhotoImage(image = self.Logo_image)
            self.Logo_image_list.append(self.Logo_image)
        
            # 每十個建立新的Frame
            if i % 10 == 0:
                self.team_frame = tk.Frame(self.F2, bg = "bisque2",width = 1000, height = 120)
                Frame_List.append(self.team_frame)
                self.team_frame.pack(side = "top", pady = 8, padx = 20, anchor = "n", fill = "x", expand = True)  
            
            # 建立隊伍button
            self.button_logo = tk.Button(self.team_frame, text=self.Team_name_List[i], font=f0, bg = "old lace", image = self.Logo_image_list[i], compound="bottom")
            
            # click_team_button 這個是打開指令的函數
            # command接執行的動作，lambda代表這個動作會在被按下的時候才執行（一定要加上i=i）
            self.button_logo.configure(command = lambda i=i:click_team_button(self.Team_name_List[i]))
            self.button_logo.pack(side = "left", pady = 12, padx = 10, anchor = "w", expand = True)
            # instance method Disabled前加self?不加？
            # self.button.bind('<Button-1>', lambda:Disabled(self.button))


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "old lace")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        

        if len(final_g) % 3 == 0:
            GameHeight = 150 * (len(final_g)//3) + 80
        else:
            GameHeight = 150 * (len(final_g)//3 + 1) + 80
        

        
        self.F2=tk.Frame(self, width=1200, height=GameHeight, bg = "old lace")
        self.F2.pack(side="top", fill="both", expand="TRUE")
        
        """
        self.F2_canvas = tk.Canvas(self, width = 500, height = GameHeight, bg = "old lace", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "old lace", width = 500, height = GameHeight)
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((0,0), window = self.F2, anchor = "nw") 
        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)
        """
        
        f1=tkFont.Font(size=20, family="標楷體")
        print(final_g)
        if len(final_g) > 0:
            # 抓明天的時間
            yesterday=datetime.datetime.now()+datetime.timedelta(days=1)    
            dstr=yesterday.strftime("%Y/%m/%d")
            self.Title=tk.Label(self.F2, text="明日賽事下注"+"("+dstr+")", font=f1, bg="old lace")
            self.Title.pack(side="top", anchor="n", pady = 15, expand=True)
            
            Frame_List = []
            
            for i in range(len(final_g)):
                
                # 每三個建立新的Frame
                if i % 3 == 0:
                    self.game_frame = tk.Frame(self.F2, bg = "bisque2",width = 500, height = 120)
                    Frame_List.append(self.game_frame)
                    self.game_frame.pack(side = "top", pady = 5, padx = 20, anchor = "n", fill = "x", expand = True)  
                
                self.btn=tk.Button(self.game_frame, height=5, width=40, relief = "raised", bg="ivory2")
                time=final_g[i][0]
                teamA=final_g[i][1]  
                teamB=final_g[i][2]
                arena=final_g[i][3]
                self.btn.configure(text=time+"\n"+teamA+"vs."+teamB+"\n"+arena, font="標楷體")
                self.btn.configure(command=lambda i=i: self.click_game_button(final_g[i])) 
                self.btn.pack(side="left", pady=20, padx=20, expand=True)

        else:
            self.NoGameLabel=tk.Label(self.F2, text="明日無賽事", font=f1, bg="old lace")
            self.NoGameLabel.pack(anchor="n", side="top", pady=15)

    # 點擊打開賽事下注
    def click_game_button(self, game_info):
        
        time  = game_info[0]
        teamA = game_info[1]  
        teamB = game_info[2]
        arena = game_info[3]
        
        # 可能跟隊伍team.py之後會修出來的東西要調整
        game_bet=gamebet()
        self.Odds=game_bet.odds(teamA, teamB)
        
        # 彈出視窗的基本介面
        window=tk.Toplevel(self)
        window.geometry("650x500")
        window.configure(bg="azure")
        self.window = window
        self.GameCanv = tk.Canvas(self.window, width=500, height = 500, highlightthickness=0, bg="azure")
        self.GameCanv.pack(side = "top", fill = "both", expand=True)
        self.GameFrame = tk.Frame(self.GameCanv, bg = "bisque2", width=500, height = 500)
        self.GameFrame.pack(side = "left", fill = "both", anchor="nw", expand=True)
        self.showL = tk.Label(self.GameFrame, bg="white", width=10, height = 10)
        self.showL.grid(row=0, column=0, columnspan=30, rowspan=6, padx=5, pady=5, sticky = "nsew")

        # 以下為所有按鈕跟label！！！
        # 單雙
        self.GL1=tk.Label(self.GameFrame, bg="linen", text="單雙（總分）")
        self.GL1.grid(row=7, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB1 = tk.Button(self.GameFrame, bg="lavender blush", text="單   1.75", command=self.clickBtnGB1)
        self.GB1.grid(row=8, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB2 = tk.Button(self.GameFrame, bg="lavender blush", text="雙   1.75", command=self.clickBtnGB2)
        self.GB2.grid(row=8, column=10, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        # 大小
        self.GL2=tk.Label(self.GameFrame, bg="linen", text="大小（總分）")
        self.GL2.grid(row=9, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB3 = tk.Button(self.GameFrame, bg="lavender blush", text=str(self.Odds[1][1])+"  1.75", command=self.clickBtnGB3)
        self.GB3.grid(row=10, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB4 = tk.Button(self.GameFrame, bg="lavender blush", text=str(self.Odds[1][3])+"  1.75", command=self.clickBtnGB4)
        self.GB4.grid(row=10, column=10, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        # 不讓分
        self.GL3= tk.Label(self.GameFrame, bg="linen", text="不讓分")
        self.GL3.grid(row=11, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB5=tk.Button(self.GameFrame, bg="lavender blush", text=str(self.Odds[2][1])+"  "+str(self.Odds[2][2]),command=self.clickBtnGB5)
        self.GB5.grid(row=12, column=0, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        self.GB6=tk.Button(self.GameFrame, bg="lavender blush", text=str(self.Odds[2][3])+"  "+str(self.Odds[2][4]),command=self.clickBtnGB6)
        self.GB6.grid(row=12, column=10, ipadx=2, pady=3, columnspan=9, sticky = "nsew")
        
        # 取消跟確認下注
        self.cancelBtn=tk.Button(self.GameFrame, bg="AntiqueWhite1", text="清除", command=self.clickcancelBtn)
        self.cancelBtn.grid(row=13, column=8, columnspan=5, padx=5, pady=20, sticky="nsew")
        self.okBtn=tk.Button(self.GameFrame, bg="AntiqueWhite1", text="確定",command=self.clickokBtn)
        self.okBtn.grid(row=13, column=14, columnspan=5, padx=5, pady=20, sticky="nsew")
        self.betBtn=tk.Button(self.GameFrame, bg="AntiqueWhite1", text="確認下注",command=lambda:[self.clickbetBtn(), self.controller.user_info_modify(), self.close_window()], state = "disabled")
        self.betBtn.grid(row=13, column=20, columnspan=5, padx=5, pady=20, sticky="nsew")
        
        # 輸入下注數的地方
        self.betnumLbl=tk.Label(self.GameFrame, text="下注數量：", justify="left", bg = "bisque2")
        self.betnumLbl.grid(row=4, column=41, columnspan=5, pady=5, padx=5, sticky = "nsew")
        self.var_betnum=tk.StringVar()
        self.betnumEnt=tk.Entry(self.GameFrame, textvariable=self.var_betnum)
        self.betnumEnt.grid(row=4, column=46, columnspan=3, pady=5, padx=5, sticky = "nsew")
        
        # 目前下注資訊顯示
        self.Words=tk.Label(self.GameFrame, text="個組合，每組合投注金額10元x", justify="left", bg = "bisque2")
        self.Words.grid(row=5, column=41, columnspan=2, pady=5, padx=5, sticky = "nsew")
        self.Words2=tk.Label(self.GameFrame, text="最高可中：", justify="left", bg = "bisque2")
        self.Words2.grid(row=6, column=41, columnspan=2, pady=5, padx=5, sticky = "nsew")
        
        # 回傳的東西們（0時間，1隊伍A，2隊伍B，3場地，4下注種類，5下注方，6賠率，7下幾注，8sure）
        self.bet_one_list = [time, teamA, teamB, arena, 0, 0, 0, 0, 0]
        self.bet_two_list = [time, teamA, teamB, arena, 0, 0, 0, 0, 0]
        self.bet_three_list = [time, teamA, teamB, arena, 0, 0, 0, 0, 0]
        self.bet_lists = []
        self.bet_lists.append(self.bet_one_list)
        self.bet_lists.append(self.bet_two_list)
        self.bet_lists.append(self.bet_three_list)
        # print(self.bet_lists)
        
    # 確認（關視窗）儲存所有下注內容
    # 每點一次按鈕都要確認一次顯示幕上的東西
    def clickBtnGB1(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"單雙（總分）　　單  　　　　　1.75", justify="left")
        self.GB1.configure(state="disabled")
        self.GB2.configure(state="disabled")
        self.bet_lists[0][4] = "單雙（總分）"
        self.bet_lists[0][5] = "單"
        self.bet_lists[0][6] = 1.75
        self.bet_lists[0][8] = 1
    def clickBtnGB2(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"單雙（總分）　　雙  　　　　　1.75", justify="left")
        self.GB1.configure(state="disabled")
        self.GB2.configure(state="disabled")
        self.bet_lists[0][4] = "單雙（總分）"
        self.bet_lists[0][5] = "雙"
        self.bet_lists[0][6] = 1.75
        self.bet_lists[0][8] = 1
    def clickBtnGB3(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"大小（總分）　　"+str(self.Odds[1][1])+"　　  1.75", justify="left")
        self.GB3.configure(state="disabled")
        self.GB4.configure(state="disabled")
        self.bet_lists[1][4] = "大小（總分）"
        self.bet_lists[1][5] = self.Odds[1][1]
        self.bet_lists[1][6] = 1.75
        self.bet_lists[1][8] = 1
    def clickBtnGB4(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"大小（總分）　　"+str(self.Odds[1][3])+"　　  1.75", justify="left")
        self.GB3.configure(state="disabled")
        self.GB4.configure(state="disabled")
        self.bet_lists[1][4] = "大小（總分）"
        self.bet_lists[1][5] = self.Odds[1][3]
        self.bet_lists[1][6] = 1.75
        self.bet_lists[1][8] = 1
    def clickBtnGB5(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"不讓分　　　　　"+str(self.Odds[2][1])+"  "+str(self.Odds[2][2]), justify="left")
        self.GB5.configure(state="disabled")
        self.GB6.configure(state="disabled")
        self.bet_lists[2][4] = "不讓分"
        self.bet_lists[2][5] = self.Odds[2][1]
        self.bet_lists[2][6] = self.Odds[2][2]
        self.bet_lists[2][8] = 1
    def clickBtnGB6(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"不讓分　　　　　"+str(self.Odds[2][3])+"  "+str(self.Odds[2][4]), justify="left")
        self.GB5.configure(state="disabled")
        self.GB6.configure(state="disabled")
        self.bet_lists[2][4] = "不讓分"
        self.bet_lists[2][5] = self.Odds[2][3]
        self.bet_lists[2][6] = self.Odds[2][4]
        self.bet_lists[2][8] = 1
        
    # 取消用的函數（一次全部取消）
    def clickcancelBtn(self):
        self.GB1.configure(state="normal")
        self.GB2.configure(state="normal")
        self.GB3.configure(state="normal")
        self.GB4.configure(state="normal")
        self.GB5.configure(state="normal")
        self.GB6.configure(state="normal")
        self.showL.configure(text="") 
        self.betnumEnt.delete(0,"end")
        for one_list in self.bet_lists:
            for i in range(4, 9):
                one_list[i] = 0

    
    # 這邊是確認函數
    def clickokBtn(self):
        """
        下注組希望回傳的資訊形式
        （0時間，1隊伍A，2隊伍B，3場地，4下注種類，5下注方，6賠率，7下幾注）
        """
        self.total_Odds = 0
        # 確認結果
        self.report_list = []
        for one_list in self.bet_lists:
            if one_list[8] == 1:
                the_one_list = one_list[0:-1]
                self.total_Odds += the_one_list[6]
                self.report_list.append(the_one_list)
        
        if len(self.report_list) == 0:
            tk.messagebox.showwarning("Warning", "你尚未選擇任何下注方法！")
        else:
            try:
                self.betnum=self.betnumEnt.get()
                self.betnum = int(self.betnum)
                
                if self.betnum < 0:
                    tk.messagebox.showwarning("Warning", "「下注數量」請輸入正整數！")
                    tk.betnumEnt.delete(0,"end")
                
                # 有選擇下注，並且輸入正確數字後，回傳list並關閉視窗
                else:
                    for i in range(len(self.report_list)):
                        self.report_list[i][7]=self.betnum
                    
                    # 按確認後改
                    content=self.Words.cget("text")
                    self.Words.configure(text=str(len(self.report_list))+content+str(self.betnum))
                    content2=self.Words2.cget("text")
                    Max = self.total_Odds * 10 * self.betnum
                    Max = number_float_check(Max)
                    self.Words2.configure(text=content2+str(Max))
                    
                    # 鎖定所有按鍵
                    try:
                        self.GB1.configure(state="disabled")
                        self.GB2.configure(state="disabled")
                        self.GB3.configure(state="disabled")
                        self.GB4.configure(state="disabled")
                        self.GB5.configure(state="disabled")
                        self.GB6.configure(state="disabled")
                        self.cancelBtn.configure(state="disabled")
                        self.okBtn.configure(state="disabled")
                        self.betnumEnt.configure(state="disabled")
                        self.betBtn.configure(state="normal")
                    except:
                        pass
            
            except:
                tk.messagebox.showwarning("Warning", "請輸入「下注數量」！")
                self.betnumEnt.delete(0,"end")
        
    def clickbetBtn(self):
        bet_list=self.report_list

        # 第一次登入或沒有任何下注紀錄時，需要在第五個加入空集合
        if len(user_info) != 5:
            user_info.append([])
        else:
            pass
        confirm_bet(bet_list)
        save_csv(username)
        print("Bet confirmed!")

        
    def close_window(self):
        self.window.destroy()

           
# HistoryPage歷史紀錄頁面

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # 抓昨天的時間
        yesterday=datetime.datetime.now()-datetime.timedelta(days=1)    
        dstr=yesterday.strftime("%Y/%m/%d")
        hist = history()
        hist.update()
        final_h = hist.get_data(dstr)
        
        
        self.configure( width = 1200, height = ( 150 + 220 * len(final_h) ), bg = "old lace")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        
        self.F2_canvas = tk.Canvas(self, width = 500, height = ( 150 + 220 * len(final_h) ), bg = "old lace", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "old lace", width = 1200, height = ( 150 + 220 * len(final_h) ))
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((0,0), window = self.F2, anchor = "n") 

        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)

        # print(final_h)
        f1=tkFont.Font(size=20, family="標楷體")
        f2=tkFont.Font(size=15, family="Didot")

        
        if len(final_h) == 0:
            self.lbl=tk.Label(self.F2_canvas, text="昨日無賽事"+"("+dstr+")", font=f1, bg="old lace")
            self.lbl.pack(side="top", anchor="center", pady=15)
        else:
            self.Title=tk.Label(self.F2_canvas, text="昨日賽事"+"("+dstr+")", font=f1, bg="old lace")
            self.Title.pack(side="top", anchor="n", pady=15)
            for i in range(len(final_h)):
                self.lbl=tk.Label(self.F2_canvas, width=40, text=str(i+1)+"\n"+"時間："+final_h[i][1]+"\n"+"客隊："+final_h[i][2]+" "+final_h[i][4]+"\n"+"主隊："+final_h[i][3]+" "+final_h[i][5]+"\n"+"賽場："+final_h[i][6])
                self.lbl.configure(font=f2, bg="old lace", justify="center")
                self.lbl.pack(side="top", pady=5, anchor="center")
            self.F2_canvas.configure(height = 120 * len(final_h))

    
class PersonalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg="old lace")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        
        self.F2_canvas = tk.Canvas(self, width = 500, height = 600, bg = "old lace", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "old lace", width = 500, height = 600)
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((0,0), window = self.F2, anchor = "nw") 
        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)        
        
    def modify(self):
        # 全部的使用者資訊
        # user_information = []
        # 抓到同帳號名使用者的資訊
        
        global user_info
        user_info=[]
        df=pd.read_csv(infopath)
        usr_info_df=df[df['Username'] == username]
        user_info_tolist=usr_info_df.values.tolist()
        user_info=user_info_tolist[0]
        # 登入時要計算之前的下注紀錄
        login_duty()
        save_csv(username)
        
        """建立東西"""
        self.F2_canvas.destroy()
        self.F2_canvas = tk.Canvas(self, width = 500, height = 130 + 187.5 * len(user_info[4]), bg = "old lace", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "old lace", width = 500, height = 130 + 187.5 * len(user_info[4]))
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((0,0), window = self.F2, anchor = "nw") 
        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)
        
        self.UsernameLbl = tk.Label(self.F2, text = "Hello, "+username+"."+" Your account balance is "+str(user_info[2])+".", font = ("標楷體", 18), bg = "old lace")
        self.UsernameLbl.pack(side="top", anchor= "nw", pady= 20, padx=20)
        
        # 下注資訊紀錄：等改

        # 我就先推測i是下注的次數？
        # 疑問：這個user_info跑進來後，第一筆會是時間最早還是最新？
        # 只顯示近十筆？下注如果超過一百筆可能會超過scrollbar可以滑的範圍
        
        f1=tkFont.Font(family="標楷體", size=15)
        
        if user_info[4] == []:
            self.ShowLbl=tk.Label(self.F2, text = "尚無下注紀錄", font = f1, bg = "old lace")
            self.ShowLbl.pack(side="top", anchor="w" , padx=20)
        
        else: # 有下注資訊
            # for game in user_info[4]:
            #     game = ast.literal_eval(game)
            self.BetLbl = tk.Label(self.F2, text="您有"+ str(len(user_info[4]))+"筆下注紀錄", font = f1 , bg="old lace")
            self.BetLbl.pack(side="top", anchor= "nw", pady= 20, padx=20)
            for i in range(len(user_info[4])):
                
                record_text =  (str(i+1)+"."+"\n"+
                                "下注時間： "+user_info[4][i][10]+"\n"+
                                "狀態： "+user_info[4][i][8]+"\n"+
                                "賽事： "+user_info[4][i][0]+" "+user_info[4][i][1]+" vs."+user_info[4][i][2]+" @"+user_info[4][i][3]+"\n"+
                                "賭法： "+user_info[4][i][4]+"\n"+
                                "方向： "+user_info[4][i][5]+"\n"+
                                "賠率： "+str(user_info[4][i][6])+"\n"+
                                "下注數： "+str(user_info[4][i][7])
                                )
                self.BetIndexLbl=tk.Label(self.F2, text=record_text, font = f1, bg = "old lace", justify="left")
                self.BetIndexLbl.pack(side="top", anchor="w", padx=20, pady = 10)
                
                
                """
                # 下注第幾筆
                self.BetIndexLbl=tk.Label(self.F2, text=str(i+1)+".", font = f1, bg = "old lace")
                self.BetIndexLbl.pack(side="top", anchor="w",padx=20)
                # 下注時間
                # time = user_info[4][i][10]
                # tstr=time.strftime(time, "%Y-%m-%d %H:%M")  
                self.BetTimeLbl=tk.Label(self.F2, text = "下注時間： "+user_info[4][i][10], font = f1, bg="old lace")
                self.BetTimeLbl.pack(side="top", anchor="w", padx=20)
                # 下注狀態
                self.StatusLbl=tk.Label(self.F2, text="狀態： "+user_info[4][i][8], font=f1, bg="old lace") 
                self.StatusLbl.pack(side="top", anchor="w", padx=20)
                # 下注賽事資訊
                self.GameLbl=tk.Label(self.F2, text="賽事： "+user_info[4][i][0]+" "+user_info[4][i][1]+" vs."+user_info[4][i][2]+" @"+user_info[4][i][3], font=f1, bg="old lace")
                self.GameLbl.pack(side="top", anchor="w", padx=20)
                # 賭法
                self.WayLbl=tk.Label(self.F2, text="賭法： "+user_info[4][i][4], bg="old lace", font=f1)
                self.WayLbl.pack(side="top", anchor="w", padx=20)
                # 方向 什麼方向？我直接寫direction...
                self.DirectLbl=tk.Label(self.F2, text="方向： "+user_info[4][i][5], bg="old lace", font=f1)
                self.DirectLbl.pack(side="top", anchor="w", padx=20)
                # 賠率
                self.OddsLbl=tk.Label(self.F2, text="賠率： "+str(user_info[4][i][6]), bg="old lace", font=f1)
                self.OddsLbl.pack(side="top", anchor="w", padx=20)
                # 下注數
                self.BetNumLbl=tk.Label(self.F2, text="下注數： "+str(user_info[4][i][7]), bg="old lace", font=f1)
                self.BetNumLbl.pack(side="top", anchor="w", padx=20)
                """

app=SportsLottery()
app.mainloop()