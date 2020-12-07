from fastapi import FastAPI
import uvicorn
import datetime
import pandas as pd
import time
from pydantic import BaseModel
from typing import Optional


class Data(BaseModel):
    division: str
    team: str
    name: str
    today: str
    date0: str
    tamselect0: str
    destnselect0: str
    date1: str
    tamselect1: str
    destnselect1: str
    date2: str
    tamselect2: str
    destnselect2: str
    date3: str
    tamselect3: str
    destnselect3: str
    date4: str
    tamselect4: str
    destnselect4: str
    date5: str
    tamselect5: str
    destnselect5: str
    date6: str
    tamselect6: str
    destnselect6: str
    date7: str
    tamselect7: str
    destnselect7: str
    date8: str
    tamselect8: str
    destnselect8: str
    date9: str
    tamselect9: str
    destnselect9: str


app = FastAPI()


def return_date_of_week(d):

    y = d.year

    w = d.isocalendar()[1] -2 # as it starts with 0 and you want week to start from sunday

    if w < 0:
        w = 0

    startdate = time.asctime(time.strptime('%d %d 0' % (y, w), '%Y %W %w')) 
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
    dates = [startdate.strftime('%Y-%m-%d')] 
    for i in range(1, 7): 
        day = startdate + datetime.timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d')) 

    dates = dates[1:6]

    return dates


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
                data[i].extend([["출근", "해당없음"]])    
        
        i+=1

    return data


@app.post("/update_data/")
async def update_data(data: Data):
    today = datetime.datetime.strptime(data.today, '%Y-%m-%d')
    dates = return_date_of_week(today)
    attends = [data.tamselect0, data.tamselect1, data.tamselect2, data.tamselect3, data.tamselect4,
               data.tamselect5, data.tamselect6, data.tamselect7, data.tamselect8, data.tamselect9 ]
    destns = [data.destnselect0, data.destnselect1, data.destnselect2, data.destnselect3, data.destnselect4,
              data.destnselect5, data.destnselect6, data.destnselect7, data.destnselect8, data.destnselect9]

    d7 = (today + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    dplusseven = datetime.datetime.strptime(d7, '%Y-%m-%d')

    nextweek = return_date_of_week(dplusseven)
    dates = dates + nextweek

    df = pd.read_csv('test.csv')

    for i in range(len(dates)):
        to_append = [data.division, data.team, data.name, today.year, today.isocalendar()[1], dates[i], attends[i], destns[i]]

        df = df.drop(df[(df.division == data.division) & (df.team == data.team) & (df.name == data.name) & (df.date == dates[i])].index)
        df = df.reset_index(drop=True)

        df_length = len(df)
        df.loc[df_length] = to_append

    df.to_csv('test.csv', index=False)

    return data