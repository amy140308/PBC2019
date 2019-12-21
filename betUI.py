class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=700, bg = "lemon chiffon")
        """
        以下是宗勳做成def create_common_frames的部分，但用mac有些問題，暫且先不寫成def看看
        """
        self.F1=tk.Frame(self,bg="misty rose",width=500, height=300)
        self.F1.pack(side="top", fill="both",anchor="n")
        self.F2=tk.Frame(self,bg="lemon chiffon",width=500, height=700)
        self.F2.pack(side="top", fill="both", expand=True)
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
            elif btn_txt == "賽事下注":
                btn.configure(command=lambda: self.controller.show_frame("GamePage"))
            elif btn_txt == "歷史資料":
                btn.configure(command=lambda: self.controller.show_frame("HistoryPage"))
        # 頁面功能 (之後可能要融合到Main_onWindows.py)
        # 現在的點就是登入之前會先跳chrome的東西...真的是滿尷尬
        f1=tkFont.Font(size=20, family="標楷體")
        if len(final_g)>0:
            for i in range(len(final_g)):
                self.btn=tk.Button(self.F2, height=5, width=50, relief =tk.RAISED, bg="ivory3")
                time=final_g[i][0]  # 
                team1=final_g[i][1]  
                team2=final_g[i][2]
                arena=final_g[i][3]
                self.btn.configure(text=time+"\n"+team1+"vs."+team2+"\n"+arena, font="標楷體")
                self.btn.cget("text")
                self.btn.configure(command=lambda click.button 
                self.btn.pack(anchor="n", side="top", pady=10, padx=5)     
        else:

            self.Label=tk.Label(text="今日無賽事", font=f1)
            self.Label.pack(anchor="n", side="top", pady=20)
        
        def click_game_button(teamA, teamB):
            window=tk.Toplevel()
            window.geometry("500x500")
            window.configure(bg="azure")
            self.teamCanv = tk.Canvas(window, width=500, height = 500, highlightthickness=0, bg="azure")
            self.teamCanv.pack(side = "top", fill = "both", expand=True)
            self.F = tk.Frame(self.teamCanv, bg = "wheat2", width=500, height = 500)
            self.F.pack(side = "bottom", fill = "both", anchor="center")
            

            