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

# 以下為試class的功能
wounded = wounded()
final_w = wounded.get_news()

# 抓賽事頁面（不會跳瀏覽器）
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
        driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver', options=chrome_options)
        # executable_path = '/usr/local/bin/chromedriver'
        # executable_path = 'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python37\\chromedriver.exe'
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
                today = datetime.date.today()
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

# 以下為試class的功能
bet = bet()
final_g = bet.get_data()

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
        self.driver = webdriver.Chrome( executable_path = '/usr/local/bin/chromedriver', options=chrome_options)
        self.driver.get('https://tw.global.nba.com/schedule/#!/7')
        # executable_path = '/usr/local/bin/chromedriver'
        # executable_path = 'chromedriver.exe'

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
                
                filepath = 'C:\\Users\\user\\Downloads\\data.csv'
                # 
                # 'C:\\Users\\user\\Downloads\\data.csv'
                wf = open(file=filepath, mode="a+",newline='', encoding="utf-8")
                writer = csv.writer(wf)
                rf = open(file=filepath, mode="r", encoding="utf-8")
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
        filepath = "/Users/yangqingwen/Downloads/data.csv" 
        # "/Users/yangqingwen/Downloads/data.csv" 
        # 'C:\\Users\\user\\Downloads\\data.csv'
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

# 抓各個隊伍資訊
"""
class Team:
"""

