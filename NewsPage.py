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

 
# 主頁面（視窗）


# 抓news（尚未更新至最新的code版本，明日更）
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

# 以下會放抓wounded的class
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



#  SportsLottery相當於開一個主視窗
class SportsLottery(tk.Tk):
   
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

        self.frames = {}
        for page in (NewsPage, StartPage): # StartPage：測試用，之後會換掉
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame # 存進dictionary
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")
        self.show_frame("StartPage")
        
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name（跳轉頁面）'''
        frame = self.frames[page_name]
        frame.tkraise()
        
# NewsPage新聞頁（之後應該會把傷兵資訊寫在同一頁右側）    
class NewsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller=controller
        self.configure(bg="lemon chiffon",width=250, height=700)
        self.pack(side=BOTTOM, expand=TRUE)
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
                btn.configure(command=lambda: controller.show_frame("StartPage"))
        
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


# StartPage僅試驗跳轉功能用，之後會移除  
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700)
        self.controller = controller
        self.configure(width=500, height=700)
        self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
        self.F1.pack(side=TOP, fill=BOTH)
        label = tk.Label(self, text="This is a page waiting for team logos.", font="Didot")
        label.pack(side=TOP, fill="x", pady=10)
        functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
        for function in reversed(functions):
            btn=tk.Button(self.F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
            btn.pack(side=RIGHT, pady=30, anchor=N)
            btn_txt=btn.cget("text")
            if btn_txt == "新聞介紹":
                btn.configure(command=lambda: controller.show_frame("NewsPage"))
        
app=SportsLottery()
app.mainloop()        

