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
import pandas as pd

#這個需要在class team與class bet之下
class gamebet():
    """
    def odds 需要輸入雙方隊伍名字
    return 賠率清單，單元數固定
    [['單雙', '單', 1.75, '雙', 1.75],
     ['大小(總分)', '大/X分', 1.75, '小/X分', 1.75],
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
        
        team_file = "C://Users//kevin//OneDrive//Documents//GitHub//PBC2019//team.csv" #要改
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
                        print(row)
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
    
    #判斷下幾注，賠率
    """
    判斷是否賭贏的程式
    """
        
    
    #下注
    """
    如果是空的話就不能下注
    def gobet 需要輸入betlist，betlist長相:
    [['時間', 'A隊', 'B隊', '地點', '大小(總分)', '大', 1.75 ,2],
     ['時間', 'A隊', 'B隊', '地點', '單雙(總分)', '小於X分', 1.75, 2],
     ['時間', 'A隊', 'B隊', '地點', '賭法', '方向', 賠率, 4]]
    
    - 從帳戶扣除應繳金額
    - 新增一筆交易資料，此交易資料會是一個清單：
      ['時間', 'A隊', 'B隊', '地點', '賭法', '方向', 賠率, 下幾注,'輸/贏/未交割', 盈虧, 下注時間]
    - 回傳
    """
    def confirm_bet(self, user_info, bet_list):
        #user_info = ['kevin', '123', 200, 'login', [ [], [], [] ]  ]
        
        #計算總價金，做成交易紀錄
        bet_sum = 0
        for i in range(len(bet_list)):
            bet_sum += bet_list[i][7] * 10
            bet_list[i].append('未結算')
            bet_list[i].append(- (bet_list[i][7] * 10))
            bet_list[i].append(t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
        
        #需要Check Balance的函數
        if user_info[2] < bet_sum:
            #tk.MessageBox.showWarning(text="帳戶餘額不足，無法投注")
            print("帳戶餘額不足，無法投注。")
        
        else:   
            #從帳戶扣取應繳金額
            user_info[2] -= bet_sum
            
            #新增一筆交易資料
            for i in range(len(bet_list)):
                user_info[4].append(bet_list[i])
            
        return user_info
                    
def save_csv():
    # 讀檔
    df=pd.read_csv("userInformation.csv")

def save_csv():
    # 讀檔
    df=pd.read_csv("userInformation.csv")

    # 刪除使用者原本在csv檔中的那列
    # username為login後pass進來的使用者名稱
    df=df[df.Username != Username]

    # 把修改後的user_info增加至csv檔中的最後一項
    # usr_list=['123', '123', 10000, '17:53'] 我隨便打的
    df.loc[len(df)] = user_info

    # 存檔
    df.to_csv('userInformation.csv', index = False)
