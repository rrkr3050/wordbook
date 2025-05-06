from ast import Pass
from turtle import back
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.factory import Factory
from kivy.graphics import Color,RoundedRectangle
#from cgi import test
from operator import index
from kivy.uix.button import Button
from kivy.lang import Builder
from this import d
from types import ClassMethodDescriptorType
import pandas as pd
import numpy as np
import csv
import datetime
import time
import os
from kivy.clock import Clock
from time import sleep
import threading
import glob
import pathlib
import my_module

from kivy.logger import Logger
from kivy.logger import LoggerHistory
Logger.setLevel('DEBUG')
Logger.debug("This is a debug message")
print(LoggerHistory.history)

print("現在の作業ディレクトリ:", os.getcwd())
print("ファイルの絶対パス:", os.path.abspath('combination/decks/diction1.csv'))
print("存在するか？", os.path.exists('combination/decks/diction1.csv'))


texttest = "aaaa"

group_size = 5
#１グループ5単語として作成する

#ホーム画面追加したい
files = os.listdir("./")
if "decks" in files and len(files) != 0:
    decks = os.listdir("./decks")
    print("デッキリスト :",decks)
    deck = decks[0]
    deck[:-4]
    deckname = deck[:-4]
elif "decks" not in files:
    os.mkdir("./decks")
elif len(files) != 0:
    print("デッキないで")






words1 = pd.read_csv('decks/diction1.csv',encoding = "cp932")
words2 = pd.read_csv('decks/diction2.csv',encoding = "cp932")


words = words1
allcount = len(words)
print("allcount",allcount)

resource_add_path('kivy/fonts')
LabelBase.register(DEFAULT_FONT, './fonts/Koruri-Regular.ttf')
#日本語フォント導入


cardno = 1
#frontword = words.loc[cardno,"front"]
#backword = words.loc[cardno,"back"]

#homegamen

class homewindow(Screen):
    #widgetクラスを継承してる。widgetクラスはkivyに標準搭載してるから使える。
    text = StringProperty()
    newdeckname = StringProperty()
    deckpath = StringProperty()
    numb = 0
    words = words1
    restcn = []
    want_to_plays = 10
    #restcn = [0,999999]
    #9999の理由不明
    print("ホームウィンドウ")
    
    #def __init__(self,**kwargs):
        #super(homewindow, self).__init__(**kwargs)
    def __init__(self,**kwargs):
        super(homewindow, self).__init__(**kwargs)
        
        homewindow.info_df = pd.read_csv('info.csv',encoding = "cp932")
        print("homewindow","init","homewindow.info_df :",homewindow.info_df)
    #追加デッキのボタンに搭載する関数は同じ物を使う
    #関数は変えずに、外部からその関数に用いる変数を変更することで別のデッキに対応する
    
    def on_pre_enter(self):
        homewindow.alllearnings = my_module.sum_alllearning("./decks/")
        self.ids.info_alllearnings.text = "総学習数 :" + str(homewindow.alllearnings)
        
        homewindow.todayplays = my_module.sum_todaylearning(homewindow.info_df)
        self.ids.info_todaylearnings.text = "今日の学習数 :" + str(homewindow.todayplays)
        print("homewindow","on_pre_enter","last_istoday :",my_module.lastplay_date_is_today(homewindow.info_df))
        print("homewindow","on_pre_enter","last_isyester :",my_module.lastplay_date_is_yesterday(homewindow.info_df))
        if not my_module.lastplay_date_is_today(homewindow.info_df):
            if my_module.lastplay_date_is_yesterday(homewindow.info_df):
                homewindow.info_df.loc[0,"consec_days"] += 1
            else:
                homewindow.info_df.loc[0,"consec_days"] = 0
        
    def showinfo(self):
        my_module.showinfo("info.csv")





    def decksreload(self):
        files = os.listdir("./decks")
        decklist = []
        decks_numb = len(files)
        for i in range(decks_numb):
            
            filename = files[i]
            decklist.append(filename[:-4])
            homewindow.filename = filename
            homewindow.newdeckpath = "./decks/" + filename
            homewindow.newdeck = pd.read_csv(homewindow.newdeckpath,encoding = "cp932")
            #homewindow.newdeckname = homewindow.newdeck.loc[0,"deck"]
            
            Newbutton = Addedbutton()
            Box_inscroll = self.ids.bola1
            Box_inscroll.add_widget(Newbutton)
        info_df = pd.read_csv("info.csv",encoding = "cp932")
        homewindow.info_decklist = info_df["deckname"].to_list()
        newestdate = my_module.get_newest_playdate(info_df)
        print("homewindow","decksreload","newestdate :",newestdate)
        print("homewindow","decksreload","df_dictin1 :",info_df[info_df["deckname"]=="diction1"])
        #print("homewindow","decksreload","df_dictin1 :",info_df[info_df["deckname"]=="diction1"].loc[0]["lastplay"])
        print("homewindow","decksreload","info_df :",info_df)
        #print("homewindow","decksreload","[diction1] :",info_df[info_df["deckname"]=="diction1"].loc[0]["lastplay"])
        print("homewindow","decksreload","info_df :",info_df)
        
        #if info_decklist != decklist:
        
        
        



    def Addbutton(self):
        #Addedbutton.deckpath = 'decks/diction.csv'
        Newbutton = Addedbutton()
        #Newbutton.text = "new"
        Box_inscroll = self.ids.bola1
        Box_inscroll.add_widget(Newbutton)
        files = os.listdir("./decks")


    def reset(self):
        #self.parent.remove_widget(cardback(name='back'))
        homewindow.restcn = [0]

