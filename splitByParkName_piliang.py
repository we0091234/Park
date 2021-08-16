import pandas as pd
import os
import datetime
import numpy as np
# -*- coding:utf-8 -*-
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

filePath = r"H:\@chengfu\ParkData\Exit"
savePath=r"H:\@chengfu\ParkData\2"


def allFilePath(rootPath,allFIleList):
    fileList = os.listdir(rootPath)
    for temp in fileList:

# foldname=r"D:\trainTemp\Upcolor\train"
# foldname=r"F:\PedestrainAttribute\onePic"
        if os.path.isfile(os.path.join(rootPath,temp)):
            allFIleList.append(os.path.join(rootPath,temp))
        else:
            allFilePath(os.path.join(rootPath,temp),allFIleList)

def getNumber(str1):
    index=1
    haha=str1.split(":")
    number=int(haha[-2])
    shizhong=haha[0].split(" ")[-1]
    if number<30:
        index=2*int(shizhong)
    else:
        index=2*int(shizhong)+1
    return str1[:10]+" "+str(index)

def parkTimeRange(ParkTimeStr):
    if int(ParkTimeStr)<=15:
        return 0
    elif int(ParkTimeStr)<=120:
        return 1
    elif int(ParkTimeStr)<=360:
        return 2
    elif int(ParkTimeStr)<=720:
        return 3
    else:
        return 4



str1="2020-12-04 11:59:34"

# ParkTimeStrList=["15分钟内","15分钟-2小时","2小时-6小时","6小时-12小时","12小时以上"]
# print(getNumber(str1))
xlsFileList=[]
allFilePath(filePath,xlsFileList)

cnt = 0
# for i_xls in range(1):
for i_xls in range(len(xlsFileList)):
    xlsfile=xlsFileList[i_xls]
    print(xlsfile)
    pd_csv=pd.read_csv(xlsfile,usecols=["park_id","time","plate_no","park_time","exit_event_id","enter_event_id"])
    # pd_csv = pd.read_csv(xlsfile, usecols=["park_id", "time", "plate_no","event_id"])
    newData=group = pd_csv.groupby(["park_id"],as_index=False)

    DataLen=len(list(newData))
    DataLen=1
    print(len(list(newData)))
    sum=0
    for i in range(len(list(newData))):
        myData=list(newData)[i][1]
        parkIDD=list(newData)[i][0]
        print(parkIDD)
        sum+=len(myData)


        # myData["time_half"]=myData["time"].apply(lambda  x:x[:13])
        # myData["ParkRange"]=myData["park_time"].apply(parkTimeRange)
        # myData["date_day"]=myData["time"].apply(lambda  x:x[:10])
        myData["date_day"] = myData["time"].apply(lambda x: x.split(" ")[0])
        myData["Hour"]=myData["time"].apply(lambda  x:x.split(" ")[-1].split(":")[0])
        ##############################################筛选时间#######################################
        s_date = datetime.datetime.strptime('2020/12/31', '%Y/%m/%d').date()
        myData['date_day1'] =pd.to_datetime(myData['date_day'])
        myData = myData[myData.date_day1 > pd.Timestamp(s_date)]
        ##############################################筛选时间#######################################

        # myData=myData.drop(["time"],axis=1)
        # print(myData)
        # newPdEnter = myData.groupby(["ParkRange","park_id"], as_index=False).count()
        # newPdEnter = newPdEnter.drop(["date_day","Hour"], axis=1)
        # print(newPdEnter)
        # parkId=myData["park_id"]
        # print(str(myData["park_id"].values[0]))
        # print(myData)
        csvName = str(parkIDD)+".csv"
        csvPath=os.path.join(savePath,csvName)
        if os.path.exists(csvPath):
            myData.to_csv(csvPath,mode='a',header=False)
        else:
            myData.to_csv(csvPath)
    print(sum)



# group = myData.groupby(["date_day","Hour"],as_index=False).count()
# print(group)
# usrTime=group["time"]
# groupTime=group["time_half"]
# array=group.values
# # print(list(groupTime))
#
# clockTime=[int(x.split(" ")[-1]) for x in list(groupTime) ]
# print(clockTime)
# print(list(usrTime))
# #
#
# newDict=dict(zip(list(groupTime),list(usrTime)))
# print(newDict)
# print(group)