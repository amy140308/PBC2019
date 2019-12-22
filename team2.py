from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time as t
import csv


class Team:
    def __init__(self, driver, city_name):  # 用字典連動網址，用Chrome打開網站取得原始碼
        # 台灣版網站
        team_url = {"波士頓塞爾蒂克": "https://tw.global.nba.com/teams/#!/celtics", 
                "芝加哥公牛": "https://tw.global.nba.com/teams/#!/bulls", 
                "亞特蘭大老鷹": "https://tw.global.nba.com/teams/#!/hawks", 
                "布魯克林籃網": "https://tw.global.nba.com/teams/#!/nets", 
                "克里夫蘭騎士": "https://tw.global.nba.com/teams/#!/cavaliers", 
                "夏洛特黃蜂": "https://tw.global.nba.com/teams/#!/hornets", 
                "紐約尼克": "https://tw.global.nba.com/teams/#!/knicks", 
                "底特律活塞": "https://tw.global.nba.com/teams/#!/pistons", 
                "邁阿密熱火": "https://tw.global.nba.com/teams/#!/heat", 
                "費城76人": "https://tw.global.nba.com/teams/#!/sixers", 
                "印第安納溜馬": "https://tw.global.nba.com/teams/#!/pacers", 
                "奧蘭多魔術": "https://tw.global.nba.com/teams/#!/magic", 
                "多倫多暴龍": "https://tw.global.nba.com/teams/#!/raptors", 
                "密爾瓦基公鹿": "https://tw.global.nba.com/teams/#!/bucks", 
                "華盛頓巫師": "https://tw.global.nba.com/teams/#!/wizards", 
                "丹佛金塊": "https://tw.global.nba.com/teams/#!/nuggets", 
                "金州勇士": "https://tw.global.nba.com/teams/#!/warriors", 
                "達拉斯獨行俠": "https://tw.global.nba.com/teams/#!/mavericks", 
                "明尼蘇達灰狼": "https://tw.global.nba.com/teams/#!/timberwolves", 
                "洛杉磯快艇": "https://tw.global.nba.com/teams/#!/clippers", 
                "休士頓火箭": "https://tw.global.nba.com/teams/#!/rockets", 
                "奧克拉荷馬城雷霆": "https://tw.global.nba.com/teams/#!/thunder", 
                "洛杉磯湖人": "https://tw.global.nba.com/teams/#!/lakers", 
                "曼菲斯灰熊": "https://tw.global.nba.com/teams/#!/grizzlies", 
                "波特蘭拓荒者": "https://tw.global.nba.com/teams/#!/blazers", 
                "鳳凰城太陽": "https://tw.global.nba.com/teams/#!/suns", 
                "紐奧良鵜鶘": "https://tw.global.nba.com/teams/#!/pelicans", 
                "猶他爵士": "https://tw.global.nba.com/teams/#!/jazz", 
                "沙加緬度國王": "https://tw.global.nba.com/teams/#!/kings", 
                "聖安東尼奧馬刺": "https://tw.global.nba.com/teams/#!/spurs"}
        url = team_url[city_name]
        
        # 美國版網站，取隊伍勝率
        team_us_url = {"波士頓塞爾蒂克": "https://www.nba.com/teams/celtics",
                "芝加哥公牛": "https://www.nba.com/teams/bulls",
                "亞特蘭大老鷹": "https://www.nba.com/teams/hawks",
                "布魯克林籃網": "https://www.nba.com/teams/nets",
                "克里夫蘭騎士": "https://www.nba.com/teams/cavaliers",
                "夏洛特黃蜂": "https://www.nba.com/teams/hornets",
                "紐約尼克": "https://www.nba.com/teams/knicks",
                "底特律活塞": "https://www.nba.com/teams/pistons",
                "邁阿密熱火": "https://www.nba.com/teams/heat",
                "費城76人": "https://www.nba.com/teams/sixers",
                "印第安納溜馬": "https://www.nba.com/teams/pacers",
                "奧蘭多魔術": "https://www.nba.com/teams/magic",
                "多倫多暴龍": "https://www.nba.com/teams/raptors",
                "密爾瓦基公鹿": "https://www.nba.com/teams/bucks",
                "華盛頓巫師": "https://www.nba.com/teams/wizards",
                "丹佛金塊": "https://www.nba.com/teams/nuggets",
                "金州勇士": "https://www.nba.com/teams/warriors",
                "達拉斯獨行俠": "https://www.nba.com/teams/mavericks",
                "明尼蘇達灰狼": "https://www.nba.com/teams/timberwolves",
                "洛杉磯快艇": "https://www.nba.com/teams/clippers",
                "休士頓火箭": "https://www.nba.com/teams/rockets",
                "奧克拉荷馬城雷霆": "https://www.nba.com/teams/thunder",
                "洛杉磯湖人": "https://www.nba.com/teams/lakers",
                "曼菲斯灰熊": "https://www.nba.com/teams/grizzlies",
                "波特蘭拓荒者": "https://www.nba.com/teams/blazers",
                "鳳凰城太陽": "https://www.nba.com/teams/suns",
                "紐奧良鵜鶘": "https://www.nba.com/teams/pelicans",
                "猶他爵士": "https://www.nba.com/teams/jazz",
                "沙加緬度國王": "https://www.nba.com/teams/kings",
                "聖安東尼奧馬刺": "https://www.nba.com/teams/spurs"}
        url_us = team_us_url[city_name]
        
        # 台灣網站
        driver.get(url)
        t.sleep(2)
        html = driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')

        # 美國官網
        driver.get(url_us)
        t.sleep(2)
        html_us = driver.page_source
        self.soup_us = BeautifulSoup(html_us, 'html.parser')

        # 每個隊伍包含基本資料、球員資料、賽程
        self.info = [city_name]
        self.player = [[0 for i in range(4)] for j in range(5)]
        self.game = [[0 for i in range(4)] for j in range(6)]
    @classmethod
    def clear(cls, before, after, words):  # 從原始碼中去掉不需要的，取得資訊
        start = 0
        end = 0
        num = 0
        keep = []
        for i in range(len(words)):
            if words[i:i+2] == before:
                start = i+2
            elif words[i:i+2] == after:
                end = i
            if end > start:
                keep.append(words[start:end])
                start = end
                num += 1
        return(keep)

    def get_info(self):  # 基本資料
        information = []
        # 教練
        attr = {'data-ng-bind-html': 'teamStanding.team.coach.headCoach'}
        coach = str(self.soup.find_all('span', attrs = attr))
        information.append(self.clear('\">', "</", coach))

        # 東西區聯盟
        try:
            attr = {'data-ng-href': '/standings/#!/eastern'}
        except:
            attr = {'data-ng-href': '/standings/#!/western'}
        finally:
            EW = str(self.soup.find_all('a', attrs = attr))
            information.append(self.clear("\">", "</", EW))

        # 排名
        attr = {'class': 'conference-ranking'}
        rank = str(self.soup.find_all('p', attrs = attr))
        information.append(self.clear("名#", "\'>", rank))
        
        # 轉成適當的格式放入list
        for i in range(len(information)):
            try:
                self.info.append(information[i][0])
            except:
                self.info.append("西區聯盟")
                    
        # 勝率
        attr = {'class': 'team_stat percentage'}
        wp = self.soup_us.find_all('div', attrs = attr)
        wp = self.clear("> ", " <", str(wp))
        self.info.append(wp[0])

        writer.writerow(self.info)

    def get_player(self): # 球員資料
        keep = [0] * 5
        members = []
        
        # First Name
        attr = {'data-ng-bind-html': 'player.profile.firstName'}
        first = str(self.soup.find_all('span', attrs = attr))
        members.append(self.clear("\">", "</", first))
        
        # Last Name
        attr = {'data-ng-bind-html': 'player.profile.lastName'}
        last = str(self.soup.find_all('span', attrs = attr))
        members.append(self.clear("\">", "</", last))

        # 球員位置
        attr = {'class': 'hidden-lg ng-binding'}
        posi = str(self.soup.find_all('span', attrs = attr))
        members.append(self.clear("\">", "</", posi))

        # 照片連結
        imgs = self.soup.find_all('img')
        photo = []
        for img in imgs:
            if 'src' in img.attrs:
                if 'headshots' in img['src'] and img['src'].endswith('.png'):
                    img['src'] = "https:" + str(img['src'])
                    photo.append(img['src'])
        members.append(photo)

        # 依照名、姓、位置、照片網址順序存入
        for i in range(5):
            for j in range(4):
                try:
                    self.player[i][j] = members[j][i]
                except:  # 避免網頁缺少部分資料造成錯誤
                    self.player[i][j] = "No Exist"
                    
        for i in range(5):
            writer.writerow(self.player[i][j] for j in range(4))

    def get_game(self): # 賽程資訊
        
        # 賽程日期
        attr = {'class': 'date ng-binding'}
        vsdate = str(self.soup.find_all('td', attrs = attr))
        vsdate = self.clear("\">", "</", vsdate)
        num = 0
        for i in vsdate:
            self.game[num][0] = i
            num += 1
        
        # 對手名稱
        chinesename = {"BOS": "波士頓塞爾蒂克", "CHI": "芝加哥公牛", "ATL": "雅特蘭大老鷹",
                        "BKN": "布魯克林籃網", "CLE": "克里夫蘭騎士", "CHA": "夏洛特黃蜂",
                        "NYK": "紐約尼克", "DET": "底特律活塞", "MIA": "邁阿密熱火",
                        "PHI": "費城76人", "IND": "印第安納溜馬", "ORL": "奧蘭多魔術",
                        "TOR": "多倫多暴龍", "MIL": "密爾瓦基公鹿", "WAS": "華盛頓巫師",
                        "DEN": "丹佛金塊", "MIN": "明尼蘇達灰狼", "OKC": "奧克拉荷馬城雷霆",
                        "POR": "波特蘭拓荒者", "UTA": "猶他爵士", "GSW": "金州勇士",
                        "LAC": "洛杉磯快艇", "LAL": "洛杉磯湖人", "PHX": "鳳凰城太陽",
                        "SAC": "沙加緬度國王", "DAL": "達拉斯獨行俠", "HOU": "休士頓火箭",
                        "MEM":"曼菲斯灰熊", "NOP": "紐奧良鵜鶘", "SAS": "聖安東尼奧馬刺"}

        attr = {'data-ng-controller': 'TeamScheduleSnapshotController'}  # 找出名稱簡寫
        vs = self.soup.find_all('div', attrs = attr)
        attr = {'class': 'team-img'}
        vs = vs[0].find_all('img', attrs = attr)
        shortname = []
        for i in vs:
            shortname.append(self.clear("s/", "_l", str(i)))
        while len(shortname) < 12:
            shortname.append("BOS")
        
        index = []  # 判斷是自己的名字
        for i in range(11):
            count = 1
            for j in range(i+1, 12):
                if shortname[i] == shortname[j]:
                    count += 1
                    index.append(i)
                    index.append(j)
            if count == 6:
                break
        index = set(index)


        num = 0  # 不是自己的名字就轉成中文存進去
        for i in range(12):
            if i not in index:
                self.game[num][1] = chinesename[shortname[i][0]]
                num += 1

        # 比賽時間
        attr = {'class': 'results'}
        time = self.soup.find_all('td', attrs = attr)
        point = []
        for i in time:
            attr = {'class': 'ng-binding'}
            time = i.find_all('span', attrs = attr)
            break

        try:
            self.game[0][2] = self.clear("\">", " <", str(time[2]))[0]
        except:
            self.game[0][2] = "9:00"

        # 比分
        a = self.soup.find_all('tbody')
        num = 0
        for i in a:
            attr = {'class': 'results'}
            b = i.find_all('td', attrs = attr)
            for j in b:
                if num == 0:
                    num += 1
                    continue
                else:
                    attr = {'class': 'ng-binding'}
                    point = j.find_all('span', attrs = attr)
                    list = []
                    for j in point:
                        list.append(j.get_text())
                    self.game[num][2] = list[2]
                    self.game[num][3] = list[3]
                    num += 1

        for i in range(6):
            writer.writerow(self.game[i][j] for j in range(4))
                
        # 近五場平均比分
        sum = 0
        for i in range(1,6):
            sum += int(self.game[i][2])
        avg = sum / 5
        writer.writerow([avg])