class Addedbutton(Button):
    previous_deckname =StringProperty()
    deckname =StringProperty()
    check_first = 1
    def __init__(self,**kwargs):
        super(Addedbutton, self).__init__(**kwargs)
        print("Addedbutton_init","スタート")
        
        self.deckpath = homewindow.newdeckpath
        self.deck = homewindow.newdeck
        self.text = homewindow.filename[:-4]
        self.offset_cn = homewindow.newdeck.index.values.tolist()
        self.gr_pri_list = []
        print("Addedbutton","init","self.offset_cn",self.offset_cn)
        
        print("Addedbutton","init","_ラスト",self.text,"デッキセット")
    @staticmethod
    def restcn():
        return homewindow.restcn[0][0]
    def go_deck(self):
        print("Addedbutton","go_deck","スタート")
        #if len(homewindow.restcn[]) == 0:
        
        #一定時間経過しているカードのpriority増加
        for i in range(len(homewindow.words)):
            if time.time() - homewindow.words.loc[i,"addday"] > 10:
                homewindow.words.loc[i,"f_rate"] += 1
                #最終学習日から一日以上経過している単語はpriorityをインクリメント
        #一定時間経過しているカードのpriority増加

        
        #rest_cnの生成
        print("Addedbutton","go_deck","rest_cnの生成")
        #priority>97の単語をrestcnに追加
        #基本pri順に追加し、102以上は同じものと扱う。
        #必要な情報:"いくつグループをプレイするか",""
        #1グループ目のgr_priが94を下回ったらしたら2グループ目もrestcnに追加する。
        print()
        
        group_numb = 50
        
        pri_threshold = 95
        wantplays = 100
        
        #homewindow.words→self.deckに変更
        #↑でエラー解決したっぽい
        homewindow.restcn = my_module.finalize_restcn(self.offset_cn,95,self.deck,group_numb,wantplays)
        print("Addedbutton","go_deck","restcn :",homewindow.restcn)
        if not homewindow.restcn:
            print("警告: デッキが空か、条件に合うカードがありません。")
            homewindow.restcn = [[0]]
        
        
        
        
        homewindow.nowdeckpath = self.deckpath
        homewindow.nowdeckname = self.text
        #現在プレイしているデッキのpathをここに保存
        print(homewindow.nowdeckpath)
        print("Addedbutton","go_deck","プレイデッキ名:",self.text)
        print("Addedbutton","go_deck","プレイデッキ:",self.deck)
        print("Addedbutton","go_deck","selfdeckのindex",self.deck.index.values.tolist())
        print("Addedbutton","go_deck","cnリストオフセット:",self.offset_cn)
        print("Addedbutton","go_deck","現在のcnリスト:",homewindow.restcn)
        print("Addedbutton","go_deck","初プレイチェック:",self.check_first)
        print("Addedbutton","go_deck","前回のデッキ名",Addedbutton.previous_deckname)
        if Addedbutton.previous_deckname != self.text:
            self.check_first = 1
            #homewindow.restcn == [0,999999]
            
        #Addedbutton.previous_deckname = self.text

        if len(homewindow.restcn) == 0 or homewindow.restcn == [0,999999] or self.check_first == 1:
            print("新規プレイ")
            print("cnリストオフセット:",self.offset_cn)
            
            #offcetの時点で
            
            
            #デッキの単語カードのインデックスをすべてrestcnに追加
            print("現在のcnリスト",homewindow.restcn)
            #デッキ固有のオフセットcnをセット
            homewindow.words = self.deck
            #print(go_deck,init,)
            print("go_deck,init,restcn",homewindow.restcn)

        else:
            #print("self.offset_cn",self.offset_cn)
            homewindow.words = self.deck
            print("restcn_list",homewindow.restcn)
            print("restcn[0]",homewindow.restcn)
        #選択したデッキのindexをリストで取得
        homewindow.allcount = len(homewindow.words)
        
        #homewindow.deckname = homewindow.words.loc[cardback.cn,"deck"]
        #cardfront.deckname = cardback.deckname = homewindow.deckname
        self.check_first = 0
        self.parent.parent.parent.parent.manager.current = 'beforedeck'



