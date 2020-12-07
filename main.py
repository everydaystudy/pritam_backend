from fastapi import FastAPI
import uvicorn
import datetime
import pandas as pd
import time


app = FastAPI()


def return_date_of_week(d):

    y = d.year

    w = d.isocalendar()[1] - 2 # as it starts with 0 and you want week to start from sunday
    startdate = time.asctime(time.strptime('%d %d 0' % (y, w), '%Y %W %w')) 
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
    dates = [startdate.strftime('%Y-%m-%d')] 
    for i in range(1, 7): 
        day = startdate + datetime.timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d')) 

    dates = dates[1:6]

    return dates

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/weeknumber")
def weeknumber():

    print(datetime.datetime.today().isocalendar()[1])

    # print(datetime.date(2020, 11, 30).isocalendar()[1])

    return {"Hello": "World"}


@app.get("/today_biztrip")
def today_biztrip(division: str, team: str, today: str):

    df = pd.read_csv('test.csv')
    df = df[(df['division'] == division) & (df['team'] == team) & (df['date'] == today) & (df['attendance'] == "출장")]
    df["biztrip"] = df['name'] + " (" + df['destn'] + ")"

    biztrip_lst = df["biztrip"].tolist()

    return biztrip_lst


@app.get("/today_wfh")
def today_wfh(division: str, team: str, today: str):

    df = pd.read_csv('test.csv')
    df = df[(df['division'] == division) & (df['team'] == team) & (df['date'] == today) & (df['attendance'] == "재택")]
    df["wfh"] = df['name']

    wfh_lst = df["wfh"].tolist()

    return wfh_lst
    

@app.get("/wfh_rate")
def wfh_rate(division: str, team: str, today: str):

    d = datetime.datetime.strptime(today, '%Y-%m-%d')

    dates = return_date_of_week(d)

    df = pd.read_csv('members.csv')
    mem_cnt = len(df[(df['division'] == division) & (df['team'] == team)])

    df = pd.read_csv('test.csv')
    rate_lst = []
    for dat in dates:
        rate_lst.append(len(df[(df['division'] == division) & (df['team'] == team) & (df['date'] == dat) & (df['attendance'] == "재택")]) / mem_cnt * 100)

    rate_lst = [round(x, 1) for x in rate_lst]

    return rate_lst


@app.get("/tam_data")
def tam_data(division: str, team: str, today: str):

    d = datetime.datetime.strptime(today, '%Y-%m-%d')

    dates = return_date_of_week(d)

    df = pd.read_csv('members.csv')
    mem = df[(df['division'] == division) & (df['team'] == team)].values.tolist()

    df = pd.read_csv('test.csv')
    df["destn"].fillna("", inplace = True) 

    i = 0
    data = []
    for m in mem:
        data.extend([m])
        for d in dates:
            data[i].extend(df[(df['division'] == m[0]) & (df['team'] == m[1]) & (df['name'] == m[2]) & (df['date'] == d)][['attendance', 'destn']].values.tolist())
            if len(df[(df['division'] == m[0]) & (df['team'] == m[1]) & (df['name'] == m[2]) & (df['date'] == d)][['attendance', 'destn']].values.tolist()) == 0:
                data[i].extend([[]])    
        
        i+=1

    return data
