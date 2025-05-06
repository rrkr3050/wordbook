from ast import Pass
from turtle import back
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
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

texttest = "aaaa"

group_size = 5
#１グループ5単語として作成する

#ホーム画面追加したい
files = os.listdir("./")
if "decks" in files and len(files) != 0:
    decks = os.listdir("./decks")
    
    print("deckリスト :",decks)
    #decksに何も入ってない
    deck = decks[0]
    #[0]がout of range??
    deck[:-4]
    deckname = deck[:-4]
elif "decks" not in files:
    os.mkdir("./decks")
elif len(files) != 0:
    print("デッキないで")



print(decks)


words1 = pd.read_csv('decks/diction1.csv',encoding = "cp932")
words2 = pd.read_csv('decks/diction2.csv',encoding = "cp932")


words = words1
allcount = len(words)
print("allcount",allcount)

resource_add_path('kivy/fonts')
LabelBase.register(DEFAULT_FONT, 'Koruri-Regular.ttf')
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
        
        
        

    def golc1(self):

        #print("godeck1,cardback.cn:",cardback.cn)
        
        homewindow.words = words1
        homewindow.allcount = len(words1)
        #print("godeck,cardback.cn:",cardback.cn)
        homewindow.deckname = homewindow.words.loc[homewindow.restcn[0],"deck"]
        cardfront.deckname = cardback.deckname = homewindow.deckname
        #self.parent.sm = ScreenManager(transition = NoTransition())
        
        #self.parent.remove_widget(cardfront(name='front'))
        self.parent.current = 'front'

    #追加デッキのボタンに搭載する関数は同じ物を使う
    #関数は変えずに、外部からその関数に用いる変数を変更することで別のデッキに対応する

    def decksreload(self):
        files = os.listdir("./decks")
        decks_numb = len(files)
        for i in range(decks_numb):
            #print(i)
            filename = files[i]
            homewindow.filename = filename
            homewindow.newdeckpath = "./decks/" + filename
            homewindow.newdeck = pd.read_csv(homewindow.newdeckpath,encoding = "cp932")
            #homewindow.newdeckname = homewindow.newdeck.loc[0,"deck"]
            
            
            

            Newbutton = Addedbutton()
            Box_inscroll = self.ids.bola1
            Box_inscroll.add_widget(Newbutton)



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
        self.offset_cn_raw = homewindow.newdeck.index.values.tolist()
        self.gr_pri_list = []
        
        #offsetをグループごとの二重リストにする
        self.offset_cn = []
        
        #二重配列のoffsetを生成
        current_cn = 0
        temp =[]
        while 1:
            #current_cnがcn_rawの最大要素数に達したら終了
            temp.append(self.offset_cn_raw[current_cn])
            if len(temp) == 5:
                print("Addedbutton_init","二重配列offset_while","tempをoffsetに追加 temp :",temp)
                self.offset_cn.append(temp)
                temp = []
            #5で割り切れないあまりのカードは少数グループとして追加し、break
            if current_cn == self.offset_cn_raw[-1]:
                self.offset_cn.append(temp)
                break
            current_cn += 1
        
        print("Addedbutton_init","二重配列offeset :",self.offset_cn)
        
        print("Addedbutton_init","_ラスト","デッキセット時のオフセットcn :",self.offset_cn)
        print("Addedbutton_init","_ラスト","デッキセット時のrestcn :",homewindow.restcn)
        
        print("Addedbutton_init","_ラスト",self.text,"デッキセット")
        print("Addedbutton_init","_ラスト","added_init,self.offset_cn",self.offset_cn)

    def go_deck(self):  
        print("Addedbutton_go_deck","スタート")
        #if len(homewindow.restcn[]) == 0:
        
        #一定時間経過しているカードのpriority増加
        for i in range(len(homewindow.words)):
            if time.time() - homewindow.words.loc[i,"addday"] > 10:
                homewindow.words.loc[i,"priority"] += 1
                #最終学習日から一日以上経過している単語はpriorityをインクリメント
        #一定時間経過しているカードのpriority増加


        #rest_cnの生成
        print("Addedbutton_go_deck","rest_cnの生成")
        #priority>97の単語をrestcnに追加
        #基本pri順に追加し、102以上は同じものと扱う。
        #必要な情報:"いくつグループをプレイするか",""
        #1グループ目のgr_priが94を下回ったらしたら2グループ目もrestcnに追加する。
        print()
        gr_pri_threshold = 94
        card_pri_threshold = 95
        
        homewindow.restcn = my_module.finalize_restcn_old(self.offset_cn,gr_pri_threshold,card_pri_threshold,homewindow.words)
        #rest_cnの生成ed
        
        
        homewindow.nowdeckpath = self.deckpath
        #現在プレイしているデッキのpathをここに保存
        print(homewindow.nowdeckpath)
        print("プレイデッキ名:",self.text)
        print("プレイデッキ:",self.deck)
        print("selfdeckのindex",self.deck.index.values.tolist())
        print("cnリストオフセット:",self.offset_cn)
        print("現在のcnリスト:",homewindow.restcn)
        print("初プレイチェック:",self.check_first)
        print("前回のデッキ名",Addedbutton.previous_deckname)
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
        self.parent.parent.parent.parent.manager.current = 'front'


