from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

class bet():
    '''
    抓明日的比賽資訊(for 下注)
    用的driver是google chrome

    def get_data() 不用input
    return: 一場比賽一個list[時間, 客隊, 主隊, 場地]
            list數量不定, 視當天比賽場數, 全數包裝在一個二維list裡面回傳
    '''

    def __init__(self):   
        driver = webdriver.Chrome(executable_path = '/Users/joneschou/Downloads/chromedriver')
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
                p = str(i)
                start = p.find('<span bo-hide')
                if start == -1:
                    continue
                end = p.find('</span>', start)
                time = p[start + 62: end - 1]
                team = i.find_all('a', limit = 2)
                team_list = list()
                for j in team:
                    team_list.append(j.get_text())
                away = team_list[0]
                home = team_list[1]
                attrr = {'bo-text' : 'game.profile.arenaName'}
                arena = i.find('td', attrs = attrr).string
                data_list.append([time, away, home, arena])
        except:
            pass

        return data_list

# 以下為試class的功能
bet = bet()
final = bet.get_data()
print(final)
