#通过计算停车时间算出日期前一天晚上的停留车辆有多少


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

savePath=r"E:\MachineLearning\Park\HKPark_0526\data\save0527"
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

def  getRemainDate(csvPath):
    # csvPath=r"E:\MachineLearning\Park\HKPark_0526\data\save0627\Exit_10119123017444502000.csv"
    pd_csv=pd.read_csv(csvPath)
    myList=pd_csv["time"]
    pd_csv["Enter_time"]=pd_csv.apply(lambda row:getDate(row["time"],row["park_time"]),axis=1)
    pd_csv["Enter_State"]=pd_csv.apply(lambda row:getSecond(row["time"],row["park_time"]),axis=1)
    df=pd_csv["Enter_State"]<0
    newdf=pd_csv[df]
    newdf["Enter_Day"]=newdf["Enter_time"].apply(lambda  x: x.split(" ")[0])

    newdf["Daylist"]=newdf.apply(lambda row:datelist2(row["Enter_Day"],row["date_day"]),axis=1)
    s_date = datetime.datetime.strptime('2021-04-10', '%Y-%m-%d').date()
    # print(newdf[:100])
    # dateDf=datetime.datetime.strptime(newdf["date_day"], '%Y-%m-%d').date()
    newdf['date_day1']=pd.to_datetime(newdf['date_day'])
    # myData['date_day1'] = pd.to_datetime(myData['date_day'])
    TimeDf=newdf[newdf.date_day1>pd.Timestamp(s_date)]
    print(newdf)
    # print(dateDf)
    # head=newdf.head()
    # for temp in head:
    #     print(temp)
    haha=list(newdf["Daylist"])
    haha1=[ x  for x in haha if  len(x)>0]
    dayListStr=" ".join(haha1)
    monthDayList=dayListStr.split(" ")
    StaticsTime=Counter(monthDayList)
    m=StaticsTime.most_common(len(StaticsTime))
    timeDict1={}
    d,v=zip(*m)
    dateList=getEndDayList2(csvPath)

    for   temp in m:
        timeDict1[str(temp[0])]=temp[1]

    for day in dateList:
        if not day in d:

            timeDict1[day] = 0


    print(timeDict1)
    # for temp in haha:
    #     if temp:
    #         print(temp)
    # hahaDf=newdf[haha]
    # newdf["times"] = newdf.groupby("date_day").count()
    # EnterDayList=list(newdf["Enter_Day"])
    # # print(newdf.head())
    # newDict=Counter(EnterDayList)
    # k = newDict.most_common(len(newDict))
    # timeDict={}
    # for   temp in k:
    #     timeDict[str(temp[0])]=temp[1]
    #
    # print(timeDict,timeDict1)
    #
    # for key,value in timeDict.items():
    #     for key1,value1 in timeDict1.items():
    #         if key1==key:
    #             timeDict[key]+=timeDict1[key1]
    # print(timeDict)
    # keys=timeDict.keys()

    s=sorted(timeDict1.items(),key=lambda x:x[0])
    print(s)
    keys,values=zip(*s)
    nePdf=pd.DataFrame(s,columns=["Date","Remain_Vehicle"])
    print(nePdf)
    nePdf["Date"]=pd.to_datetime(nePdf['Date'])+ datetime.timedelta(1)
    print(nePdf)
    csvName=csvPath.split("\\")[-1]
    nePdf.to_csv(os.path.join(savePath,csvName))

if __name__=="__main__":
    filePath=r"E:\MachineLearning\Park\HKPark_0526\data\save0627"
    fileList=os.listdir(filePath)
    for file in fileList:
        if "Exit" in file:
            csvPath=os.path.join(filePath,file)
    # csvPath = r"E:\MachineLearning\Park\HKPark_0526\data\save0627\Exit_10120120121244302000.csv"
    # print(getEndDayList2(csvPath))
            getRemainDate(csvPath)
# for key,value in zip(keys,values):
#     print(key,value)
# plt.plot(s)
# plt.show()
# NewDict={}
# print(sorted(keys,key=cmp_to_key((date_compare))))
# for temp in sorted(keys,key=cmp_to_key((date_compare))):
#     # print(temp,timeDict[temp])
#     # if timeDict[temp]>200:
#         NewDict[temp]=timeDict[temp]

# keys=NewDict.keys()
# value=NewDict.values()
# plt.plot(values)
# plt.show()

# New=sorted(timeDict.keys(),date_compare)
# print(New)
# pd_csv["Enter_time"]=getDate(pd_csv["time"],pd_csv["park_time"])
# print(newdf[newdf.Enter_Day.isin(['2021-04-01'])])
# print(EnterGroup)
# dayCount=newdf["Enter_Day"].value_counts()
# dayCountList=dayCount.tolist()
#
# # d_dic = dayCount.set_index('axes')['values'].to_dict()
# print(dayCountList)
# print(newdf["Enter_Day"].value_counts())