import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import PIL
from PIL import ImageTk, Image

root = tk.Tk()
root.title("隊伍資訊")
root.geometry("500x500")


# 創建畫布
canvas = tk.Canvas(root, width = 500, height = 600, bg = "lemon chiffon")  #height調整canvas的長度，要手動調（或寫def）
canvas.pack(side = BOTTOM,fill = BOTH,expand = Y)
# 要建立frame，透過create_widget放在canvas上面才能滾動
F1 = tk.Frame(root,bg = "misty rose",width = 500, height = 300)
F1.pack(side = TOP,fill = BOTH) 

frame = tk.Frame(canvas, bg = "lemon chiffon", width = 500, height = 1200)
frame.pack(side = BOTTOM, fill = BOTH ,expand=TRUE)
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
f0=tkFont.Font(family="標楷體", size=20)
wow=tk.Label(frame, text="球隊介紹", font=f0 ,bg="lemon chiffon").pack(side = TOP)

# 打開隊伍資訊
def click_team_button():
    window = Toplevel(root)
    window.title("hey")
    window.geometry("300x500")
    
    F10 = tk.Frame(window, bg = "wheat2", width = 500, height = 300)
    F10.pack(side = TOP, fill = BOTH) 

Logo_road_list = ["/Users/yangqingwen/Desktop/team_logo/ATL_logo.png","/Users/yangqingwen/Desktop/team_logo/BKN_logo.png","/Users/yangqingwen/Desktop/team_logo/BOS_logo.png","/Users/yangqingwen/Desktop/team_logo/CHA_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/CHI_logo.png","/Users/yangqingwen/Desktop/team_logo/CLE_logo.png","/Users/yangqingwen/Desktop/team_logo/DAL_logo.png","/Users/yangqingwen/Desktop/team_logo/DEN_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/DET_logo.png","/Users/yangqingwen/Desktop/team_logo/GSW_logo.png","/Users/yangqingwen/Desktop/team_logo/HOU_logo.png","/Users/yangqingwen/Desktop/team_logo/IND_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/LAC_logo.png","/Users/yangqingwen/Desktop/team_logo/LAL_logo.png","/Users/yangqingwen/Desktop/team_logo/MEM_logo.png","/Users/yangqingwen/Desktop/team_logo/MIA_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/MIL_logo.png","/Users/yangqingwen/Desktop/team_logo/MIN_logo.png","/Users/yangqingwen/Desktop/team_logo/NOP_logo.png","/Users/yangqingwen/Desktop/team_logo/NYK_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/OKC_logo.png","/Users/yangqingwen/Desktop/team_logo/ORL_logo.png","/Users/yangqingwen/Desktop/team_logo/PHI_logo.png","/Users/yangqingwen/Desktop/team_logo/PHX_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/POR_logo.png","/Users/yangqingwen/Desktop/team_logo/SAC_logo.png","/Users/yangqingwen/Desktop/team_logo/SAS_logo.png","/Users/yangqingwen/Desktop/team_logo/TOR_logo.png",
             "/Users/yangqingwen/Desktop/team_logo/UTA_logo.png","/Users/yangqingwen/Desktop/team_logo/WAS_logo.png"]
             
Logo_image_list = []
Frame_List = []

for i in range(30):
    
    # 用image抓取png檔並resize
    logo_image = Image.open(Logo_road_list[i])
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    # 用「ImageTk.PhotoImage」轉換成tk可以讀的樣子
    logo_image = ImageTk.PhotoImage(image = logo_image)
    Logo_image_list.append(logo_image)
    
    # 每五個建立新的Frame
    if i % 5 == 0:
        team_frame = tk.Frame(frame, bg = "wheat2",width = 1000, height = 120)
        Frame_List.append(team_frame)
        team_frame.pack(side = TOP, pady = 10, padx = 20, anchor = NW, fill = "x")  
    
    
    button_logo = tk.Button(team_frame, image = Logo_image_list[i], command = click_team_button)
    button_logo.pack(side = LEFT, pady = 10, padx = 20, anchor = NW, expand = True)

root.mainloop()