class cardfront(Screen):
    #widgetクラスを継承してる。widgetクラスはkivyに標準搭載してるから使える。
    text = StringProperty()
    deckname = StringProperty()
    front_color = ListProperty([])
    print("カードフロント")


    def __init__(self,**kwargs):
        super(cardfront, self).__init__(**kwargs)
        
        
    #initにより初期処理が動くから、ここで追加する
    def on_pre_enter(self):
        print("cardfront","on_pre_enter","start")
        
    


        
        #最終更新日を更新
        if type(Addedbutton.restcn()) == int:
            homewindow.words.loc[Addedbutton.restcn(),"addday"] = time.time()
        
        #デバッグ用
        if type(homewindow.restcn[0]) == str:
            print("エラー :restcn[0]にstrが入ってる")
        #デバッグ用
        
        self.text = homewindow.words.loc[Addedbutton.restcn(),"front"]
        print("カード表,init,表単語:",self.ids.frontword.text)
        print(self.text)
        
        cardback.text = homewindow.words.loc[Addedbutton.restcn(),"back"]
        #print("cardfront_init",cardback.text,cardfront.text)
        #if cardback.cn+1 < homewindow.allcount:  
        
        self.front_color = (240,240,240,1)
        self.ids.actionbar.title = homewindow.words.loc[Addedbutton.restcn(),"deck"]
        self.ids.frontword.text = homewindow.words.loc[Addedbutton.restcn(),"front"]
        #print("homewindow.restcn[0][0]",Addedbutton.restcn())
        #print("表テキスト",homewindow.words.loc[Addedbutton.restcn(),"front"])
        #print("cardfront","on_pre_enter","end")
    def viewbackbutton(self):
        #sm = ScreenManager(transition = NoTransition())
        #sm.add_widget(cardback(name='back')) 
        print("cardfront/viewbackbutton : ",Addedbutton.restcn())
        #これが0になっている
        homewindow.words.loc[Addedbutton.restcn(),"leaning_count"] += 1
        self.manager.current = 'back'
        print("cardfront/viewbackbutton : end")

