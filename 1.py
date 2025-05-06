from ast import Pass
from turtle import back
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
#from cgi import test
from operator import index
from this import d
from types import ClassMethodDescriptorType
import pandas as pd
import numpy as np
import csv
import datetime
import time

def test_cards(df,cardno):
    print(df.loc[cardno,"front"],"\nわからない:a  難しい:b  わかった:c")
    ans = input("回答:")
    if ans == "a":
        df.loc[cardno,"mistakes"] += 1
        df.loc[cardno,"priority"] += 2
        df.loc[cardno,"current"] = 2
        print("誤答数を１足しました")
    elif ans == "b":
        df.loc[cardno,"close"] += 1
        df.loc[cardno,"current"] = 1
        print("closeを1足しました")
    elif ans == "c":
        print("正答数を1足しました")
        df.loc[cardno,"corrects"] += 1
        df.loc[cardno,"priority"] -= 1
        df.loc[cardno,"current"] = 0
    df.loc[cardno,"leaning_count"] += 1
    return df

def cardno_alltest(df,filename,amount):

    for i in range(amount):
        df = test_cards(df,i)
    df.to_csv(filename,index = False,encoding = 'cp932')

words = pd.read_csv('diction.csv',encoding = "cp932")
allcount = len(words)
print("allcount",allcount)

#kivy_2_trans.pyより
resource_add_path('kivy/fonts')
LabelBase.register(DEFAULT_FONT, 'Koruri-Regular.ttf')
#日本語フォント導入


cardno = 1
#frontword = words.loc[cardno,"front"]
#backword = words.loc[cardno,"back"]

class cardfront(BoxLayout):
    #widgetクラスを継承してる。widgetクラスはkivyに標準搭載してるから使える。
    text = StringProperty()


    def __init__(self,**kwargs):
        super(cardfront, self).__init__(**kwargs)

        self.text = words.loc[cardback.cn,"front"]
        cardback.text = words.loc[cardback.cn,"back"]
        print("cardfront_init",cardback.text,cardfront.text)


            
    def viewbackbutton(self):
        self.clear_widgets()
        cb = cardback()
        self.add_widget(cb)

#cardfront.text = "aaa"

class cardback(BoxLayout):
    text = StringProperty()
    nextback = StringProperty()
    cn = 0
    print("cardbackのdef上")
    def __init__(self,**kwargs):
        print("cardback_init",self.cn)
        super(cardback, self).__init__(**kwargs)
        cardback.cn += 1
        
    
    def ansbutton1(self):
        #print(self.text)
        #print("self.cn",self.cn)
        #print("cardback.cn",cardback.cn)
        if cardback.cn < allcount:
            self.clear_widgets()
            cf = cardfront()
            self.add_widget(cf)
            print("わからない")
        else:
            print("owa")
            self.clear_widgets()
            ec = endcard()
            self.add_widget(ec)
    
    def ansbutton2(self):
        
        if cardback.cn < allcount:
            self.clear_widgets()
            cf = cardfront()
            self.add_widget(cf)
            print("難しい")
        else:
            print("owa")
            self.clear_widgets()
            ec = endcard()
            self.add_widget(ec)

    def ansbutton3(self):
        
        if cardback.cn < allcount:
            self.clear_widgets()
            cf = cardfront()
            self.add_widget(cf)
            print("分かった")
        else:
            print("owa")
            self.clear_widgets()
            ec = endcard()
            self.add_widget(ec)

#テキストに入れてる文が長すぎると落ちる
class endcard(BoxLayout): 
    
    text = StringProperty()
    def __init__(self,**kwargs):
        super(endcard, self).__init__(**kwargs)
        print("end__init__")

    def button_gohome(self):
        print("ホームへ戻る")

    

class Kivy2transApp(App):
    def __init__(self, **kwargs):
        super(Kivy2transApp,self).__init__(**kwargs)
        self.title = 'english'

#kivy_2_trans.py



Kivy2transApp().run()
