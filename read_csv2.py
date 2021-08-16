#数据清洗，去除只有进没有出，或者只有出没有进的停车记录

import pandas as pd
from nparrayCaculate import getDate
from nparrayCaculate import getSecond
from collections import Counter
from nparrayCaculate import date_compare
from nparrayCaculate import datelist
from nparrayCaculate import datelist2
import matplotlib.pyplot as plt
import datetime
import os

from functools import cmp_to_key
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
savePath=r"E:\pytorch\HikiPark\HKPark_0526\data\save0627"

def remainValue(pdEnter,errorValue2,ExitCsv,lookBack,flag=0):
    state = "event_id" if flag == 0 else "enter_event_id"
    pdError2Enter = pdEnter[pdEnter[state].isin(errorValue2)]
    pdError2Enter.index = range(pdError2Enter.shape[0])
    BeginDateList, EndDateList = getEndDayList(ExitCsv, lookBack=lookBack)
    # print(BeginDateList)
    BeginDateList=BeginDateList if flag==0 else EndDateList
    pdError2Enter.drop(pdError2Enter[pdError2Enter["date_day1"].isin(BeginDateList)].index, inplace=True)
    # print(len(pdError2Enter))

    errorValue2 = list(pdError2Enter[state])
    # print(len(errorValue2))
    pdEnter.drop(pdEnter[pdEnter[state].isin(errorValue2)].index, inplace=True)
    return pdEnter



def getEndDayList(ExitCsv,lookBack):
    # EnterCsv = r"data/data0526/1\10119112210362202000.csv"
    # ExitCsv = r"data/data0526/2\10119112210362202000.csv"
    pdExit = pd.read_csv(ExitCsv)
    pdExit = pdExit[pdExit["enter_event_id"].notnull()]
    # pdEnter = pd.read_csv(EnterCsv)
    beginDay = list(pdExit["date_day"])[0]
    endDay = list(pdExit["date_day"])[-1]
    begin_date = datetime.datetime.strptime(beginDay, r"%Y/%m/%d")
    end_date = datetime.datetime.strptime(endDay, r"%Y/%m/%d")
    end_date += datetime.timedelta(days=1)
    end_date = end_date.strftime(r"%Y/%m/%d")
    endDate1=(begin_date+datetime.timedelta(days=lookBack)).strftime(r"%Y/%m/%d")
    begin_date1=(begin_date+datetime.timedelta(days=-1)).strftime(r"%Y/%m/%d")
    return datelist(beginDay, end_date, look_back=lookBack).split(" "),datelist(begin_date1, endDate1, look_back=lookBack).split(" ")

def getEndDayList2(ExitCsv):
    # EnterCsv = r"data/data0526/1\10119112210362202000.csv"
    # ExitCsv = r"data/data0526/2\10119112210362202000.csv"
    pdExit = pd.read_csv(ExitCsv)
    pdExit = pdExit[pdExit["enter_event_id"].notnull()]
    # pdEnter = pd.read_csv(EnterCsv)
    beginDay = list(pdExit["date_day"])[0]
    endDay = list(pdExit["date_day"])[-1]
    # begin_date = datetime.datetime.strptime(beginDay, r"%Y/%m/%d")
    # end_date = datetime.datetime.strptime(endDay, r"%Y/%m/%d")
    # end_date += datetime.timedelta(days=1)
    # end_date = end_date.strftime(r"%Y/%m/%d")
    # endDate1=(begin_date+datetime.timedelta(days=lookBack)).strftime(r"%Y/%m/%d")
    # begin_date1=(begin_date+datetime.timedelta(days=-1)).strftime(r"%Y/%m/%d")
    return datelist2(beginDay, endDay).split(" ")

def getNostdValue(ExitCsv):
    # EnterCsv=r"data/data0526/1\10119112210362202000.csv"
    csvName=ExitCsv.split("\\")[-1].split(".")[0]+".csv"
    EnterPath=ExitCsv.split("\\")[0].replace("/2","/1")
    EnterCsv=os.path.join(EnterPath,csvName)
    # ExitCsv=r"data/data0526/2\10119112210362202000.csv"

    # EnterCsv=r"H:\@chengfu\ParkData\1\10120030821200902000.csv"
    # ExitCsv=r"H:\@chengfu\ParkData\2\10120030821200902000.csv"

    pdExit=pd.read_csv(ExitCsv)
    pdExit=pdExit[pdExit["enter_event_id"].notnull()]  #去除出场数据中入场事件id为空的记录
    pdEnter=pd.read_csv(EnterCsv)
    ExitEnterEventId=list(pdExit["enter_event_id"])
    EnterEventId=list(pdEnter["event_id"])
    print(len(ExitEnterEventId),len(EnterEventId))

    pdNull=pdExit[pdExit["enter_event_id"].isnull()]
    pdNull.index=range(pdNull.shape[0])
    pd0_exit=pdExit[pdExit["park_time"]==0]
    pd0_exit.index=range(pd0_exit.shape[0])
    pd0ExEn=list(pd0_exit["enter_event_id"])
    # print(pdExit)
    sum=0
    i=0
    lookBack=7
    errorvalue=list(set(pd0ExEn).difference(set(EnterEventId)))
    print(errorvalue)

    pdExit.drop(pdExit[pdExit['enter_event_id'].isin(errorvalue)].index, inplace=True)
    ExitEnterEventId=list(pdExit["enter_event_id"])
    errorValue2=list(set(EnterEventId).difference(set(ExitEnterEventId)))
    pdEnter=remainValue(pdEnter,errorValue2,ExitCsv,lookBack=lookBack,flag=0)
    print(pdEnter)
    EnterEventId=list(pdEnter["event_id"])

    errorExitDifferEnter=list(set(ExitEnterEventId).difference(set(EnterEventId)))
    print(errorExitDifferEnter)

    pdExit = remainValue(pdExit, errorExitDifferEnter, ExitCsv, lookBack=lookBack,flag=1)
    print(len(pdExit),len(pdEnter))
    pdEnter.index=range(pdEnter.shape[0])
    pdExit.index = range(pdExit.shape[0])
    pdEnter=pdEnter.drop(["Unnamed: 0"],axis=1)
    pdExit = pdExit.drop(["Unnamed: 0"], axis=1)
    saveEnterName="Enter_"+csvName
    saveEnterPath=os.path.join(savePath,saveEnterName)
    pdEnter.to_csv(saveEnterPath)

    saveExitName = "Exit_" + csvName
    saveExitPath = os.path.join(savePath, saveExitName)
    pdExit.to_csv(saveExitPath)


    # print(beginDay, endDay)
if  __name__ == "__main__":
    # EnterCsv = r"data/data0526/1\10119112210362202000.csv"
    filePath=r"data/data0526/2"
    fileList=os.listdir(filePath)
    for file in fileList:
        csvPath=os.path.join(filePath,file)
        print(csvPath)
    # ExitCsv = r"data/data0526/2\10119112210362202000.csv"
    # print()
    # EndDayList=getEndDayList(ExitCsv,lookBack=7)
    # print(EndDayList)
        getNostdValue(csvPath)
