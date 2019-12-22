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
"""
寫球隊分頁用的測試主頁（for 跑不出toplevel的可憐mac）
"""



class Temp(tk.Tk):
    
    def __init__(self, team_name):
        tk.Tk.__init__(self)
        self.geometry("500x500")
        self.title("運彩模擬器")
        self.configure(bg="wheat2")
        self.team_name=team_name
       
        # window = tk.Tk(self)
        # window.geometry("500x500")
        # 以下是有container的scrollbar寫法
        self.container = tk.Frame(self, height=500, width=1000)
        self.container.pack(side="top",fill="both", expand=True)
        self.teamCanv = tk.Canvas(self.container, width=500, height = 1000, highlightthickness=0, scrollregion=(0,0,500,500), bg="wheat2")
        self.teamCanv.pack(side = "top", fill = "both", expand=True)
        teamBar = tk.Scrollbar(self.teamCanv, orient = "vertical", command = self.teamCanv.yview)
        teamBar.pack(side = "right", fill = "y")
       
        self.scrollableF=tk.Frame(self.teamCanv, bg = "wheat2", width=1000, height = 500)
        self.scrollableF.pack(side = "bottom", fill = "both", anchor="center")
        self.teamCanv.configure(yscrollcommand = teamBar.set)
        self.scrollableF.bind("<Configure>",lambda e: self.teamCanv.configure(scrollregion=self.teamCanv.bbox("all")))
        self.teamCanv.create_window((0, 0), window=self.scrollableF, anchor="n")
        
        
        # 隊伍資訊
        """
        
        """
        filepath = "/Users/yangqingwen/Desktop/PBC2019/team.csv"
        wf = open(file=filepath, mode="r", encoding="utf-8")
        rows = csv.reader(wf)  
        info = []
        players = []
        games = []

        count = 0
        for i in rows:
            if i[0] == team_name:
                count = 1
                info = i
            
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
        self.Label.configure(text="隊伍名稱："+info[0]+
                                    "\n"+"教練："+info[1]+
                                    "\n"+"分區聯盟："+info[2]+
                                    "\n"+"分區排名："+info[3]+
                                    "\n"+"勝率："+info[4]+"\n"+"\n")
    
        # 名、姓氏、位置、頭像連結 (五個先發各在一個list，包成2-d list回傳)
        self.PlayerLabel=tk.Label(self.scrollableF, text="先發名單", font=("標楷體", 15), bg="peach puff")
        self.PlayerLabel.pack(side= "top", pady=10)
        # 修改使用team.csv後造成的bug
        playerPhotos=[]
        for player in players:
            image_url=player[3]

            ssl._create_default_https_context = ssl._create_unverified_context
            
            try:
                u = urlopen(image_url)
                raw_data = u.read()
                u.close()
                self.playerPhoto = Image.open(BytesIO(raw_data))
                self.playerPhoto = self.playerPhoto.resize((130, 95), Image.ANTIALIAS) 
                self.playerPhoto = ImageTk.PhotoImage(self.playerPhoto)
                self.photoLabel = tk.Label(self.scrollableF, image=self.playerPhoto)
                self.photoLabel.pack(side="top", pady=2, anchor="e")   
            except:
                self.photoLabel = tk.Label(self.scrollableF, text="No image")
                self.photoLabel.pack(side="top", pady=2, anchor="e") 
                            
            self.PInfoLabel= tk.Label(self.scrollableF, bg="wheat2")
            self.PInfoLabel.pack(side= "top", pady=5)
            self.PInfoLabel.configure(text="球員姓名："+player[0]+" "+player[1]+"\n"+ "隊中位置："+player[2])
            
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

Temp=Temp("夏洛特黃蜂")
Temp.mainloop()
