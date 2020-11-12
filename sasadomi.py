#!/usr/bin/env python
# coding: utf-8

# In[460]:


import requests
import json
import datetime, time


# In[461]:


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


# In[9]:


def getDate(x):
    a=datetime.datetime.now()
    d=(datetime.datetime(a.year,a.month,a.day,0,0).timetuple())
    return int(time.mktime(d))+86400*int(x)

def stdu_num(x):
    return x[0],x[1],str(int(x[2:]))


# In[64]:


file=open("pw.txt",'r')
was_pw=file.read().split()
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
    file.write(' '.join(account))
    file.close()
stdunt=stdu_num(account[2])


# In[520]:


URL='https://sasadomi.hs.kr/Lib/user.action.php'
data={'mode':'login','id':account[0],'pw':account[1]}
res=requests.post(URL,data)
x=res.headers['Set-Cookie'].split(';')[0].split('=')
cookies={x[0]:x[1]}


# In[521]:


while(1):
    """
    hour=17
    date=getDate(0)
    place=reason=1"""
    detail_reason=''
    print("\n<사사도미 입력기>\n취소는 불가능합니다",'\n시간: ',*timeSelect,'\n장소: ',*placeSelect,'\n이유: ',*reasonSelect)
    print("\n다음에 해당되는 값을 공백으로 구분해서 입력하십시오")
    a=input("시간, 장소, 사유, 날짜\n[입력예시]: 오늘 1자 소학에서 학습을 하고 싶다면 =>> 1자 소학 학습 0\n").split()#2 3 2 1자 소학 취미 10
    #stdunt=a[:3]
    hour=timeSelect[a[3-3]]
    place=placeSelect[a[4-3]]
    reason=reasonSelect[a[5-3]]
    date=getDate(int(a[6-3]))

    URL='https://sasadomi.hs.kr/Lib/study_apply.action.php'
    #mode=apply&grade=2&class=3&class_number=2&date=1605020400&time=17&place=1&reason=1&detail_reason=
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
    print("요청이 처리되었습니다")
    st=str(res.content)
    ct=st.find("content")
    st[ct+9:-2]
    #print(a,"성공" if a=='null' else "오류")

