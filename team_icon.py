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
F1 = tk.Frame(root,bg = "wheat2",width = 500, height = 300)
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
    btn = tk.Button(F1, height = 2, width = 10, relief = tk.FLAT, bg = "lemon chiffon", fg = "sienna4", font = "Didot", text = function)
    btn.pack(side = RIGHT, pady = 30, anchor = N)

# 放賽事
PageLabel=tk.Label(frame, text="球隊介紹", font="Didot", bg="lemon chiffon").pack(side = TOP)

def click_team_button(btn_txt):
    window = Toplevel(root)
    window.title(btn_txt)
    window.geometry("300x500")


Logo_road_list = ["C:\\logo\\ATL_logo.png","C:\\logo\\BKN_logo.png","C:\\logo\\BOS_logo.png","C:\\logo\\CHA_logo.png",
             "C:\\logo\\CHI_logo.png","C:\\logo\\CLE_logo.png","C:\\logo\\DAL_logo.png","C:\\logo\\DEN_logo.png",
             "C:\\logo\\DET_logo.png","C:\\logo\\GSW_logo.png","C:\\logo\\HOU_logo.png","C:\\logo\\IND_logo.png",
             "C:\\logo\\LAC_logo.png","C:\\logo\\LAL_logo.png","C:\\logo\\MEM_logo.png","C:\\logo\\MIA_logo.png",
             "C:\\logo\\MIL_logo.png","C:\\logo\\MIN_logo.png","C:\\logo\\NOP_logo.png","C:\\logo\\NYK_logo.png",
             "C:\\logo\\OKC_logo.png","C:\\logo\\ORL_logo.png","C:\\logo\\PHI_logo.png","C:\\logo\\PHX_logo.png",
             "C:\\logo\\POR_logo.png","C:\\logo\\SAC_logo.png","C:\\logo\\SAS_logo.png","C:\\logo\\TOR_logo.png",
             "C:\\logo\\UTA_logo.png","C:\\logo\\WAS_logo.png"]
Logo_image_list = []
Frame_List = []

logo_account = 0

for i in range(30):
    logo_account += 1
    
    # 用image抓取png檔並resize
    logo_image = Image.open(Logo_road_list[i])
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    # 用「ImageTk.PhotoImage」轉換成tk可以讀的樣子
    logo_image = ImageTk.PhotoImage(image = logo_image)
    Logo_image_list.append(logo_image)
    
    if logo_account % 5 == 1:
        team_frame = tk.Frame(frame, bg = "ivory2",width = 620, height = 200)
        Frame_List.append(team_frame)
        team_frame.pack(side = TOP, pady = 10, padx = 20, anchor = NW)  
        
        button_logo = tk.Button(team_frame, image = Logo_image_list[i])
        button_logo.pack(side = LEFT, pady = 10, padx = 20, anchor = NW)  
    else:
        button_logo = tk.Button(team_frame, image = Logo_image_list[i])
        button_logo.pack(side = LEFT, pady = 10, padx = 20, anchor = W)

root.mainloop()