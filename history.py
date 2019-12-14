from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time as t
import datetime

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
        self.driver = webdriver.Chrome(executable_path = '/Users/joneschou/Downloads/chromedriver')
        self.driver.get('https://tw.global.nba.com/schedule/#!/7')

    def update(self):
        stop = False
        while not stop:
            self.driver.find_element_by_xpath('//*[@class="icon-caret-left days"]').click()
            t.sleep(3)
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
                else:
                    year = today.year + 1
                d = datetime.datetime(year, month, day)
                filepath = '/Users/joneschou/Downloads/data.csv'
                wf = open(file=filepath, mode="a+", encoding="utf-8")
                writer = csv.writer(wf)
                rf = open(file=filepath, mode="r", encoding="utf-8")
                reader = csv.reader(rf)
                exist = False
                for row in reader:
                    if row[0] == d.strftime('%Y-%m-%d'):
                        exist = True
                        break
                if d < datetime.datetime(2019, 12, 1):
                    stop = True           
                elif not exist:
                    data = tag.find_all('tr')
                    data_list = list()
                    for i in data:
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
                        attrrr = {'bo-text' : ' game.boxscore.awayScore'}
                        away_score = int(i.find('span', attrs = attrrr).string)
                        attrrrr = {'bo-text' : ' game.boxscore.homeScore'}
                        home_score = int(i.find('span', attrs = attrrrr).string)
                        writer.writerow([d.strftime('%Y-%m-%d'), time, away, home, away_score, home_score, arena])
                else:
                    stop = True
        wf.close()
        rf.close()
        self.driver.close()

    def get_data(self, date):
        filepath = '/Users/joneschou/Downloads/data.csv'
        f = open(file=filepath, mode="r", encoding="utf-8")
        rows = csv.reader(f)
        data = list()
        for row in rows:
            if row[0] == date:
                data.append(row)
        return data

# 以下為試class的功能
history = history()
history.update()
final = history.get_data('2019-12-06')
print(final)
