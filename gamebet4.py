 #下注
    """
    如果是空的話就不能下注
    def gobet 需要輸入betlist，betlist長相:
    [['時間', 'A隊', 'B隊', '地點', '大小(總分)', '大', 1.75 ,2],
     ['時間', 'A隊', 'B隊', '地點', '單雙(總分)', '小於X分', 1.75, 2],
     ['時間', 'A隊', 'B隊', '地點', '不讓分', '隊名', 賠率, 2]]
    
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
            
            #寫回csv裡面
            # 
            file_address ="/Users/yangqingwen/Downloads/userInformation.csv"
            #  "C://Users//kevin//OneDrive//Desktop//userInformation.csv"
            temp_users = []
            temp_user_info = []
            
            #將資料append存進一個暫時清單
            with open(file_address, "r", newline = '', encoding = 'UTF-8') as f:
                rows = csv.reader(f)
                for row in rows:
                    if row != []:
                        temp_users.append(row)
            
            #將User info存進暫時清單
            for i in range(len(user_info)):
                temp_user_info = copy.deepcopy(user_info)
            
            c = 0
            for i in range(len(temp_users)):
                if temp_users[i][0] == temp_user_info[0]:
                    temp_users[i] = temp_user_info
                    c = 1
                    
            if c == 0:
                temp_users.append(temp_user_info)
                    
            with open(file_address, "w", newline = '', encoding = 'UTF-8') as f:
                writer = csv.writer(f)
                for i in range(len(temp_users)):
                    writer.writerow(temp_users[i])


    def click_game_button(self, teamA, teamB):
        # 可能跟隊伍team.py之後會修出來的東西要調整
        game_bet=gamebet()
        Odds=game_bet.odds(teamA, teamB)

        count=0
        Sure=[0,0,0,0,0,0]

        window=tk.Toplevel(self)
        window.geometry("500x500")
        window.configure(bg="azure")
        
        self.GameCanv = tk.Canvas(window, width=500, height = 500, highlightthickness=0, bg="azure")
        self.GameCanv.pack(side = "top", fill = "both", expand=True)
        self.GameFrame = tk.Frame(self.GameCanv, bg = "wheat2", width=500, height = 500)
        self.GameFrame.pack(side = "top", fill = "both", anchor="center", expand=True)
        self.showL = tk.Label(self.GameFrame, bg="white", width=10, height = 10)
        self.showL.grid(row=0, column=0, columnspan=8, rowspan=4, padx=5, pady=5, sticky = "nsew")
        
        
        
        # 單雙
        self.GL1=tk.Label(self.GameFrame, bg="linen", text="單雙（總分）")
        self.GL1.grid(row=4, column=0, pady=10, columnspan=2, sticky = "nsew")
        self.GB1 = tk.Button(self.GameFrame, bg="lavender blush", text="單   1.75", command=self.clcikBtnGB1)
        self.GB1.grid(row=5, column=0, pady=10, columnspan=2, sticky = "nsew")
        self.GB2 = tk.Button(self.GameFrame, bg="lavender blush", text="雙   1.75", command=self.clcikBtnGB2)
        self.GB2.grid(row=5, column=3, pady=10, columnspan=2, sticky = "nsew")
        # 大小
        self.GL2=tk.Label(self.GameFrame, bg="linen", text="大小（總分）")
        self.GL2.grid(row=6, column=0, columnspan=2, pady=10, sticky = "nsew")
        self.GB3 = tk.Button(self.GameFrame, bg="lavender blush", text=Odds[1][1]+"  1.75", command=self.clcikBtnGB3)
        self.GB3.grid(row=7, column=0, columnspan=2, pady=10, sticky = "nsew")
        self.GB4 = tk.Button(self.GameFrame, bg="lavender blush", text=Odds[1][3]+"  1.75", command=self.clcikBtnGB4)
        self.GB4.grid(row=7, column=3, columnspan=2, pady=10, sticky = "nsew")
        # 不讓分
        self.GL3= tk.Label(self.GameFrame, bg="linen", text="不讓分")
        self.GL3.grid(row=8, column=0, columnspan=2, pady=10, sticky = "nsew")
        self.GB5=tk.Button(self.GameFrame, bg="lavender blush", text=str(Odds[2][1])+"  "+str(Odds[2][2]),command=self.clcikBtnGB5)
        self.GB5.grid(row=9, column=0, columnspan=2, pady=10, sticky = "nsew")
        self.GB6=tk.Button(self.GameFrame, bg="lavender blush", text=str(Odds[2][3])+"  "+str(Odds[2][4]), command=self.clcikBtnGB6)
        self.GB6.grid(row=9, column=3, columnspan=2, pady=10, sticky = "nsew")

        self.cancelBtn=tk.Button(self.GameFrame, bg="AntiqueWhite1", text="清除下注", command=self.clickcancelBtn)
        self.cancelBtn.grid(row=10, column=4, columnspan=2, padx=5, pady=20, sticky="nsew")
        self.okBtn(self.GameFrame, bg="AntiqueWhite1", text="確定",command=self.clickokBtn(final_g))
        self.okBtn(row=10, column=6, columnspan=2, padx=5, pady=20, sticky="nsew")

        
        """
        新增
        """
        
        self.betnumLbl=tk.Label(self.GameFrame, text="下注數量：",, justify="left")
        self.betnumLbl.grid(row=3, column=9, columnspan=2, pady=5, padx=5)
        self.var_betnum=tkStringVar()
        self.betnumEnt=tk.Entry(self.GameFrame, textvariable=self.var_betnum)
        self.betnumEnt.grid(row=3, column=11, columnspan=2, pady=5, padx=5)
        global betnum
        
        self.Words=tk.Label(self.GameFrame, text="個組合，每組合投注金額10元x", justify="left")
        self.Words.grid(row=4, column=9, columnspan=2, pady=5, padx=5)
        self.Words2=tk.Label(self.GameFrame, text="最高可中：", justify="left")
        self.Words2.grid(row=5, column=9, columnspan=2, pady=5, padx=5)



        # 按確認後改 或是按每個按鈕後改
        content=self.Words.cget("text")
        self.Words.configure(text= str(len(betlist))+content+str(betnum))
        
        
        content2=self.Words2.cget("text")
        Max = len(betlist)*10*betnum
        self.Words2.configure(text=content+str(Max))

    

            
        


        """
        回傳 string 的投注數（只限整數）
        """

        # 確認（關視窗）儲存所有下注內容
        # 每點一次按鈕都要確認一次顯示幕上的東西，不能把content寫外面？
        # 單雙（總分）
        
    def clickBtnGB1(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"單雙（總分）     單  1.75", justify="left")
        self.GB1.configure(state="disabled")
        self.GB2.configure(state="disabled"）
        
        

    def clickBtnGB2(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"單雙（總分）     雙  1.75", justify="left")
        self.GB1.configure(state="disabled")
        self.GB2.configure(state="disabled")
        
        
    # 大小（總分）
    def clickBtnGB3(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"大小（總分）  "+Odds[1][1]+"     1.75", justify="left")
        self.GB3.configure(state="disabled")
        self.GB4.configure(state="disabled")
        
    def clickBtnGB4(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"大小（總分）  "+Odds[1][3]+"     1.75", justify="left")
        self.GB3.configure(state="disabled")
        self.GB4.configure(state="disabled")
        count+=1
        Sure[3]=1
    # 不讓分
    def clickBtnGB5(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"不讓分    "+Odds[2][1]+"  "+Odds[2][2], justify="left")
        self.GB5.configure(state="disabled")
        self.GB6.configure(state="disabled")
        

    def clickBtnGB6(self):
        content = self.showL.cget("text")
        self.showL.configure(text=content+"\n"+"不讓分    "+Odds[2][3]+"  "+Odds[2][4], justify="left")
        self.GB5.configure(state="disabled")
        self.GB6.configure(state="disabled")
        

    # 取消用的函數（一次全部取消）
    def clickcancelBtn(self):
        self.GB1.configure(state="normal")
        self.GB2.configure(state="normal")
        self.GB3.configure(state="normal")
        self.GB4.configure(state="normal")
        self.GB5.configure(state="normal")
        self.GB6.configure(state="normal")
        self.showL.configure(text="")
        count=0
    

    def clickokBtn(final_g):
        """
        下注組希望回傳的資訊形式
        """
        
        betlist=[0,0,0,0,0,0,0,0,0]
        betlistMax.append(betlist*3)
        betlist[0]=time # type(time)=string
        betlist[1]=teamA
        betlist[2]=teamB
        betlist[3]=arena
        if :
            




            betnum=self.betnumEnt.get()
            try:
                int(betnum)
                if betnum<0:
                    tk.messagebox.showwarning("Warning", "請輸入正整數")
                else:
                    betlist[7]=betnum
            except:
                tk.messagebox.showwarning("Warning", "請輸入正整數")
            betlistMax.append(bestlist)

        return betlistMax

    
    """
    [['時間', 'A隊', 'B隊', '地點', '大小(總分)', '大', 1.75 ,2],
     ['時間', 'A隊', 'B隊', '地點', '單雙(總分)', '小於X分', 1.75, 2],
     ['時間', 'A隊', 'B隊', '地點', '賭法', '方向', 賠率, 投注數]]
    """



            return 