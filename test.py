import os
import pandas as pd
import time
import datetime
text = "123456"
endlist = []

infodf = pd.read_csv("info.csv",encoding = "cp932")

endlist = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
del endlist[0]



t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
nowtime = now.strftime('%Y%m%d%H%M')
#print(nowtime[:8])
deckname = "diction1"


list1 = [1,2,3,4,5,6,7,8,9,10]

print(list1[:8])
