import csv

# 記得先跑team_v2.py
# 讀已經抓下來的30隊csv
"""
記得改filepath 
"""
filepath = ''
wf = open(file=filepath, mode="r", encoding="utf-8")
rows = csv.reader(wf)

name = input()  # 記得這邊是讓你們輸隊名
info = []
player = []
game = []

count = 0
for i in rows:
    if i[0] == name:
        count = 1
        info = i
    
    elif 1 <= count and count <= 5:
        player.append(i)
        count += 1
    elif 6 <= count and count <= 11:
        game.append(i)
        count += 1
    elif count == 12:
        game.append(i[0])
        count += 1
    elif count > 13:
        break
wf.close

# 這下面也不用
print(info)
print(player)
print(game)
