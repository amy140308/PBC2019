# List1=[0,0,0,0,0]
# List2=[0,0,0,0,0]
# List3=[0,0,0,0,0]

# BigList=[]
# BigList.append(List1)
# BigList.append(List2)
# BigList.append(List3)
# BigList[0][1]=5
# print(BigList)
# BigListStr=str(BigList)
# user_info=[3,4,5,6,6]
# user_info.append([])
# print(user_info)

# import ast
# stringList="[['單雙', '單', 1.75, '雙', 1.75], ['大小(總分)', '大於X分', 1.75, '小於X分', 1.75], ['不讓分', 'A隊名', 'A賠率', 'B隊名', 'B賠率']]"
# aList="[5,6,7]"
# List = ast.literal_eval(BigListStr)

# print(List)
# # for i in range(len(List)):
#    # print(List[i][2])
import csv
import pandas as pd

username="mm"

df=pd.read_csv("/Users/yangqingwen/Downloads/userInformation.csv")


df=df[df.Username != username]
# df.drop(index = df[df["Username"]].isin([username]), index=0)
# df.drop_duplicates(inplace=True)
df.to_csv("/Users/yangqingwen/Downloads/userInformation.csv", index=False)

# 把修改後的user_info增加至csv檔中的最後一項
# usr_list=['123', '123', 10000, '17:53'] 我隨便打的

df.loc[len(df)] = user_info

# 存檔

# df.to_csv("/Users/yangqingwen/Desktop/PBC2019/userInformation.csv", index = False)