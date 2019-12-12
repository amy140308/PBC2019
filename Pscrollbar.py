import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk


# class GamesPage(tk.Frame):

#     def __init__(self):
#         tk.Frame.__init__(self) 
#         self.grid()
#         self.pack()
#         self.createWidgets()
#     def createWidgets(self):
#         self.gameBar=tk.Scrollbar(self,orient=tk.VERTICAL)
#         self.btn1=tk.Button(self, text="game1")
#         self.btn1.grid(row=0, column=0, columnspan=3, sticky=tk.E)
# G=GamesPage()
# G.mainloop()


import os 
root = tk.Tk()
root.title("賽事下注")
root.geometry("500x500")


List=["9:00	76人 @ 塞爾蒂克 \n TD花園球場", "9:30	騎士 @ 馬刺\nAT&T中心", "10:00	獨行俠 @ 活塞\nArena Ciudad de Mexico", "11:30	拓荒者 @ 金塊\n百事中心球場"]

lis=[]
for num in range(21):
   lis.append(num)
# 創建畫布
canvas=tk.Canvas(root, width=500, height=1200, bg="lemon chiffon")  #height調整canvas的長度，要手動調（或寫def）
canvas.pack(side=BOTTOM,fill=BOTH,expand=Y)
# 要建立frame，透過create_widget放在canvas上面才能滾動
F1=tk.Frame(root,bg="misty rose",width=500, height=300)
F1.pack(side=TOP,fill=BOTH) 


frame=tk.Frame(canvas, bg="lemon chiffon",width=500, height=1200)
frame.pack(side=BOTTOM, fill=BOTH)
canvas.create_window((300,300), window=frame, anchor=NW) 
# 滾動條
gameBar= tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
gameBar.pack(side="right", fill="y")
canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=gameBar.set)

functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
for function in reversed(functions):
    btn=tk.Button(F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
    btn.pack(side=RIGHT, pady=30, anchor=N)

# 放賽事
wow=tk.Label(frame, text="今日賽事", font="Didot",bg="lemon chiffon").pack()
def click_game_button(btn_txt):
    window=Toplevel(root)
    window.title(btn_txt)
    window.geometry("300x500")

for i in lis:
    btn = tk.Button(frame, height=2, width=30,relief=tk.RAISED,bg="lemon chiffon",fg="purple3",font="Dosis",text=i)
    btn_txt=btn.cget("text")
    btn.configure(command=click_game_button(btn_txt))
    btn.pack(side=TOP, pady=10, padx=20) # 不能用grid，顯示固定位置不能滑動

root.mainloop()
