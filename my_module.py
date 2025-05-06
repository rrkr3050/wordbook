import pandas as pd
import numpy as np
import time
import datetime
import os

print("現在の作業ディレクトリ:", os.getcwd())
print("ファイルの絶対パス:", os.path.abspath('decks/diction1.csv'))
print("存在するか？", os.path.exists('decks/diction1.csv'))

module_dir = os.path.dirname(__file__)
csv_path = os.path.join(module_dir, 'decks', 'diction1.csv')

print("読み込みパス:", csv_path)

words1 = pd.read_csv(csv_path,encoding = "cp932")

#showinfo
def get_newest_playdate(infodf):
    lastplay_list = infodf["lastplay"].to_list()
    newest_playdate = int(str(max(lastplay_list))[:-4])
    print("get_newest_playdate","newest_playdate :",newest_playdate)
    return newest_playdate
#showinfo

#指定のcolmnsの値の合計値を返す
def sum_df(df,columns):
    list_raw = df[columns].to_list()
    return sum(list_raw)

def sum_alllearning(folderpath):
    sum_allcount = 0
    files = os.listdir(folderpath)
    for i in files:
        deck_df = pd.read_csv(folderpath + str(i),encoding = "cp932")
        sum_allcount += sum_df(deck_df,"leaning_count")
        
    return sum_allcount

def sum_todaylearning(infodf):
    todayplays_list = infodf["today_plays"].to_list()
    today_plays = sum(todayplays_list)
    return today_plays
        
#連続学習日数を加算するかどうかの判断
def lastplay_date_is_today(infodf):
    lastplay_list_int = []
    lastplay_list = infodf["lastplay"].to_list()
    print("lasyplay_data_is_today","lastplay_list :" ,lastplay_list)
    for i in lastplay_list:
        lastplay_list_int.append(int(i))
    
    lastplay = max(lastplay_list_int)
    
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    nowtime = now.strftime('%Y%m%d%H%M')
    
    return  nowtime[:8] == str(lastplay)[:8]

def lastplay_date_is_yesterday(infodf):
    lastplay_list = infodf["lastplay"].to_list()
    lastplay_list_int = []
    for i in lastplay_list:
        lastplay_list_int.append(int(i))
    
    lastplay = max(lastplay_list_int)
    
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    nowtime = now.strftime('%Y%m%d%H%M')
    yesterday = int(nowtime[:8]) - 1

    return  str(yesterday) == str(lastplay)[:8]

def lastplay_updating(infodf,deckname):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    nowtime = now.strftime('%Y%m%d%H%M')
    print("lastplay_updating",infodf[infodf["deckname"]==deckname])
    #nowdeck_index = infodf.index.get_loc
    infodf["lastplay"][infodf["deckname"]==deckname]  = str(nowtime)
    print("lastplay_updating","infodf :",infodf)
    print("lastplay_updating","end",str(nowtime))
    return infodf
    



#学習終了後のdfの情報をinfoに記録
def write_to_info(df,info_df,deckname):
    plays = sum_df(df,"leaning_count")
    mistakes = sum_df(df,"mistakes")
    close = sum_df(df,"close")
    corrects = sum_df(df,"corrects")
    pri_sum = sum_df(df,"f_rate")
    n_of_cards = len(df["f_rate"].to_list())
    pri_ave = pri_sum / n_of_cards
    
    deckslist = info_df["deckname"].to_list()
    n_of_decks = len(deckslist)
    print("write_to_info","deckslist :",deckslist)
    if deckname not in deckslist:
        print("write_to_info","デッキ名発見せず")
        info_df.loc[n_of_decks,"deckname"] = deckname
        target_no = n_of_decks
    else:
        print("write_to_info","デッキ名発見")
        for i in range(len(deckslist)):
            if deckslist[i] == deckname:
                target_no = i
                break

    print("target_no",target_no)

    info_df.loc[target_no,"cards"] = n_of_cards
    info_df.loc[target_no,"today_plays"] += info_df.loc[target_no,"cards"]
    info_df.loc[target_no,"laps"] += 1
    info_df.loc[target_no,"ave_priority"] = pri_ave
    info_df.loc[target_no,"cardplays"] = plays
    info_df.loc[target_no,"mistakes"] = mistakes
    info_df.loc[target_no,"close"] = close
    info_df.loc[target_no,"corrects"] = corrects
    
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    info_df.loc[target_no,"lastplay"] = now.strftime('%Y%m%d%H%M')
    print("write_to_info","")
    return info_df
    
    
    
