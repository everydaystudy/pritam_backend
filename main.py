from fastapi import FastAPI
import uvicorn
import datetime
import pandas as pd
import time


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/weeknumber")
def weeknumber():

    print(datetime.datetime.today().isocalendar()[1])

    # print(datetime.date(2020, 11, 30).isocalendar()[1])

    return {"Hello": "World"}


@app.get("/today_biztrip")
def today_biztrip():

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    df = pd.read_csv('test.csv')
    df = df[(df['date'] == today) & (df['attendance'] == "출장")]
    df["biztrip"] = df['name'] + "(" + df['destn'] + ")"

    biztrip_lst = df["biztrip"].tolist()

    return biztrip_lst


@app.get("/today_wfh")
def today_wfh():

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    df = pd.read_csv('test.csv')
    df = df[(df['date'] == today) & (df['attendance'] == "재택")]
    df["wfh"] = df['name']

    wfh_lst = df["wfh"].tolist()

    return wfh_lst
    

@app.get("/wfh_rate/{today}")
def wfh_rate(today: str):

    d = datetime.datetime.strptime(today, '%Y%m%d')
    y = d.year

    w = d.isocalendar()[1] - 2 # as it starts with 0 and you want week to start from sunday
    startdate = time.asctime(time.strptime('%d %d 0' % (y, w), '%Y %W %w')) 
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
    dates = [startdate.strftime('%Y-%m-%d')] 
    for i in range(1, 7): 
        day = startdate + datetime.timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d')) 

    dates = dates[1:6]

    df = pd.read_csv('test.csv')
    for dat in dates:
        print(df[(df['date'] == dat) & (df['attendance'] == "재택")])

    return {"Hello": "World"}