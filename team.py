from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Team:
    def __init__(self, city_name):  # 用字典連動網址，用Chrome打開網站取得原始碼
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
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 瀏覽器不提供視覺化頁面
        chrome_options.add_argument('--disable-gpu')  # 規避bug
        driver = webdriver.Chrome(executable_path = '/Users/amy1226/Downloads/chromedriver', options=chrome_options)driver.get(url)
        html = driver.page_source
        driver.close()
        self.soup = BeautifulSoup(html, 'html.parser')

        # 每個隊伍包含基本資料、球員資料、賽程
        self.info = [city_name]
        self.player = [[0 for i in range(4)] for j in range(5)]
        self.game = [[0 for i in range(4)] for j in range(6)]

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

        #排名
        attr = {'class': 'conference-ranking'}
        rank = str(self.soup.find_all('p', attrs = attr))
        information.append(self.clear("名#", "\'>", rank))
        for i in range(len(information)):
            try:
                self.info.append(information[i][0])
            except:
                self.info.append("西區聯盟")


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
                self.player[i][j] = members[j][i]

    def get_game(self): # 賽程資訊
        
        # 賽程日期
        attr = {'class': 'date ng-binding'}
        vsdate = str(self.soup.find_all('td', attrs = attr))
        vsdate = self.clear("\">", "</", vsdate)
        num = 0
        for i in vsdate:
            self.game[num][0] = i
            num += 1
        
        # 下一場對手logo
        attr = {'class': 'results'}
        vs = self.soup.find_all('td', attrs = attr)
        attr = {'class': 'team-img'}
        vslogo = vs[0].find('img', attrs = attr)
        self.game[0][1] = "https://tw.global.nba.com" + str(vslogo.get('src'))

        # 過去對手logo
        attr = {'data-ng-repeat': 'game in previousGames | orderBy : \'-profile.utcMillis\''}
        vs = self.soup.find_all('tr', attrs = attr)
        photo = []
        image = []
        for i in vs:
            imgs = i.find_all('img')
            for img in imgs:
                photo.append("https://tw.global.nba.com" + str(img.get('src')))

        index = []
        count = 0
        for i in range(len(photo)-1):
            count = 0
            for j in range(i+1,len(photo)):
                if photo[i] == photo[j]:
                    index.append(i)
                    index.append(j)
                    count += 1
            if count == 4:
                break
        
        num = 1
        for i in range(10):
            if i in index:
                continue
            else:
                self.game[num][1] = photo[i]
                num += 1

        # 比賽時間
        attr = {'class': 'results'}
        time = self.soup.find_all('td', attrs = attr)
        point = []
        for i in time:
            attr = {'class': 'ng-binding'}
            time = i.find_all('span', attrs = attr)
            break

        self.game[0][2] = self.clear("\">", " <", str(time[2]))[0]

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
                    # 這邊不知為何不會動
                    self.game[num][2] = self.clear("\">", "<\/", str(point[2]))
                    self.game[num][3] = self.clear("\">", "<\/", str(point[3]))
                    num += 1


team = Team(input())

team.get_info()
print(team.info)

team.get_player()
print(team.player)

team.get_game()
print(team.game)