class cardfront(Screen):
    #widgetクラスを継承してる。widgetクラスはkivyに標準搭載してるから使える。
    text = StringProperty()
    deckname = StringProperty()
    print("カードフロント")


    def __init__(self,**kwargs):
        super(cardfront, self).__init__(**kwargs)
        
        #print("カード表,init,カードNo:",homewindow.restcn[0])
        
        
    #initにより初期処理が動くから、ここで追加する
    def on_pre_enter(self):
        print("cardfront","on_pre_enter","restcn :",homewindow.restcn)
        #最終更新日を更新
        homewindow.words.loc[homewindow.restcn[0],"addday"] = time.time()
        
        #デバッグ用
        if type(homewindow.restcn[0]) == str:
            print("エラー :restcn[0]にstrが入ってる")
        #デバッグ用
        
        self.text = homewindow.words.loc[homewindow.restcn[0],"front"]
        print("カード表,init,表単語:",self.ids.frontword.text)
        print(self.text)
        
        cardback.text = homewindow.words.loc[homewindow.restcn[0],"back"]
        #print("cardfront_init",cardback.text,cardfront.text)
        #if cardback.cn+1 < homewindow.allcount:  
        self.ids.actionbar.title = homewindow.filename
        self.ids.frontword.text = homewindow.words.loc[homewindow.restcn[0],"front"]
        print("homewindow.restcn[0]",homewindow.restcn[0])
        print("表テキスト",homewindow.words.loc[homewindow.restcn[0],"front"])

    def viewbackbutton(self):
        #sm = ScreenManager(transition = NoTransition())
        #sm.add_widget(cardback(name='back')) 
        homewindow.words.loc[homewindow.restcn[0],"leaning_count"] += 1
        self.manager.current = 'back'

#cardfront.text = "aaa"