def count_allcn(restcn):
    count = 0
    for i in restcn:
        print(i)
        if type(i) == list:
            count += len(i)
        elif i[:-1] == "waypoint":
            continue
        elif i == "end":
            print("おわり" ,count)
            return count
    
        
        
    
    
    
    
    
#グループごとのpriorityの平均値をリストとして返す関数
def pri_ave_list(doublelist,columns,dataframe):
    #print("pri_ave_list",doublelist,columns,dataframe)
    ave_list = []
    gr_pri_ave = 0
    temp = 0
    for a in range(len(doublelist)):
        #print(a)
        for i in doublelist[a]:
            temp += dataframe.loc[i,columns]
            #print("pri_ave_list","priority",dataframe.loc[i,columns])
        #print("pri_ave_list","追加するtemp :",temp)
        ave_list.append(temp / len(doublelist[a]))
        temp = 0
    return ave_list

#priorityは学習の優先度であり、ユーザーにとっては学習のだるさでもある。
#restcn作成関数


temp_offsetcn = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
print("offset_cn_list",temp_offsetcn)

##生成されたoffsetcnリストから、priorityが低いものを消してリストを返す
def del_low_pri(cnlist,pri_threshold,dataframe):
    #priorityがthreshold以上の単語を再生する。
    print("del_low_pri","dataframe :" ,dataframe)
    restcn = []
    for i in cnlist:
        if dataframe.loc[i,"f_rate"] >= pri_threshold:
            restcn.append(i)
            
    return restcn
##生成されたoffsetcnリストから、priorityが低いものを消してリストを返す
updated_cnlist = del_low_pri(temp_offsetcn,96,words1)
print("del_low_pri",updated_cnlist)


##指定の語数ずつにグループ化
def become_group(cnlist,groupcount):
    groupline = groupcount
    group = []
    grouplist = []
    cn_count = len(cnlist)
    for i in cnlist:
        
        if i < groupline:
            group.append(i)
            
            if i == cnlist[-1]:
                grouplist.append(group)
                grouplist.append("end")
                break
            
        else:
            #newgroup
            #print("group作成 :",group)
            waypoint_numb = groupline / groupcount
            grouplist.append(group) 
            grouplist.append("waypoint"+ str(int(waypoint_numb)) )
            group = []
            group.append(i)
            
            if i == cnlist[-1]:
                grouplist.append(group)
                grouplist.append("end")
                break
            
            #grouplineの更新
            while i >= groupline:
                groupline += groupcount
                
    return grouplist
##指定の語数ずつにグループ化
grouplist = become_group(updated_cnlist,5)
print("become_group",grouplist)


##リスト内の数みてプレイするグループリスト作成
def play_group_adjust(grouplist,numb_of_play):
    play_grouplist = []
    count = 0
    for i in grouplist:
        if type(i) == str:
            play_grouplist.append(i)
            continue
        if count >= numb_of_play:
            break
        elif len(i) != 0:
            play_grouplist.append(i)
            count += len(i)
        
    return play_grouplist
##指定した枚数を超えるようにプレイグループを追加

grouplist_2 = play_group_adjust(grouplist,100)
print("play_group_adjust",grouplist_2)

##restcnの最終決定
def finalize_restcn(cnlist,pri_threshold,dataframe,groupcount,numb_of_play):
    deleted = del_low_pri(cnlist,pri_threshold,dataframe)
    doublelist = become_group(deleted,groupcount)
    restcn = play_group_adjust(doublelist,numb_of_play)
    return restcn
##restcnの最終決定