#cardfront.text = "aaa"

class cardback(Screen):
    print("ここにコード書いていいの？")
    text = StringProperty()
    frontword = StringProperty()
    nextback = StringProperty()
    deckname = StringProperty()
    back_color = ListProperty([])
    print("")
    cn = 0
    print("cardback/多分コンストラクタ")
    def __init__(self,**kwargs):
        super(cardback, self).__init__(**kwargs)
        print("cardback","init")

    def on_pre_enter(self):
        
        #
        self.backcolor = (240,240,240,1)
        self.ids.back_actionbar.title = homewindow.words.loc[Addedbutton.restcn(),"deck"]
        #cardfront.text = homewindow.words.loc[homewindow.restcn[0],"front"]
        self.ids.backword.text = homewindow.words.loc[Addedbutton.restcn(),"back"]
        print("カード裏,init,裏単語:",self.ids.backword.text)
        self.parent.deckname = homewindow.words.loc[Addedbutton.restcn(),"front"]
        print("cardback_on_pre_enter : end")
        


    def reset(self):
        homewindow.restcn = [0]
        #self.parent.remove_widget(cardback(name='back'))
        #self.parent.add_widget(cardback(name='back'))

    def ansbutton1(self):
        if homewindow.restcn[0][:-1] == "waypoint":
            waypoint.waypoint_numb = int(homewindow.restcn[0][-1])
            waypoint.next_groupcards = int(len(homewindow.restcn[2]))
        
        my_module.change_perameter_mis(homewindow.words,Addedbutton.restcn())
        
        #残りカードNoリストの先頭を削除
        homewindow.restcn = my_module.mistakecard_relearning(homewindow.restcn)
        nextscreen = my_module.card_check_changescreen(homewindow.restcn)
        self.manager.current =nextscreen
        
    
    
    def ansbutton2(self):
        
        if homewindow.restcn[1][:-1] == "waypoint":
            waypoint.waypoint_numb = int(homewindow.restcn[1][-1])
            waypoint.next_groupcards = int(len(homewindow.restcn[2]))
        
        my_module.change_perameter_dif(homewindow.words,Addedbutton.restcn())
        
        nextscreen = my_module.card_check_changescreen(homewindow.restcn)
        self.manager.current =nextscreen

    def ansbutton3(self):
        if homewindow.restcn[0][:-1] == "waypoint":
            waypoint.waypoint_numb = int(homewindow.restcn[0][-1])
            waypoint.next_groupcards = int(len(homewindow.restcn[2]))
        
        my_module.change_perameter_cor(homewindow.words,Addedbutton.restcn())
        
        nextscreen = my_module.card_check_changescreen(homewindow.restcn)
        self.manager.current =nextscreen

class beforedeck(Screen):
    text = StringProperty()
    def __init__(self,**kwargs):
        super(beforedeck, self).__init__(**kwargs)
        
        #print("カード表,init,カードNo:",homewindow.restcn[0])
        
        
    #initにより初期処理が動くから、ここで追加する
    def on_pre_enter(self):
        self.ids.bef_actionbar.text = homewindow.nowdeckname
        
        self.ids.beforedeck_text1.text = "グループ1"
        self.ids.beforedeck_text2.text = "グループ１の学習予定カード :" + str(len(homewindow.restcn[0])) + "枚"
        print("beforedeck/on_pre_enter : homewindow.restcn :" , homewindow.restcn)
        deck_cards = my_module.count_allcn(homewindow.restcn)
        self.ids.beforedeck_text3.text = "プレイ予定のカード総数 :" + str(deck_cards) +"枚"
        
        #デッキのlastplay更新
        
        
        
    def gohome_button(self):
        self.manager.current = "end"
        
        
    def gofront_button(self):
        print("beforedeck","godront_button","start")
        self.manager.current = 'front'
        
        #デッキのlastplayを更新
        print("homewindow.info_df","\n",homewindow.info_df)
        homewindow.info_df = my_module.lastplay_updating(homewindow.info_df,homewindow.nowdeckname)
        print("homewindow.info_df","updated","\n",homewindow.info_df)
        print("beforedeck","godront_button","end")
    def reset(self):
        homewindow.restcn = [0]

