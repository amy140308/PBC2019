# import tkinter as tk

# # Our first square root calculator
# class Calculator(tk.Frame):

#     def __init__(self):
#         tk.Frame.__init__(self)
#         # Frame寫的，可以產生視窗上的網格
#         self.grid()

# cal=Calculator()
# cal.master.title("My Cal") # Frame寫的函數：視窗那條標題字樣
# cal.mainloop() # show up

# 老師上課寫的計算機程式，參考對照tkinter的功能用

import tkinter as tk
import tkinter.font as tkFont
import math

class Calculator(tk.Frame):
    
    shouldReset=True #立一個旗
  
    def __init__(self):
        tk.Frame.__init__(self) 
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        f1=tkFont.Font(size=48, family="Helvetica")
        f2=tkFont.Font(size=32,family="Herculanum")
        # 計算機顯示幕 
        self.lblNum=tk.Label(self,text="0", height=1, width=10, font=f1)
        
        self.btnNum1=tk.Button(self,text="1", command=self.clickBtnNum1, height=1, width=10, font=f2)
        self.btnNum2=tk.Button(self,text="2", command=self.clickBtnNum2, height=1, width=10, font=f2)
        self.btnNum3=tk.Button(self,text="3", command=self.clickBtnNum3, height=1, width=10, font=f2)
        self.btnNum4=tk.Button(self,text="4", command=self.clickBtnNum4, height=1, width=10, font=f2)
        self.btnNum5=tk.Button(self,text="5", command=self.clickBtnNum5, height=1, width=10, font=f2)
        self.btnNum6=tk.Button(self,text="6", command=self.clickBtnNum6, height=1, width=10, font=f2)
        self.btnNum7=tk.Button(self,text="7", command=self.clickBtnNum7, height=1, width=10, font=f2)
        self.btnNum8=tk.Button(self,text="8", command=self.clickBtnNum8, height=1, width=10, font=f2)
        self.btnNum9=tk.Button(self,text="9", command=self.clickBtnNum9, height=1, width=10, font=f2)
        self.btnNum0=tk.Button(self,text="0", command=self.clickBtnNum0, height=1, width=8, font=f2)
        
        self.btnSqrt=tk.Button(self,text="s", command=self.clickBtnSqrt, height=1, width=8, font=f2) 
        # self.btnClose=tk.Button(self, text="close",commad=self.master.destroy, height=1, width=8, font=f1)
        
        self.lblNum.grid(row=0, column=0, columnspan=3)
        self.btnNum1.grid(row=1,column=0)
        self.btnNum2.grid(row=1,column=1)
        self.btnNum3.grid(row=1,column=2)
        self.btnNum4.grid(row=2,column=0)
        self.btnNum5.grid(row=2,column=1)
        self.btnNum6.grid(row=2,column=2)
        self.btnNum7.grid(row=3,column=0)
        self.btnNum8.grid(row=3,column=1)
        self.btnNum9.grid(row=3,column=2)

        # 最下面一行
        self.btnNum0.grid(row=4,column=0, columnspan=2)
        self.btnSqrt.grid(row=4,column=2) 
    def clickBtnNum0(self):
        self.lblNum.configure(text="0")

    def clickBtnNum1(self):
        self.lblNum.configure(text="1")
    def clickBtnNum2(self):
        self.lblNum.configure(text="2")
    def clickBtnNum3(self):
        self.lblNum.configure(text="3")
    def clickBtnNum4(self):
        self.lblNum.configure(text="4")
    def clickBtnNum5(self):
        self.lblNum.configure(text="5")
    def clickBtnNum6(self):
        self.lblNum.configure(text="6")
    def clickBtnNum7(self):
        self.lblNum.configure(text="7")
    def clickBtnNum8(self):
        self.lblNum.configure(text="8")
    def clickBtnNum9(self):
        self.lblNum.configure(text="9")   
    def clickBtnSqrt(self):
        curNum = float(self.lblNum.cget("text"))
        self.lblNum.configure(text=str(round(math.sqrt(curNum),2)))  # configure，對元件進行補充改動
        self.shouldReset=True
        # cget取得當前計算得出的數字（lblNum是顯示欄）
    def setNumStr(self,content):
        if self.shouldReset==True:
            self.lblNum.configure(text=content)
            self.shouldReset=False
        else:
            self.lblNum.configure(text=self.lblNum.cget("text")+content)
            

    def clickBtnNum1(self):
        self.setNumStr("1")

    def clickBtnNum2(self):
        self.setNumStr("2")

    def clickBtnNum3(self):
        self.setNumStr("3")

    def clickBtnNum4(self):
        self.setNumStr("4")

    def clickBtnNum5(self):
        self.setNumStr("5")

    def clickBtnNum6(self):
        self.setNumStr("6")

    def clickBtnNum7(self):
        self.setNumStr("7")

    def clickBtnNum8(self):
        self.setNumStr("8")

    def clickBtnNum9(self):
        self.setNumStr("9")

    def clickBtnNum0(self):
        self.setNumStr("0")

cal = Calculator()
cal.master.title("My Calculator")
cal.mainloop()
# REMOVE MARGINS：see c04-06