class cardback(Screen):
    text = StringProperty()
    frontword = StringProperty()
    nextback = StringProperty()
    deckname = StringProperty()
    
    print("")
    cn = 0
    def __init__(self,**kwargs):
        super(cardback, self).__init__(**kwargs)
        print("cardback","init")

    def on_pre_enter(self):
        print("カード裏,init,裏単語:",self.ids.backword.text)
        
        self.ids.back_actionbar.title = homewindow.words.loc[homewindow.restcn[0],"deck"]
        #cardfront.text = homewindow.words.loc[homewindow.restcn[0],"front"]
        self.ids.backword.text = homewindow.words.loc[homewindow.restcn[0],"back"]
        self.parent.deckname = homewindow.words.loc[homewindow.restcn[0],"front"]
        


    def reset(self):
        homewindow.restcn = [0]
        #self.parent.remove_widget(cardback(name='back'))
        #self.parent.add_widget(cardback(name='back'))

    def ansbutton1(self):
        #最終更新日を更新
        homewindow.words.loc[homewindow.restcn[0],"addday"] = time.time()
        
        #front = cardfront()
        #self.sm = ScreenManager(transition = NoTransition())
        #self.sm.add_widget(cardfront(name='front')) 
        print(homewindow.newdeckpath)
        #デッキのpath
        
        
        #restcn[0]を"waypoint" or "end"の前に追加
        print("cardback","ansbutton1","ミスカード移動前","restcn :",homewindow.restcn)
        for i in range(len(homewindow.restcn)):
            if type(i) == str:
                homewindow.restcn.insert(i,homewindow.restcn[0])
                break
        print("cardback","ansbutton1","ミスカード移動後","restcn :",homewindow.restcn)
        #restcn[0]を"waypoint" or "end"の前に追加
        
        homewindow.words.loc[homewindow.restcn[0],"mistakes"] += 1
        homewindow.words.loc[homewindow.restcn[0],"priority"] += 2
        
        #間違えたらcurrentを0に設定
        homewindow.words.loc[homewindow.restcn[0],"current"] = 0
        #wordsデータフレームのmistakesカラムに+1
        
        #残りカードNoリストの先頭を削除
        
        nextscreen = my_module.card_check_changescreen(homewindow.restcn)
        self.manager.current =nextscreen
        
        print("")
        #del homewindow.restcn[0]
        
        """ if type(current_cn) == int:
            print("ミス,カードナンバー",homewindow.restcn)
            self.manager.current = 'front'
            
            print("わからない")
        elif homewindow.restcn[0][:-1] == "waypoint"
            group = homewindow.restcn[0][-1]
            self.manager.current = 'waypoint'
            #homewindow.restcn = [0]
            #self.manager.current = 'front'
        elif homewindow.restcn[0] == "end":
            self.manager.current = 'end' """
 
        
        
            
    
    def ansbutton2(self):
        #最終更新日を更新
        homewindow.words.loc[homewindow.restcn[0],"addday"] = time.time()
        
        homewindow.words.loc[homewindow.restcn[0],"close"] += 1
        
        del homewindow.restcn[0]
        if len(homewindow.restcn) != 0:
            self.manager.current = 'front'
            print("難しい,カードナンバー",homewindow.restcn)
            
        else:
            self.manager.current = 'end'
            #homewindow.restcn = [0]

    def ansbutton3(self):
        #最終更新日を更新
        homewindow.words.loc[homewindow.restcn[0],"addday"] = time.time()
        
        homewindow.words.loc[homewindow.restcn[0],"corrects"] += 1
        
        #priorityの現象値をcurennt値によって変動させる
        nowcurrent = homewindow.words.loc[homewindow.restcn[0],"current"]
        homewindow.words.loc[homewindow.restcn[0],"priority"] -= (1 + nowcurrent)
        
        #正解したらcurrentに1を追加(連続正解数)
        homewindow.words.loc[homewindow.restcn[0],"current"] += 1
        
        del homewindow.restcn[0]
        if len(homewindow.restcn) != 0:
            self.manager.current = 'front'
            
            
        else:
            self.manager.current = 'end'
            #homewindow.restcn = [0]

#グループ終了時の中間地点
class waypoint(Screen):
    text = StringProperty()
    def __init__(self,**kwargs):
        super(waypoint, self).__init__(**kwargs)
        print("waypoint_card","__init__")
        
    def gohome_button(self):
        self.manager.current = "end"
    def continue_button(self):
        self.manager.current = 'front'
        
#テキストに入れてる文が長すぎると落ちる
class endcard(Screen): 
    
    text = StringProperty()
    def __init__(self,**kwargs):
        super(endcard, self).__init__(**kwargs)
        print("end__init__")

    def button_gohome(self):
        homewindow.restcn = []
        #print("ホームへ戻る")
        self.manager.current = 'home'
        #homewindow.restcn = [0]
        homewindow.words.to_csv(homewindow.nowdeckpath , encoding="cp932",index=False)
        print("エンドカード","restcn :",homewindow.restcn)




class Learning_test1App(App):
    def __init__(self, **kwargs):
        super(Learning_test1App,self).__init__(**kwargs)
        self.title = 'english'

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager(transition = NoTransition())
        self.sm.add_widget(homewindow(name='home')) 
        self.sm.add_widget(cardfront(name='front')) 
        self.sm.add_widget(cardback(name='back')) 
        self.sm.add_widget(waypoint(name='waypoint')) 
        self.sm.add_widget(endcard(name='end')) 
        
        #self.sm.current = 'front'
        
        
        
        
        

        return self.sm

Learning_test1App().run()
