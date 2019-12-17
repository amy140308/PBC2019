"""
測試inner class
"""
import tkinter as tk
from tkinter import *
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

class LoginPage(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self) 
        self.configure(width=250, height=700)
        self.pack(side=BOTTOM, expand=TRUE)
        self.canvas=tk.Canvas(self, height=1000, width=500, bg="plum2") 
        # self.img=Image.open("NBALogo.gif")
        # self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        # self.img=ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.pack(fill=BOTH,expand=Y)
        self.canvas.configure(bg="misty rose")

        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self.canvas, text="使用者名稱：", font=f1)
        self.l2=tk.Label(self.canvas, text="密碼：", font=f1)
        self.l1.pack(side=TOP, fill=X, padx=10, pady=10)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self.canvas, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side=TOP,padx=20, pady=10) #fill=X

        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self.canvas, textvariable=self.var_usr_pwd, show="*") 
        self.entry_usr_pwd.pack(side=TOP, padx=10, pady=10)
        # 以下login command之後要寫成判斷式並用configure結合
        self.btn_login=tk.Button(self.canvas, text="Log in", font=f1, command=self.login)
        self.btn_login.pack(side=RIGHT, padx=10, pady=10)
        self.btn_signup=tk.Button(self.canvas, text="Sign up", font=f1, command=self.usr_signup)
        self.btn_signup.pack(side=RIGHT, padx=10, pady=10)
    def login(self):
        app=self.SportsLottery()
        app.mainloop()
        self.destroy()

    def usr_signup(self):
        pass

    
    class SportsLottery(tk.Frame):
        # SportsLottery和以下所有分頁全部塞在LoginPage下面，所謂inner classes
   
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.geometry("1000x1000")
            self.title("運彩模擬器")
            
            # self.canvas=tk.Canvas(self, width=500, height=1000)
            # self.canvas.pack(fill=BOTH,expand=Y)
            # canvas.configure(bg="misty rose")
            
            # container中，堆疊frames，跳轉頁面用
            container = tk.Frame(self, width=500, height=700)
            container.pack(side=TOP, fill=BOTH, expand=TRUE)
            container.grid_rowconfigure(1, weight=1)
            container.grid_columnconfigure(0, weight=1)

            LoginPage(parent=container, controller=self).grid(row=1, column=0, sticky="nsew")

            for page in (NewsPage, TeamPage, PersonalPage, GamePage, HistoryPage): 
                page_name = page.__name__
                frame = page(parent=container, controller=self)
                self.frames[page_name] = frame # 存進dictionary
                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=1, column=0, sticky="nsew")
            self.show_frame("NewsPage")
            # 預設開啟頁面為新聞頁
            
            
        def show_frame(self, page_name):
            '''Show a frame for the given page name（跳轉頁面）'''
            frame = self.frames[page_name]
            frame.tkraise()

    
    # NewsPage新聞頁
    class NewsPage(tk.Frame):
        
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent) 
            self.controller=controller
            self.configure(bg="lemon chiffon",width=250, height=700)
            # self.pack(side=BOTTOM, expand=TRUE)
            # welcome page
            self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
            self.F1.pack(side=TOP, fill=BOTH,anchor=N)
            self.F2=tk.Frame(self,bg="sienna4",width=500, height=700)
            self.F2.pack(side=TOP, fill=BOTH, expand=TRUE)
            self.FN=tk.Frame(self.F2,bg="lemon chiffon",width=250, height=700)
            self.FN.pack(side=LEFT, anchor=W,fill=BOTH, expand=TRUE)
            self.FW=tk.Frame(self.F2, bg="floral white", width=300, height=700)
            self.FW.pack(side=LEFT,fill=BOTH, expand=TRUE)
            functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
            for function in reversed(functions):
                btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
                btn.pack(side=RIGHT, pady=30, anchor=N)
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
            self.TitleLbl.pack(side=TOP)
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
                self.picLabel.pack(side=TOP, pady=10, padx=10, anchor=W) 
                
                f1=tkFont.Font(size=20, family="標楷體")
                f2=tkFont.Font(size=10, family="微軟正黑體")
                self.btn=tk.Label(self.FN, text=title, font=f1,bg="lemon chiffon",cursor="hand2")
                self.btnsmall=tk.Label(self.FN, text=time+"\n"+intro,font=f2, bg="lemon chiffon", justify=LEFT) # 傷兵/justify=RIGHT
                def callback(event):
                    webbrowser.open_new(one_news[-2])
                self.btn.bind("<Button-1>", callback)
                self.btnsmall.bind("<Button-1>", callback)
                self.picLabel.bind("<Button-1>", callback)
                self.btn.pack(side=TOP, pady=2,padx=10, anchor=W) # 傷兵：anchor=E
                self.btnsmall.pack(side=TOP,pady=2,padx=10, anchor=W) # 傷兵：anchor=E
            f0=tkFont.Font(family="標楷體", size=20)
            self.TitleLbl=tk.Label(self.FW, text="傷兵資訊", font=f0, bg="floral white")
            self.TitleLbl.pack(side=TOP)
            
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
                self.picLabel.pack(side=TOP, pady=10, padx=10, anchor=W) 
                
                f1=tkFont.Font(size=20, family="標楷體")
                f2=tkFont.Font(size=10, family="微軟正黑體")
                self.btn=tk.Label(self.FW, text=title, font=f1,bg="floral white",cursor="hand2")
                self.btnsmall=tk.Label(self.FW, text=time+"\n"+intro,font=f2, bg="floral white", justify=LEFT) # 傷兵/justify=RIGHT
                def callback(event):
                    webbrowser.open_new(one_wounded[-2])
                self.btn.bind("<Button-1>", callback)
                self.btnsmall.bind("<Button-1>", callback)
                self.picLabel.bind("<Button-1>", callback)
                self.btn.pack(side=TOP, pady=2,padx=10, anchor=W) # 傷兵：anchor=E
                self.btnsmall.pack(side=TOP,pady=2,padx=10, anchor=W) # 傷兵：anchor=E



    class TeamPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.configure(width=500, height=700, bg = "lemon chiffon")
            self.createWidgets()

        def createWidgets(self):
            self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
            self.F1.pack(side=TOP, fill=BOTH)
            
            functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
            for function in reversed(functions):
                self.btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
                self.btn.pack(side=RIGHT, pady=30, anchor=N)
                btn_txt=self.btn.cget("text")
                if btn_txt == "球隊介紹":
                    self.btn.configure(command=lambda: self.controller.show_frame("TeamPage"))
                elif btn_txt == "新聞介紹":
                    self.btn.configure(command=lambda: self.controller.show_frame("NewsPage"))
                elif btn_txt == "個人帳戶":
                    self.btn.configure(command = lambda: self.controller.show_frame("PersonalPage"))
                elif btn_txt == "賽事下注":
                    self.btn.configure(command=lambda: self.controller.show_frame("GamePage"))
                elif btn_txt == "歷史資料":
                    self.btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
        


            self.F2_canvas = tk.Canvas(self, width = 500, height = 600, bg = "lemon chiffon")  #height調整canvas的長度，要手動調（或寫def）
            self.F2_canvas.pack(side = BOTTOM,fill = BOTH, expand = TRUE)
            # 要建立frame，透過create_widget放在canvas上面才能滾動
            self.frame = tk.Frame(self.F2_canvas, bg = "lemon chiffon", width = 500, height = 1200)
            self.frame.pack(side = BOTTOM, fill = BOTH ,expand=TRUE)
            self.F2_canvas.create_window((200,200), window = self.frame, anchor = NW) 
            # 滾動條
            gameBar = tk.Scrollbar(self.F2_canvas, orient = "vertical", command = self.F2_canvas.yview)
            gameBar.pack(side = "right", fill = "y")
            self.F2_canvas.configure(scrollregion = self.F2_canvas.bbox('all'), yscrollcommand = gameBar.set)

            # 放賽事
            f0=tkFont.Font(family="標楷體", size=20)
            self.TitleLbl=tk.Label(self.frame, text="球隊介紹", font=f0 ,bg="lemon chiffon").pack(side = TOP)
            
            Logo_road_list = ["/Users/yangqingwen/Desktop/team_logo/ATL_logo.png","/Users/yangqingwen/Desktop/team_logo/BKN_logo.png","/Users/yangqingwen/Desktop/team_logo/BOS_logo.png","/Users/yangqingwen/Desktop/team_logo/CHA_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/CHI_logo.png","/Users/yangqingwen/Desktop/team_logo/CLE_logo.png","/Users/yangqingwen/Desktop/team_logo/DAL_logo.png","/Users/yangqingwen/Desktop/team_logo/DEN_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/DET_logo.png","/Users/yangqingwen/Desktop/team_logo/GSW_logo.png","/Users/yangqingwen/Desktop/team_logo/HOU_logo.png","/Users/yangqingwen/Desktop/team_logo/IND_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/LAC_logo.png","/Users/yangqingwen/Desktop/team_logo/LAL_logo.png","/Users/yangqingwen/Desktop/team_logo/MEM_logo.png","/Users/yangqingwen/Desktop/team_logo/MIA_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/MIL_logo.png","/Users/yangqingwen/Desktop/team_logo/MIN_logo.png","/Users/yangqingwen/Desktop/team_logo/NOP_logo.png","/Users/yangqingwen/Desktop/team_logo/NYK_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/OKC_logo.png","/Users/yangqingwen/Desktop/team_logo/ORL_logo.png","/Users/yangqingwen/Desktop/team_logo/PHI_logo.png","/Users/yangqingwen/Desktop/team_logo/PHX_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/POR_logo.png","/Users/yangqingwen/Desktop/team_logo/SAC_logo.png","/Users/yangqingwen/Desktop/team_logo/SAS_logo.png","/Users/yangqingwen/Desktop/team_logo/TOR_logo.png",
                        "/Users/yangqingwen/Desktop/team_logo/UTA_logo.png","/Users/yangqingwen/Desktop/team_logo/WAS_logo.png"]
            
            """ for windows
            Logo_road_list = ["C:\\logo\\ATL_logo.png","C:\\logo\\BKN_logo.png","C:\\logo\\BOS_logo.png","C:\\logo\\CHA_logo.png",
                            "C:\\logo\\CHI_logo.png","C:\\logo\\CLE_logo.png","C:\\logo\\DAL_logo.png","C:\\logo\\DEN_logo.png",
                            "C:\\logo\\DET_logo.png","C:\\logo\\GSW_logo.png","C:\\logo\\HOU_logo.png","C:\\logo\\IND_logo.png",
                            "C:\\logo\\LAC_logo.png","C:\\logo\\LAL_logo.png","C:\\logo\\MEM_logo.png","C:\\logo\\MIA_logo.png",
                            "C:\\logo\\MIL_logo.png","C:\\logo\\MIN_logo.png","C:\\logo\\NOP_logo.png","C:\\logo\\NYK_logo.png",
                            "C:\\logo\\OKC_logo.png","C:\\logo\\ORL_logo.png","C:\\logo\\PHI_logo.png","C:\\logo\\PHX_logo.png",
                            "C:\\logo\\POR_logo.png","C:\\logo\\SAC_logo.png","C:\\logo\\SAS_logo.png","C:\\logo\\TOR_logo.png",
                            "C:\\logo\\UTA_logo.png","C:\\logo\\WAS_logo.png"]
            """
            
            Frame_List = []
            # 打開隊伍資訊
            self.Team_name_List = ["亞特蘭大老鷹", "布魯克林籃網", "波士頓塞爾蒂克", "夏洛特黄蜂", "芝加哥公牛",
                            "克里夫蘭騎士", "達拉斯獨行俠", "丹佛金塊","底特律活塞", "金州勇士", 
                            "休士頓火箭","印第安納溜馬", "洛杉磯快艇", "洛杉磯湖人", "曼菲斯灰熊", 
                            "邁阿密熱火", "密爾瓦基公鹿", "明尼蘇達灰狼", "紐奧良鵜鶘", "紐約尼克",
                            "奧克拉荷馬城 雷霆", "奧蘭多魔術", "費城76人","鳳凰城太陽", "波特蘭拓荒者", 
                            "沙加緬度國王","聖安東尼奧馬刺", "多倫多暴龍", "猶他爵士", "華盛頓巫師"] 
            self.Logo_image_list=[]
            for i in range(30):
                
                # 用image抓取png檔並resize
                self.logo_image = Image.open(Logo_road_list[i])
                self.logo_image = self.logo_image.resize((100, 100), Image.ANTIALIAS)
                # 用「ImageTk.PhotoImage」轉換成tk可以讀的樣子
                self.logo_image = ImageTk.PhotoImage(image = self.logo_image)
                self.Logo_image_list.append(self.logo_image)
            
            
                # 每五個建立新的Frame
                if i % 5 == 0:
                    self.team_frame = tk.Frame(self.frame, bg = "wheat2",width = 1000, height = 120)
                    Frame_List.append(self.team_frame)
                    self.team_frame.pack(side = TOP, pady = 10, padx = 20, anchor = N, fill = "x")  
                
                # 
                self.button_logo = tk.Button(self.team_frame, text=self.Team_name_List[i] , image = self.Logo_image_list[i], compound=BOTTOM, command = self.click_team_button)
                self.button_logo.pack(side = LEFT, pady = 10, padx = 20, anchor = NW, expand = True)
        
        # 點按鈕為各隊伍資訊
        def click_team_button(self):
            window = Toplevel(self)
            window.title("")
            window.geometry("300x500")
            F10 = tk.Frame(window, bg = "wheat2", width = 500, height = 300)
            F10.pack(side = TOP, fill = BOTH) 


    class GamePage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.configure(width=500, height=700, bg = "lemon chiffon")
            """
            以下是宗勳做成def create_common_frames的部分，但用mac有些問題，暫且先不寫成def看看
            """
            self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
            self.F1.pack(side=TOP, fill=BOTH,anchor=N)
            self.F2=tk.Frame(self,bg="lemon chiffon",width=500, height=700)
            self.F2.pack(side=TOP, fill=BOTH, expand=TRUE)
            functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
            for function in reversed(functions):
                btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
                btn.pack(side=RIGHT, pady=30, anchor=N)
                btn_txt=btn.cget("text")
                if btn_txt == "球隊介紹":
                    btn.configure(command=lambda: controller.show_frame("TeamPage"))
                elif btn_txt == "新聞介紹":
                    btn.configure(command=lambda: controller.show_frame("NewsPage"))
                elif btn_txt == "個人帳戶":
                    btn.configure(command = lambda: controller.show_frame("PersonalPage"))
                elif btn_txt == "賽事下注":
                    btn.configure(command=lambda: self.controller.show_frame("GamePage"))
                elif btn_txt == "歷史資料":
                    btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
            # 頁面功能 (之後可能要融合到Main_onWindows.py)
            # 現在的點就是登入之前會先跳chrome的東西...真的是滿尷尬
            for i in range(len(final_g)):
                self.btn=tk.Button(self.F2, height=5, width=50, relief =tk.RAISED, bg="ivory3")
                time=final_g[i][0]
                team1=final_g[i][1]
                team2=final_g[i][2]
                arena=final_g[i][3]
                self.btn.configure(text=time+"\n"+team1+"vs."+team2+"\n"+arena,font="標楷體")
                self.btn.pack(anchor=N, side=TOP, pady=10, padx=5)     

            
    # HistoryPage歷史紀錄頁面
    class HistoryPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.configure(width=500, height=700, bg = "lemon chiffon")
            self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
            self.F1.pack(side=TOP, fill=BOTH,anchor=N)
            self.F2=tk.Frame(self,bg="lemon chiffon",width=500, height=700)
            self.F2.pack(side=TOP, fill=BOTH, expand=TRUE)
            functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
            for function in reversed(functions):
                btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
                btn.pack(side=RIGHT, pady=30, anchor=N)
                btn_txt=btn.cget("text")
                if btn_txt == "球隊介紹":
                    btn.configure(command=lambda: controller.show_frame("TeamPage"))
                elif btn_txt == "新聞介紹":
                    btn.configure(command=lambda: controller.show_frame("NewsPage"))
                elif btn_txt == "個人帳戶":
                    btn.configure(command = lambda: controller.show_frame("PersonalPage"))
                elif btn_txt == "賽事下注":
                    btn.configure(command=lambda: self.controller.show_frame("GamePage"))
                elif btn_txt == "歷史資料":
                    btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
        
        
        # def click_game_button(self):



            

    class PersonalPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.configure(width=500, height=700, bg="lemon chiffon")
            self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
            self.F1.pack(side=TOP, fill=BOTH)
            
            functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
            for function in reversed(functions):
                btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
                btn.pack(side=RIGHT, pady=30, anchor=N)
                btn_txt=btn.cget("text")
                if btn_txt == "球隊介紹":
                    btn.configure(command=lambda: controller.show_frame("TeamPage"))
                elif btn_txt == "新聞介紹":
                    btn.configure(command=lambda: controller.show_frame("NewsPage"))
                elif btn_txt == "個人帳戶":
                    btn.configure(command = lambda: controller.show_frame("PersonalPage"))
                elif btn_txt == "賽事下注":
                    btn.configure(command=lambda: self.controller.show_frame("GamePage"))
                elif btn_txt == "歷史資料":
                    btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
        


            # 帳戶組要給的餘額數字：
            Balance=5
            f1=tkFont.Font(family="Didot", size=30)

            self.BalanceLbl=tk.Label(self,text="帳戶餘額："+str(Balance), font=f1,bg="lemon chiffon")
            self.BalanceLbl.pack(side=TOP, anchor=CENTER,pady=20)





L=LoginPage()
L.mainloop()