team_name = ["波士頓塞爾蒂克", "芝加哥公牛", "亞特蘭大老鷹", "布魯克林籃網", "克里夫蘭騎士",
             "夏洛特黃蜂", "紐約尼克", "底特律活塞", "邁阿密熱火", "費城76人", "印第安納溜馬",
             "奧蘭多魔術", "多倫多暴龍", "密爾瓦基公鹿", "華盛頓巫師", "丹佛金塊", "明尼蘇達灰狼",
             "奧克拉荷馬城雷霆", "波特蘭拓荒者", "猶他爵士", "金州勇士", "洛杉磯快艇",
             "洛杉磯湖人", "鳳凰城太陽", "沙加緬度國王", "達拉斯獨行俠", "休士頓火箭",
             "曼菲斯灰熊", "紐奧良鵜鶘", "聖安東尼奧馬刺"]

chrome_options = Options()
chrome_options.add_argument('--headless')  # 瀏覽器不提供視覺化頁面
chrome_options.add_argument('--disable-gpu')  # 規避bug
driver = webdriver.Chrome(executable_path = '/Users/amy1226/Downloads/chromedriver', options=chrome_options)

filepath = '/Users/amy1226/Downloads/team.csv'
wf = open(file=filepath, mode="w", newline = '', encoding="utf-8")
writer = csv.writer(wf)

for i in range(30):
    team = Team(driver, team_name[i])
    team.get_info()  # 隊伍名稱、教練名字、分區聯盟、分區排名、勝率
    team.get_player()  # 名、姓氏、位置、頭像連結
    team.get_game()  # 比賽日期、對手logo連結、自己的分數、對手的分數（第一筆資料是下一場要比的，比分的位置是比賽時間）、近五場平均得分

driver.close()
wf.close
