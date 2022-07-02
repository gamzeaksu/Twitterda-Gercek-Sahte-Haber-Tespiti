# -*- coding: utf-8 -*-

from nltk.stem.snowball import SnowballStemmer
from tensorflow.keras.preprocessing.text import Tokenizer

from keras.preprocessing.sequence import pad_sequences
import nltk
nltk.download('stopwords')
import keras
import string
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np


model = keras.models.load_model("dropout_w2v.h5")
stopwords = nltk.corpus.stopwords.words('english')

def tahmin(girilen):
    #noktalama
    son = ""
    for i in girilen:
        if i not in string.punctuation:
            son+=i
    son = son.lower()
    son = son.split()
    son1=list()
    son2 = list()
    son3 = list()
    tweet = list()
    for i in son:
        if i not in stopwords:
            son1.append(i)
    print("son1:",son1)
    for i in son1:
        if not i.startswith("http"):
            son2.append(i)
    print("son2:",son2)
    snow_stemmer = SnowballStemmer(language='english')
    for i in son2:
        son3.append(snow_stemmer.stem(i))
    print("son3:",son3)
    tweet.append(" ".join(son3)) 
    #tweet = str(tweet)
    #tweet = son3
    print("tweet:",tweet)
    print("type:",type(tweet))
    df=pd.read_csv("stemmed.csv")
 
    df.loc[len(df)] = str(tweet)

    X=[d.split() for d in df['Stemmed']] #hepsinin toplamı
    
    #tokenizer 
    tokenizer=Tokenizer()
    tokenizer.fit_on_texts(X)
    #print("tweet1:",X)
    print(type(tweet))
    print(tweet[0].split())
    X=tokenizer.texts_to_sequences(tweet)
    print("X:",X)
    #print("bok:",X) [[1,2],[3,4]]
    X=pad_sequences(X, padding="post",maxlen=22)
    
    X=X.tolist() #hepsinin toplamı
    
    print(X[0])

    a = len(X)-1
    
    tweet = list()
    tweet.append(X[a])
    print(tweet)
    y_pred = (model.predict(tweet))# >= 0.5).astype("int")
    print("pred:",round(y_pred[0][0],4))
    y_pred = round(y_pred[0][0],4)*100
    sonuc = ""
    if y_pred <= 50:
        sonuc = "GERÇEK"
    else:
        sonuc = "SAHTE"
    pred_prob = (model.predict_proba(tweet))
    messagebox.showinfo("Bilgi",f"Girilen tweet {sonuc} olarak belirlenmiştir.")
                        

###ARAYÜZ##########
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
window = Tk()
window.geometry("640x500")
window["background"]="#dcf4f7"
load = Image.open("twitter.jpg")

resize_image = load.resize((200, 150))
 
img = ImageTk.PhotoImage(resize_image)
 
# create label and add resize image
label1 = Label(window,image=img)
label1.image = img
#label1.grid(row=0,column=0,padx={10,10})
 

greeting = Label(window,text="Twitter Platformunda Sahte Haber Tespiti",
                 padx=10,
                 pady=20,
                 font=("Arial", 15),
                 #bg="#f7e4e4"
                 bg="#dcf4f7")

def Take_input():
    INPUT = entry.get("1.0", END)
    if len(INPUT) == 1:
        messagebox.showinfo("Bilgi","Lütfen bir tweet giriniz.") 
    elif len(INPUT)>280:
        messagebox.showinfo("Bilgi","Girdiğiniz tweetin boyutu 280 karakteri aşmamalıdır.") 
        entry.delete("1.0", END)
    else:   
        tahmin(INPUT)

def Del_input():
    entry.delete("1.0", END)

entry = Text(window,width = 50,
             height=5,
             padx=15,
             pady=15,
             font =12)


        
entry.insert(INSERT,"Tweet giriniz...")
b1 = Button(window, text = "Tahmin", 
            width=15,height=2,
            bg="#c4f2e1",
            font=("Arial", 9),
            command = lambda:Take_input())
  
# Create an Exit button.
b2 = Button(window, text = "Sayfayı Temizle", 
            width=15,height=2,
            bg="#c4f2e1",
            font=("Arial", 9),
            command = lambda:Del_input())

b3 = Button(window,relief="flat", text = "", width=1,height=1,bg="#dcf4f7")



b3.pack()
label1.pack()
greeting.pack()
entry.pack()
b1.place(x=140,y=430)
b2.place(x=330,y=430)


#messagebox.showinfo("Information","Information for user") 
window.mainloop()