#グループ終了時の中間地点
class waypoint(Screen):
    text = StringProperty()
    waypoint_numb = StringProperty()
    next_groupcards = StringProperty()
    
    def __init__(self,**kwargs):
        super(waypoint, self).__init__(**kwargs)
        print("waypoint_card","__init__")
        
    def on_pre_enter(self):
        self.ids.way_actionbar.text = "デッキ名"
        self.ids.waypoint_name.text = "グループ" + str(waypoint.waypoint_numb) + "の学習が終わりました。"
        self.ids.waypoint_text.text = "次グループのカード :" +str(waypoint.next_groupcards) +"枚"
        
    def gohome_button(self):
        self.manager.current = "end"
        print("waypoint","gohome","info_df","updating","\n",homewindow.info_df)
        homewindow.info_df = my_module.write_to_info(homewindow.words,homewindow.info_df,homewindow.nowdeckname)
        print("waypoint","gohome","info_df","updated","\n",homewindow.info_df)
        homewindow.words.to_csv(homewindow.nowdeckpath , encoding="cp932",index=False)
        homewindow.info_df.to_csv("info.csv", encoding="cp932",index=False)
        
    def continue_button(self):
        self.manager.current = 'front'
        
    def reset(self):
        homewindow.restcn = [0]
        
#テキストに入れてる文が長すぎると落ちる
class endcard(Screen): 
    
    text = StringProperty()
    def __init__(self,**kwargs):
        super(endcard, self).__init__(**kwargs)
        print("end__init__")

    def on_pre_enter(self):
        
        self.ids.end_actionbar.text = "デッキ名"
        
        
    def button_gohome(self):
        homewindow.restcn = []
        #print("ホームへ戻る")
        self.manager.current = 'home'
        #homewindow.restcn = [0]
        deckinfo = pd.read_csv("info.csv",encoding = "cp932")
        print("endcard","gohome","homewindow.info_df","updating",homewindow.info_df)
        homewindow.info_df = my_module.write_to_info(homewindow.words,homewindow.info_df,homewindow.nowdeckname)
        print("endcard","gohome","homewindow.info_df","updated",homewindow.info_df)
        homewindow.words.to_csv(homewindow.nowdeckpath , encoding="cp932",index=False)
        homewindow.info_df.to_csv("info.csv", encoding="cp932",index=False)
        print("エンドカード","restcn :",homewindow.restcn)
        
        
        
        homewindow.todayplays = my_module.sum_todaylearning(homewindow.info_df)
        
        
        
        
        
    def reset(self):
        homewindow.restcn = [0]




class Learning_test1App(App):
    def __init__(self, **kwargs):
        super(Learning_test1App,self).__init__(**kwargs)
        self.title = 'english'

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager(transition = NoTransition())
        print("1aaaa")
        self.sm.add_widget(homewindow(name='home')) 
        print("2aaaa")
        self.sm.add_widget(cardfront(name='front')) 
        print("1aaaa")
        self.sm.add_widget(cardback(name='back')) 
        print("1aaaa")
        self.sm.add_widget(waypoint(name='waypoint')) 
        print("1aaaa")
        self.sm.add_widget(endcard(name='end')) 
        print("1aaaa")
        self.sm.add_widget(beforedeck(name='beforedeck')) 
        print("1aaaa")
        
        #self.sm.current = 'front'
        
        
        
        
        

        return self.sm

Learning_test1App().run()
