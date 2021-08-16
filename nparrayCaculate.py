import numpy as np
import pandas as pd
import time
import datetime
import os
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

def Caltime(date1,date2):
    #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    #date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    #date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    # date1=time.strptime(date1,"%Y-%m-%d")
    # date2=time.strptime(date2,"%Y-%m-%d")
    date1 = date1.strftime(r"%Y-%m-%d")
    date2=date2.strftime(r"%Y-%m-%d")
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    #date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    #date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    #返回两个变量相差的值，就是相差天数
    return date2-date1

def getParkName():
    Park_pd = pd.read_excel(r"data/车场/车场数据.xlsx",usecols=["park_id","park_name","total_park_num","park_location"])
    # print(Park_pd)
    # Park_pd.to_csv("ParkName.csv")
    parkDict={}
    idList=list(Park_pd["park_id"])
    nameList=list(Park_pd["park_name"])
    park_locationList=list(Park_pd["park_location"])
    for key,value1,value2 in zip(idList,nameList,park_locationList):
        # print(key,value)
        parkDict[key]=value1+"："+value2
    return parkDict
# print(idList)

def getSecond(strTime,minute):
    hourSecond=strTime.split(" ")[-1]
    hourTime=int(hourSecond.split(":")[0])
    miniuteTime=int(hourSecond.split(":")[-2])
    secondTime=int(hourSecond.split(":")[-1])
    Sum1=hourTime*3600+miniuteTime*60+secondTime
    sum2=int(minute)*60
    return Sum1-sum2

def getDate(strTime,minutes):
    if "-" in strTime:
        startTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
        startTime2 = (startTime + datetime.timedelta(minutes=-minutes)).strftime("%Y-%m-%d %H:%M:%S")
    elif "/" in strTime:
        startTime = datetime.datetime.strptime(strTime, "%Y/%m/%d %H:%M:%S")
        startTime2 = (startTime + datetime.timedelta(minutes=-minutes)).strftime("%Y/%m/%d %H:%M:%S")
    return startTime2

def toStardTime(strTime):
    return  datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")

def date_compare(item1, item2): #日期比较哪个在前哪个在后
    if "-" in item1:
        t1 = time.mktime(time.strptime(item1, '%Y-%m-%d'))
    elif "/" in item1:
        t1 = time.mktime(time.strptime(item1, '%Y/%m/%d'))
    if "-" in item2:
        t2 = time.mktime(time.strptime(item2, '%Y-%m-%d'))
    elif "/" in item1:
        t2 = time.mktime(time.strptime(item2, '%Y/%m/%d'))
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        return 0

def datelist(start,end,look_back=5):
    date_list = []
    if "-" in start:
        begin_date = datetime.datetime.strptime(start, r"%Y-%m-%d")
        end_date = datetime.datetime.strptime(end,r"%Y-%m-%d")
    else:
        begin_date = datetime.datetime.strptime(start, r"%Y/%m/%d")
        end_date = datetime.datetime.strptime(end, r"%Y/%m/%d")

    end_date += datetime.timedelta(days=-1)
    # begin_date += datetime.timedelta(days=1)
    while look_back>0 and end_date>=begin_date:
        date_str = end_date.strftime(r"%Y-%m-%d")
        date_list.append(date_str)
        # 日期加法days=1 months=1等等
        end_date += datetime.timedelta(days=-1)
        look_back-=1
    # print(date_list)
    return " ".join(date_list)

def datelist2(start,end):
    date_list = []
    if "-" in start:
        begin_date = datetime.datetime.strptime(start, r"%Y-%m-%d")
    elif "/" in start:
        begin_date = datetime.datetime.strptime(start, r"%Y/%m/%d")
    if "-" in end:
        # begin_date = datetime.datetime.strptime(start, r"%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, r"%Y-%m-%d")
    elif "/" in end:
        # begin_date = datetime.datetime.strptime(start, r"%Y/%m/%d")
        end_date = datetime.datetime.strptime(end,r"%Y/%m/%d")
    # begin_date += datetime.timedelta(days=1)
    # num=(end_date-begin_date).days
    while begin_date < end_date :
        num = (end_date - begin_date).days
        date_str = begin_date.strftime(r"%Y-%m-%d")
        date_list.append(date_str)
        # 日期加法days=1 months=1等等
        begin_date += datetime.timedelta(days=1)
    # print(date_list)
    return " ".join(date_list)

def  getWeekDay(dateStr):
    if "/" in dateStr:
        time1 = datetime.datetime.strptime(dateStr, r"%Y/%m/%d")
    elif "-" in dateStr:
        time1 = datetime.datetime.strptime(dateStr, r"%Y-%m-%d")
    return time1.isoweekday()

def allFilePath(rootPath,allFIleList):
    fileList = os.listdir(rootPath)
    for temp in fileList:
        if os.path.isfile(os.path.join(rootPath,temp)):
            allFIleList.append(os.path.join(rootPath,temp))
        else:
            allFilePath(os.path.join(rootPath,temp),allFIleList)
def getNumOfParkingSpace():
    csvpath = r"data\车场\车场数据.xlsx"
    pd_csv=pd.read_excel(csvpath,usecols=["park_id","total_park_num"])
    parkIdList=list(pd_csv["park_id"])
    parkIdList=[str(x) for x in parkIdList]
    # print(parkIdList)
    parkTuple=zip(parkIdList,list(pd_csv["total_park_num"]))
    paarkDict=dict(parkTuple)
    return paarkDict
    
def allFilePath(rootPath,allFIleList):
    fileList = os.listdir(rootPath)
    for temp in fileList:
        if os.path.isfile(os.path.join(rootPath,temp)):
            allFIleList.append(os.path.join(rootPath,temp))
        else:
            allFilePath(os.path.join(rootPath,temp),allFIleList)

if __name__=="__main__":
    # strTime="2021-05-24"
    # strTime2="2021-03-30"
    # csvfile=r"H:\@chengfu\ParkData\Exit\biz_parking_exit_record.csv"
    # pd_csv=pd.read_csv(csvfile,usecols=["exit_event_id","park_exit_id"])
    # print(pd_csv[:100])
    # print(getWeekDay(strTime2))
    # dayList=datelist(strTime2,strTime,1)
    # print(dayList)
    # list1=[1,2,3,4,5]
    # list2=[2,3,4,5,6]
    # print(list1+list2)
    parkDict=getNumOfParkingSpace()
    print(parkDict)
  
   