"""
待修
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
        print("***calculating odds...")
        data_list = []
        
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
        
        #獲得雙方隊伍勝率與平均得分
        print("getting team", team_name_A, "stats...")
        teamA = Team(team_name_A)
        teamA.get_info() #勝率是int(teamA.info[4])
        self.win_oddsA = (float(teamA.info[4][:(len(teamA.info[4])-1)]) / 100)
        teamA.get_game() #平均得分是teamA.game[(len(teamA.game) - 1)]
        self.score_A = teamA.game[(len(teamA.game) - 1)]
        
        print("getting team", team_name_B, "stats...")        
        teamB = Team(team_name_B)
        teamB.get_info() #勝率B是int(teamB.info[4])
        self.win_oddsB = (float(teamB.info[4][:(len(teamB.info[4])-1)]) / 100)
        teamB.get_game() #平均得分是teamB.game[(len(teamB.game) - 1)]
        self.score_B = teamB.game[(len(teamB.game) - 1)]
        
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
        data_list.append(['單雙', '單', 1.75, '雙', 1.75])
        
        #大小
        scoresum = teamA.game[(len(teamA.game) - 1)] + teamB.game[(len(teamB.game) - 1)]
        scoresum = int(scoresum) + 0.5 #確保大小是以.5結尾
        data_list.append(['大小(總分)', ('大於' + str(scoresum)), 1.75,
                          ('小於' + str(scoresum)), 1.75])
        
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
    
    """
    def get_bettingA(final_g) ，需要輸入當日賽程清單
    return list：一場賽事回傳一個完整賠率清單
    舉例：[['時間', 'A隊', 'B隊', '地點', [[單雙], [大小], [不讓分]]],
           ['時間', 'C隊', 'D隊', '地點', [[單雙], [大小], [不讓分]]]...]
    
    A版本使用For迴圈一個一個計算，算出全部的賠率，非常耗時間。
    """
    def get_bettingA(self, final_g):
        #先得到當日賽事資訊
        data_list = []
        
        #Team與bet對照隊名用
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
        
        #for迴圈判定賠率
        for i in range(len(final_g)):
            data_list.append(final_g[i])
            print('***Getting game of', teamnamedict[final_g[i][1]],"vs.", teamnamedict[final_g[i][2]])
            odds_list = self.odds(teamnamedict[final_g[i][1]], teamnamedict[final_g[i][2]])
            data_list[i].append(odds_list)
            print('***Check list', data_list[i])
            print()
            print()
        
        return data_list

    #判斷下幾注，賠率
    """
    三種寫法分別對應不同的結果?
    """
    #def go_bet(self):
        
    
    #下注
    """
    def gobet 需要輸入一個清單：['時間', 'A隊', 'B隊', '地點', '賭法', '下幾柱']
    - 從帳戶扣除應繳金額
    - 新增一筆交易資料，此交易資料會是一個清單：
      ['時間', 'A隊', 'B隊', '地點', '賭法', '下幾柱', '輸/贏/未交割', 盈虧]
    - 回傳
    """
    #def confirm_bet(self, bet):
        #需要一個Check Balance的函數
        
        
        #從帳戶扣取應繳金額
        #新增一筆交易資料
        
        
    #結算
    """
    def clearance 不須輸入
    每次開檔時需跑這個函數
    - 從帳戶資料中讀取是否有未交割的賭注
    - 從歷史資料中獲得結果
    - 更新帳戶餘額與交易紀錄
    """   
    #def clearance(self): 



"""前台主程式開始"""

#  SportsLottery相當於開一個主視窗
class SportsLottery(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("300x300")
        self.title("運彩模擬器")
        self.frames = {}
        # self.canvas=tk.Canvas(self, width=500, height=1000)
        # self.canvas.pack(fill=BOTH,expand=Y)
        # canvas.configure(bg="misty rose")
        
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
    def user_info_modify(self, username):
        PersonalPage=self.frames["PersonalPage"]
        PersonalPage.modify(username)




class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.title("運彩模擬器：登入")
        self.configure(bg="misty rose")
       
        # self.img=Image.open("NBALogo.gif")
        # self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        # self.img=ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)
    
        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self, text="使用者名稱：", font=f1, bg="snow")
        self.l2=tk.Label(self, text="密碼：", font=f1, bg="snow")
        self.l1.pack(side="top", padx=10, pady=10)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side="top",padx=10, pady=10) 

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
        # filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
        userinformation = []
        try:
            with open('/Users/yangqingwen/Downloads/userInformation.csv', "r", newline = '') as f:
                rows = csv.reader(f)
                for row in rows:
                    userinformation.append(row)
        except:
           pass
        # 檢查是否有此帳號
        global username
        global password 
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
                self.controller.show_frame("NewsPage")
                self.controller.user_info_modify(username)
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
            # filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
            userinformation = []
            with open('/Users/yangqingwen/Downloads/userInformation.csv', "r", newline = '') as f:
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
            # filepath = '/Users/yangqingwen/Downloads/userInformation.csv'
            # "C:\\co-work\\userInformation.csv"
            with open('/Users/yangqingwen/Downloads/userInformation.csv', "a+", newline='') as f:
                writer=csv.writer(f)
                writer.writerow([username, password, start_money, login_time])
                f.close()
            self.entry_usr_name.delete(0, "end")
            self.entry_usr_pwd.delete(0,"end")
            tk.messagebox.showinfo("Info", "User successfully registered.\nPlease log in.")


# 登入後五個頁面共同的板塊建立方式
def create_common_frames(self, controller):

    self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
    self.F1.pack(side="top", fill="both")
    
    functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
    for function in reversed(functions):
        self.btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
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

    self.F2_canvas = tk.Canvas(self, width = 500, height = 600, bg = "lemon chiffon", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
    self.F2_canvas.pack(side = "top",fill = "both", expand = True)
    
    # 要建立frame，透過create_widget放在canvas上面才能滾動
    self.F2 = tk.Frame(self.F2_canvas, bg = "lemon chiffon", width = 500, height = 1200)
    self.F2.pack(side = "top", fill = "both" ,expand = True)
    self.F2_canvas.create_window((200,200), window = self.F2, anchor = "nw") 

    # 滾動條
    self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
    self.gameBar.pack(side = "right", fill = "y")
    self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)


# NewsPage新聞頁
class NewsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller=controller
        self.configure(bg="lemon chiffon",width=500, height=700)
        
        # self.pack(side=BOTTOM, expand=TRUE)
        # welcome page
        self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
        self.F1.pack(side="top", fill="both",anchor="n")
        self.F2=tk.Frame(self,bg="sienna4",width=500, height=700)
        self.F2.pack(side="top", fill="both", expand="TRUE")
        self.FN=tk.Frame(self.F2,bg="lemon chiffon",width=250, height=700)
        self.FN.pack(side="left", anchor="w",fill="both", expand="TRUE")
        self.FW=tk.Frame(self.F2, bg="floral white", width=300, height=700)
        self.FW.pack(side="left",fill="both", expand="TRUE")
        functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
        for function in reversed(functions):
            btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
            btn.pack(side="right", pady=30, anchor="n")
            btn_txt=btn.cget("text")
            if btn_txt == "球隊介紹":
                btn.configure(command=lambda: controller.show_frame("TeamPage"))
            elif btn_txt == "新聞介紹":
                btn.configure(command=lambda: controller.show_frame("NewsPage"))
            elif btn_txt == "個人帳戶":
                btn.configure(command = lambda: controller.show_frame("PersonalPage"))
            elif btn_txt == "歷史資料":
                btn.configure(command=lambda: controller.show_frame("HistoryPage"))
            elif btn_txt == "賽事下注":
                btn.configure(command = lambda: controller.show_frame("GamePage"))


        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl=tk.Label(self.FN, text="最新消息", font=f0, bg="lemon chiffon")
        self.TitleLbl.pack(side="top")
        for one_news in final_n:
            title=one_news[0]
            time=one_news[1]
            intro=one_news[2]
            if 20<=len(intro)<=40:
                intro=intro[:20]+"\n"+intro[21:]
            elif 40<=len(intro):
                intro=intro[:20]+"\n"+intro[21:40]+"\n"+intro[41:]
            
            image_url=one_news[-1]
            ssl._create_default_https_context = ssl._create_unverified_context
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()
            self.img = Image.open(BytesIO(raw_data))
            self.img=self.img.resize((200, 100), Image.ANTIALIAS) 
            self.img=ImageTk.PhotoImage(self.img)
            self.picLabel = tk.Label(self.FN,image=self.img)
            self.picLabel.image = self.img
            self.picLabel.pack(side="top", pady=10, padx=10, anchor="w") 
            
            f1=tkFont.Font(size=20, family="標楷體")
            f2=tkFont.Font(size=10, family="微軟正黑體")
            self.btn=tk.Label(self.FN, text=title, font=f1,bg="lemon chiffon", cursor="hand2")
            self.btnsmall=tk.Label(self.FN, text=time+"\n"+intro,font=f2, bg="lemon chiffon", justify="left") # 傷兵/justify=RIGHT
            
            def callback(event):
                webbrowser.open_new(one_news[-2])
            self.btn.bind("<Button-1>", callback)
            self.btnsmall.bind("<Button-1>", callback)
            self.picLabel.bind("<Button-1>", callback)
            self.btn.pack(side="top", pady=2,padx=10, anchor="w") # 傷兵：anchor=E
            self.btnsmall.pack(side="top",pady=2,padx=10, anchor="w") # 傷兵：anchor=E
        
        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl=tk.Label(self.FW, text="傷兵資訊", font=f0, bg="floral white")
        self.TitleLbl.pack(side="top")
        
        for one_wounded in final_w:
            title=one_wounded[0]
            time=one_wounded[1]
            intro=one_wounded[2]
            if 20<=len(intro)<=40:
                intro=intro[:20]+"\n"+intro[21:]
            elif 40<=len(intro):
                intro=intro[:20]+"\n"+intro[21:40]+"\n"+intro[41:]
            
            image_url=one_wounded[-1]
            ssl._create_default_https_context = ssl._create_unverified_context
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()
            self.img = Image.open(BytesIO(raw_data))
            self.img=self.img.resize((200, 100), Image.ANTIALIAS) 
            self.img=ImageTk.PhotoImage(self.img)
            self.picLabel = tk.Label(self.FW,image=self.img)
            self.picLabel.image = self.img
            self.picLabel.pack(side="top", pady=10, padx=10, anchor="w") 
            
            f1=tkFont.Font(size=20, family="標楷體")
            f2=tkFont.Font(size=10, family="微軟正黑體")
            self.btn=tk.Label(self.FW, text=title, font=f1,bg="floral white",cursor="hand2")
            self.btnsmall=tk.Label(self.FW, text=time+"\n"+intro,font=f2, bg="floral white", justify="left") 
            
            def callback(event):
                webbrowser.open_new(one_wounded[-2])
            self.btn.bind("<Button-1>", callback)
            self.btnsmall.bind("<Button-1>", callback)
            self.picLabel.bind("<Button-1>", callback)
            self.btn.pack(side="top", pady=2,padx=10, anchor="w") # 傷兵：anchor=E
            self.btnsmall.pack(side="top",pady=2,padx=10, anchor="w") # 傷兵：anchor=E

class TeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "lemon chiffon")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        self.createWidgets()
        
    def createWidgets(self):
        # 放賽事
        f0=tkFont.Font(family="標楷體", size=20)
        self.TitleLbl=tk.Label(self.F2, text="球隊介紹", font=f0 ,bg="lemon chiffon").pack(side = "top")

        
        # 點按鈕為各隊伍資訊
        def click_team_button(team_name):
            window = tk.Toplevel(self)
            window.title(team_name)
            window.geometry("500x500")
            window.resizable(False, False)
            
            # 以下是有container的scrollbar寫法
            self.container = tk.Frame(window, height=500, width=1000)
            self.container.pack(side="top",fill="both", expand=True)
            self.teamCanv = tk.Canvas(self.container, width=500, height = 2000, highlightthickness=0, bg="wheat2")
            self.teamCanv.pack(side = "top", fill = "both", expand=True)
            teamBar = tk.Scrollbar(self.teamCanv, orient = "vertical", command = self.teamCanv.yview)
            teamBar.pack(side = "right", fill = "y")

            self.scrollableF=tk.Frame(self.teamCanv, bg = "wheat2", width=1000, height = 500)
            self.scrollableF.pack(side = "bottom", fill = "both", anchor="center")
            self.teamCanv.configure(yscrollcommand = teamBar.set)
            self.scrollableF.bind("<Configure>",lambda x: self.teamCanv.configure(scrollregion=self.teamCanv.bbox("all")))
            self.teamCanv.create_window((0, 0), window=self.scrollableF, anchor="nw")
            
            # 視窗的隊伍資訊
            """
            記得改filepath
            """
            filepath = "C:\\co-work\\team.csv"
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
            
            self.Label= tk.Label(self.scrollableF, bg="wheat2")
            self.Label.pack(side= "top", anchor="n")
            self.Label.configure(text="隊伍名稱："+team_info[0]+
                                        "\n"+"教練："+team_info[1]+
                                        "\n"+"分區聯盟："+team_info[2]+
                                        "\n"+"分區排名："+team_info[3]+
                                        "\n"+"勝率："+team_info[4]+"\n"+"\n")
        
            # 名、姓氏、位置、頭像連結 (五個先發各在一個list，包成2-d list回傳)
            self.PlayerLabel=tk.Label(self.scrollableF, text="先發名單", font=("標楷體", 15), bg="peach puff")
            self.PlayerLabel.pack(side= "top", pady=10)
            for i in range(len(players)):
                image_url=players[i][3]
                ssl._create_default_https_context = ssl._create_unverified_context
                
                try:
                    u = urlopen(image_url)
                    raw_data = u.read()
                    u.close()
                    self.playerPhoto = Image.open(BytesIO(raw_data))
                    self.playerPhoto = self.playerPhoto.resize((130, 95), Image.ANTIALIAS) 
                    self.playerPhoto = ImageTk.PhotoImage(self.playerPhoto)
                    self.Photo_list.append(self.playerPhoto)
                    self.photoLabel = tk.Label(self.scrollableF, image=self.Photo_list[i])
                    self.photoLabel.pack(side="top", pady=2, anchor="e")   
                except:
                    self.photoLabel = tk.Label(self.scrollableF, text="No image")
                    self.photoLabel.pack(side="top", pady=2, anchor="e") 
                                
                self.PInfoLabel= tk.Label(self.scrollableF, bg="wheat2")
                self.PInfoLabel.pack(side= "top", pady=5)
                self.PInfoLabel.configure(text="球員姓名："+players[i][0]+" "+players[i][1]+"\n"+ "隊中位置："+players[i][2])
                
            self.FGLabel=tk.Label(self.scrollableF, text="下場比賽", font=("標楷體", 15), bg="peach puff")
            self.FGLabel.pack(side="top", pady=5)
            self.FG=tk.Label(self.scrollableF, text=games[0][0]+"\n"+games[0][2]+"\nvs."+games[0][1], bg="wheat2")
            self.FG.pack(side="top", pady=5)
            self.GameLabel=tk.Label(self.scrollableF, text="近期賽事", font=("標楷體", 15), bg="peach puff")
            self.GameLabel.pack(side="top", pady=5)
            
            for game in games[1:-2]:
                # print(game)
                self.GInfoLabel= tk.Label(self.scrollableF, bg="wheat2")
                if int(game[2])>int(game[3]):
                    result="勝"
                else:
                    result="敗"
                self.GInfoLabel.configure(text=game[0]+"\n"+result+"\n"+game[2]+" vs. "+game[3]+" "+game[1])
                self.GInfoLabel.pack(side= "top", pady=5)


            # 要避免使用者手殘按到很多下爬蟲程式被啟動太多次然後電腦當機嗎
            def Disabled(self, button):
                button.configure(state="disabled")
            def Normalized(self, button):
                self.button.configure(state="normal")
        
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

        # 用for loop在隊伍頁面建立button
        for i in range(30):
            
            # 用image抓取png檔並resize
            self.Logo_image = Image.open(Logo_road_list[i])
            self.Logo_image = self.Logo_image.resize((100, 100), Image.ANTIALIAS)
            # 用「ImageTk.PhotoImage」轉換成tk可以讀的樣子
            self.Logo_image = ImageTk.PhotoImage(image = self.Logo_image)
            self.Logo_image_list.append(self.Logo_image)
        
            # 每五個建立新的Frame
            if i % 5 == 0:
                self.team_frame = tk.Frame(self.F2, bg = "wheat2",width = 1000, height = 120)
                Frame_List.append(self.team_frame)
                self.team_frame.pack(side = "top", pady = 10, padx = 20, anchor = "n", fill = "x")  
            
            # 建立隊伍button
            self.button_logo = tk.Button(self.team_frame, text=self.Team_name_List[i], image = self.Logo_image_list[i], compound="bottom")
            
            # click_team_button 這個是打開指令的函數
            # command接執行的動作，lambda代表這個動作會在被按下的時候才執行（一定要加上i=i）
            self.button_logo.configure(command = lambda i=i:click_team_button(self.Team_name_List[i]))
            self.button_logo.pack(side = "left", pady = 10, padx = 20, anchor = "nw", expand = True)
            # instance method Disabled前加self?不加？
            # self.button.bind('<Button-1>', lambda:Disabled(self.button))


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "lemon chiffon")
        # 登入後五個頁面共同的板塊建立方式
        create_common_frames(self, controller)
        
        
        # 頁面功能 (之後可能要融合到Main_onWindows.py)
        
        f1=tkFont.Font(size=20, family="標楷體")
        if len(final_g)>0:
            for i in range(len(final_g)):
                self.btn=tk.Button(self.F2, height=5, width=50, relief =tk.RAISED, bg="ivory3")
                time=final_g[i][0]
                team1=final_g[i][1]  
                team2=final_g[i][2]
                arena=final_g[i][3]
                self.btn.configure(text=time+"\n"+team1+"vs."+team2+"\n"+arena, font="標楷體")
                self.btn.configure(command=lambda: click_game_button(team1, team2)) 
                self.btn.pack(side="top", pady=10, padx=5)     
        else:
            self.NoGameLabel=tk.Label(text="今日無賽事", font=f1)
            self.NoGameLabel.pack(anchor="n", side="top", pady=20)
       
        
        # 點擊打開賽事下注
        def click_game_button(teamA, teamB):
            # 可能跟隊伍team.py之後會修出來的東西要調整
            game_bet=gamebet()
            Odds=game_bet.odds(teamA, teamB)

            window=tk.Toplevel(self)
            window.geometry("500x500")
            window.configure(bg="azure")
            
            self.GameCanv = tk.Canvas(window, width=500, height = 500, highlightthickness=0, bg="azure")
            self.GameCanv.pack(side = "top", fill = "both", expand=True)
            self.GameFrame = tk.Frame(self.GameCanv, bg = "wheat2", width=500, height = 500)
            self.GameFrame.pack(side = "top", fill = "both", anchor="center", expand=True)
            self.showL = tk.Label(self.GameFrame, bg="white", width=10, height = 10, text="顯示幕")
            self.showL.grid(row=0, column=0, columnspan=8, rowspan=4, padx=5, pady=5, sticky = "nsew")
            # 單雙
            self.GL1=tk.Label(self.GameFrame, bg="linen", text="單雙（總分）")
            self.GL1.grid(row=4, column=0, pady=10, columnspan=2, sticky = "nsew")
            self.GB1 = tk.Button(self.GameFrame, bg="lavender blush", text="單   1.75")
            self.GB1.grid(row=5, column=0, pady=10, columnspan=2, sticky = "nsew")
            self.GB2 = tk.Button(self.GameFrame, bg="lavender blush", text="雙   1.75")
            self.GB2.grid(row=5, column=3, pady=10, columnspan=2, sticky = "nsew")
            # 大小
            self.GL2=tk.Label(self.GameFrame, bg="linen", text="大小（總分）")
            self.GL2.grid(row=6, column=0, columnspan=2, pady=10, sticky = "nsew")
            self.GB3 = tk.Button(self.GameFrame, bg="lavender blush", text=Odds[1][1]+"  1.75")
            self.GB3.grid(row=7, column=0, columnspan=2, pady=10, sticky = "nsew")
            self.GB4 = tk.Button(self.GameFrame, bg="lavender blush", text=Odds[1][3]+"  1.75")
            self.GB4.grid(row=7, column=3, columnspan=2, pady=10, sticky = "nsew")
            # 不讓分
            self.GL3= tk.Label(self.GameFrame, bg="linen", text="不讓分")
            self.GL3.grid(row=8, column=0, columnspan=2, pady=10, sticky = "nsew")
            self.GB5=tk.Button(self.GameFrame, bg="lavender blush", text=str(Odds[2][1])+"  "+str(Odds[2][2]))
            self.GB5.grid(row=9, column=0, columnspan=2, pady=10, sticky = "nsew")
            self.GB6=tk.Button(self.GameFrame, bg="lavender blush", text=str(Odds[2][3])+"  "+str(Odds[2][4]))
            self.GB6.grid(row=9, column=3, columnspan=2, pady=10, sticky = "nsew")
            
# HistoryPage歷史紀錄頁面

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "lemon chiffon")
        create_common_frames(self, controller)
        
        # 抓昨天的時間
        yesterday=datetime.datetime.now()-datetime.timedelta(days=1)    
        dstr=yesterday.strftime("%Y-%m-%d")
        hist = history()
        hist.update()
        final_h = hist.get_data(dstr)
        # print(final_h)
        f1=tkFont.Font(size=20, family="標楷體")
        f2=tkFont.Font(size=15, family="Didot")
        self.Title=tk.Label(self.F2, text="昨日賽事"+"("+dstr+")", font=f1, bg="lemon chiffon")
        self.Title.pack(side="left", anchor="nw")
        if len(final_h) == 0:
            self.lbl=tk.Label(self.F2, text="昨日無賽事", font=("標楷體", 18), bg="lemon chiffon")
            self.lbl.pack(side="top", anchor="center", padx=10)
        else:
            for i in range(len(final_h)):
                self.lbl=tk.Label(self.F2, width=40, text=str(i+1)+"\n"+"時間："+final_h[i][1]+"\n"+"客隊："+final_h[i][2]+" "+final_h[i][4]+"\n"+"主隊："+final_h[i][3]+" "+final_h[i][5]+"\n"+"賽場："+final_h[i][6])
                self.lbl.configure(font=f2, bg="lemon chiffon", justify="center")
                self.lbl.pack(side="top", pady=5, anchor="center")
        
    # def click_game_button(self):
class PersonalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg="lemon chiffon")
        self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
        self.F1.pack(side="top", fill="both")
        
        functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
        for function in reversed(functions):
            self.btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
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

        self.F2_canvas = tk.Canvas(self, width = 500, height = 600, bg = "lemon chiffon", highlightthickness = 0)  #height調整canvas的長度，要手動調（或寫def）
        self.F2_canvas.pack(side = "top",fill = "both", expand = True)
        
        # 要建立frame，透過create_widget放在canvas上面才能滾動
        self.F2 = tk.Frame(self.F2_canvas, bg = "lemon chiffon", width = 500, height = 1200)
        self.F2.pack(side = "top", fill = "both" ,expand = True)
        self.F2_canvas.create_window((200,200), window = self.F2, anchor = "nw") 

        # 滾動條
        self.gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
        self.gameBar.pack(side = "right", fill = "y")
        self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = self.gameBar.set)
    def modify(self, username):
        f1=tkFont.Font(family="Didot", size=30)
        UsernameLbl = tk.Label(self.F2, text="Welcome, "+username, font=f1, bg="lemon chiffon")
        UsernameLbl.pack(side="top", anchor= "center", pady= 20)

        # 帳戶組要給的餘額數字：
        # read csv讀入歷史資訊和帳戶餘額
        # 所有東西要擺在F2的Frame裡面
        self.BalanceLbl=tk.Label(self.F2,text="帳戶餘額："+str(Balance), font=f1, bg="lemon chiffon")
        self.BalanceLbl.pack(side="top", anchor="center",pady=20)

app=SportsLottery()
app.mainloop()