restcn = finalize_restcn(temp_offsetcn,96,words1,7,100)
print(restcn)
#グループのpriをみて再生するgroupを決定
#習得とは、priority<95の単語を指す
##ex,gr_priorityが94になったらでないやつのほうが多い状態
#doulelistを読み込み、再生するべきグループのcnリストを返す




#temp_group = [0,1,2,3,4]
#restcn = make_restcn(temp_group,102,"priority",words1)
#print(restcn)
temp_offsetcn = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]]

#gr_ave_list = pri_ave_list(temp_offsetcn,"priority",words1)
#print(gr_ave_list)
#play_cn_list = adopt_group_make_restcn(temp_offsetcn,gr_ave_list,90,96,words1)
#print("adopt_group_make_restcn",play_cn_list)

restcn =[]
#for i in play_cn_list:
    #restcn += del_low_pri(i,96,words1)
#print("make_restcn",restcn)

#上3つを合わせる。
def finalize_restcn_old(doublelist,group_pri_thresshold,pri_threshold,dataframe):
    restcn = []
    gr_ave_list = pri_ave_list(doublelist,"f_rate",words1)
    play_cn_doublelist = adopt_group_make_restcn(doublelist,gr_ave_list,group_pri_thresshold,pri_threshold,dataframe)
    
    #グループごとにwaypoint表示するための設定
    
    
    for i in range(len(play_cn_doublelist)):
        restcn += make_restcn(play_cn_doublelist[i],pri_threshold,"f_rate",dataframe)
        if i+1 == len(play_cn_doublelist):
            restcn.append("deck_end")
        else:
            restcn.append("waypoint" + str(i+1))
    return restcn

def making_color(dataframe,cn):
    
    color = []
    l_count  = dataframe.loc[cn,"learning_count"]
    mis_count = dataframe.loc[cn,"learning_count"]
    correct_rate = (1- (mis_count/l_count))*100
    if l_count <= 10:
        color = [240,240,240,1]
    else:
        if  98 <= correct_rate:
            color = []
        elif 70 <= correct_rate < 98:
            color = []
        elif 40 <= correct_rate < 70:
            color = []
        elif correct_rate < 40:
            color = []
        else:
            print("error")
        
    return color
#cardback_ansbutton各種
def change_perameter_mis(dataframe,cn):
    dataframe.loc[cn,"addday"] = time.time()
    dataframe.loc[cn,"mistakes"] += 1
    dataframe.loc[cn,"f_rate"] += 2
    dataframe.loc[cn,"r_range"] = int(dataframe.loc[cn,"r_range"]/2)
    
    
def change_perameter_dif(dataframe,cn):
    dataframe.loc[cn,"addday"] = time.time()
    dataframe.loc[cn,"close"] += 1
    
    
def change_perameter_cor(dataframe,cn):
    dataframe.loc[cn,"addday"] = time.time()
    dataframe.loc[cn,"corrects"] += 1
    
    r_range = dataframe.loc[cn,"r_range"]
    dataframe.loc[cn,"f_rate"] -= (1 + r_range)
    dataframe.loc[cn,"r_range"] += 1
    

def mistakecard_relearning(restcn):
    restcn[0].append(restcn[0][0])
    return restcn


def card_check_changescreen(restcn):
    screenname = ""
    print("card_check_changescreen","restcn[0][0]",restcn[0][0])
    del restcn[0][0]
    next_cn = restcn[0]
    if next_cn == []:
        del restcn[0]
    if type(restcn[0]) == list and len(next_cn) != 0:
        screenname = 'front'
        
    elif restcn[0][:-1] == "waypoint":
        group = restcn[0][-1]
        screenname = 'waypoint'
        del restcn[0]

    elif restcn[0] == "end":
        screenname = 'end'
        del restcn[0]
    
    print("my_module","changescreen","restcn :",restcn)
    return screenname
#restcn = finalize_restcn(temp_offsetcn,94,95,words1)
#print(restcn)

def consec_change(data):
    if not lastplay_date_is_today(data):
        if lastplay_date_is_yesterday(data):
            data.loc[0,"consec_days"] += 1
        else:
            data.loc[0,"consec_days"] = 0