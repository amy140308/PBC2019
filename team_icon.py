import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk

import PIL
from PIL import ImageTk, Image

root = tk.Tk()
root.title("隊伍資訊")
root.geometry("500x500")


# 創建畫布
canvas = tk.Canvas(root, width = 500, height = 1500, bg = "lemon chiffon")  #height調整canvas的長度，要手動調（或寫def）
canvas.pack(side = BOTTOM,fill = BOTH,expand = Y)
# 要建立frame，透過create_widget放在canvas上面才能滾動
F1 = tk.Frame(root,bg = "misty rose",width = 500, height = 300)
F1.pack(side = TOP,fill = BOTH) 


frame = tk.Frame(canvas, bg = "lemon chiffon",width = 500, height = 1200)
frame.pack(side = BOTTOM, fill = BOTH)
canvas.create_window((300,300), window = frame, anchor = NW) 
# 滾動條
gameBar = tk.Scrollbar(canvas, orient = "vertical", command = canvas.yview)
gameBar.pack(side = "right", fill = "y")
canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=gameBar.set)

functions = ["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
for function in reversed(functions):
    btn=tk.Button(F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
    btn.pack(side=RIGHT, pady=30, anchor=N)

# 放賽事
wow=tk.Label(frame, text="球隊介紹", font="Didot",bg="lemon chiffon").pack(side = TOP)

def click_team_button(btn_txt):
    window = Toplevel(root)
    window.title(btn_txt)
    window.geometry("300x500")

imageteam = Image.open("C:\co-work\ATL_logo.png")
imageteam = imageteam.resize((100, 100), Image.ANTIALIAS)
button_team = tk.Button(frame, image = imageteam)
button_team.pack(side=TOP, pady=10, padx=20)



root.mainloop()