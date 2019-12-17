
import datetime


yesterday=datetime.datetime.now()-datetime.timedelta(days=1)




dstr=yesterday.strftime("%Y-%m-%d")
print(dstr)
#final_h = history.get_data(dstr)
