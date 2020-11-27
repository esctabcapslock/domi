#!/usr/bin/env python
# coding: utf-8

# In[460]:

import copy
import requests
import datetime, time
from auth import *

placeSelect={
    "소학":1,
    "호실":4,
    "휴게":2,
    "본관":3,
    "정독":8
      }

timeSelect={
    "공란":17,
    "오후":18,
    "1자":20,
    "2자":22,
    "노트":25,
    "연장":27
}

reasonSelect={
    "과제":1,
    "학습":2,
    "요양":3,
    "취미":4,
    "SA":5,
    "기타":6
}




def getDate(x):
    a=datetime.datetime.now()
    d=(datetime.datetime(a.year,a.month,a.day,0,0).timetuple())
    return int(time.mktime(d))+86400*int(x)

def stdu_num(x):
    return x[0],x[1],str(int(x[2:]))




file=open("pw.txt",'r+')
was_pw=복호화(file.read()).split()
file.close()
account=[]
if len(was_pw)==3: account=was_pw
else:
    print("다음 주어진 항목을 입력하십시오. 처음 1회만 입력하면 됩니다")
    while 1:
        account=input("id, 비번, 학번입력\n").split()
        if len(account)==3: break
        else: print("입력 형식이 잘못되었습니다. 다시 입력하십시오")
    file=open("pw.txt",'w')
    file.write(암호화(' '.join(account)))
    file.close()
stdunt=stdu_num(account[2])

URL='https://sasadomi.hs.kr/Lib/user.action.php'
data={'mode':'login','id':account[0],'pw':account[1]}
res=requests.post(URL,data)
x=res.headers['Set-Cookie'].split(';')[0].split('=')
cookies={x[0]:x[1]}

def apply(hour,place,reason,detail_reason):
    print('apply');
    hour=timeSelect[hour]
    place=placeSelect[place]
    reason=reasonSelect[reason]
    date=getDate(1)

    URL='https://sasadomi.hs.kr/Lib/study_apply.action.php'
    data={
        'mode':'apply',
        'grade':stdunt[0],
        'class':stdunt[1],
        'class_number':stdunt[2],
        'date':date,
        'time':hour,
        'place':place,
        'reason':reason,
        'detail_reason':detail_reason
    }
    res=requests.post(URL,data=data,cookies=cookies)
    #print("요청이 처리되었습니다")

    messagebox.showinfo(title="안내", message="요청이 처리되었습니다.")

    st=str(res.content)
    ct=st.find("content")
    st[ct+9:-2]
    #print(a,"성공" if a=='null' else "오류")


import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.geometry('490x250+0+0')


def pre_apply(a, b):
    print(a,b)
    if a=='1,2자':
        pre_apply('1자',b)
        pre_apply('2자',b)
    elif b=='본관(SA)': apply(a,'본관','SA','')
    elif b=='본관(동아리)': apply(a,'본관','기타','동아리')
    elif b=='소학': apply(a,b,'학습','')
    else: apply(a, b, '요양', '')


time_ = ['1자', '2자', '1,2자', '연장']
place_ = ['본관(SA)', '본관(동아리)', '소학', '호실']
btn_l = []

def getcallback(a,b):
    return lambda:pre_apply(a,b)
for i in range(len(time_)):
    for j in range(len(place_)):
        btn_l.append(tk.Button(root, text=time_[i] + ' ' + place_[j], command=getcallback(time_[copy.deepcopy(i)],place_[copy.deepcopy(j)])))
        btn_l[-1].place(x=i * 120 + 10, y=j * 25+10)


def change_pw():
    account=[entry_id.get(),entry_pw.get(),entry_stn.get()]
    file = open("pw.txt", 'w')
    file.write(암호화(' '.join(account)))
    file.close()


label_id = tk.Label(root,text='id')
entry_id = tk.Entry(root,textvariable='id')
entry_pw = tk.Entry(root,textvariabl='pw',show='*')
label_pw = tk.Label(root,text='pw')
entry_stn = tk.Entry(root,textvariable='학번')
label_stn = tk.Label(root,text='학번')
entry_enter = tk.Button(root,text='개인정보 갱신',command=change_pw)

entry_id.place(x=10,y=160)
entry_pw.place(x=160,y=160)
entry_stn.place(x=310,y=160)
label_id.place(x=10,y=140)
label_pw.place(x=160,y=140)
label_stn.place(x=310,y=140)
entry_enter.place(x=200,y=180)

entry_id.insert(0,account[0])
entry_pw.insert(0,account[1])
entry_stn.insert(0,account[2])

b_end = tk.Button(root, text='종료', command=root.destroy)
b_end.place(x=220, y=220)
root.mainloop()

