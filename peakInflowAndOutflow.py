import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from nparrayCaculate import date_compare
from functools import cmp_to_key
from nparrayCaculate import getWeekDay
import sys
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

oriCsvPath=r"I:\MachineLearning\Park\HKPark_0526\data\test\test0619"
dateCsvPath=r"data/save0527"
vehileHourNumSavePath=r"I:\MachineLearning\Park\HKPark_0526\data\test\save0618"

listDay = np.arange(5,19)


def  getThan(Datepd,date):
    if "/" in date:
        s_date = datetime.datetime.strptime(date, '%Y/%m/%d').date()
    elif "-" in date:
        s_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    Datepd['date_day1'] = pd.to_datetime(Datepd['date_day'])
    Datepd = Datepd[Datepd.date_day1 > pd.Timestamp(s_date)]                            
    return Datepd
def  getNeed(array,remainVehicle):
    # sum=500
    # sum=200
    sum=0
    needArray=np.zeros((24),dtype=int)
    for i in range(array.shape[0]):
        sum += array[i]
        needArray[i]=sum
    return needArray

fileList = os.listdir(oriCsvPath)
EnterVehicledict={}
ExitVehicledict={}
for csvName in fileList:
    # parkId=csvName.split(".")[0]
    if "Exit" in csvName:
        continue
    EnterCsvPath=os.path.join(oriCsvPath,csvName)
    ExitCsvPath=os.path.join(oriCsvPath,csvName.replace("Enter","Exit"))
    dateRemainPath = ExitCsvPath
    pd_date = pd.read_csv(os.path.join(dateCsvPath,dateRemainPath.split("\\")[-1]),usecols=["Date","Remain_Vehicle"])
    # print(pd_date)
    dateDict = pd_date.set_index(['Date'])['Remain_Vehicle'].to_dict()
    # print(dateDict)
    if not os.path.exists(ExitCsvPath):
        continue
    pdEnter=pd.read_csv(EnterCsvPath)
    pdExit=pd.read_csv(ExitCsvPath)
    pdEnter=getThan(pdEnter,"2021/3/20")
    pdExit=getThan(pdExit,"2021/3/20")
    print(pdEnter.head())
    # print(len(pdEnter),len(pdExit))
    pdEnterGroupByDate=pdEnter.groupby(["date_day"])
    pdExitGroupByDate=pdExit.groupby(["date_day"])
    for groupSon in list(pdEnterGroupByDate):
        pdEnterByDay=groupSon[1]
        groupDate=groupSon[0]
        hourCounts=pdEnterByDay["Hour"].value_counts()
        hourCountsList=list(hourCounts.items())
        hourList,_=zip(*hourCountsList)
        for i in range(24):
            if not i in hourList:
                tempTuple=(i,0)
                hourCountsList.append(tempTuple)
        sortedList=sorted(hourCountsList,key=lambda  x:x[0])
        # print(sortedList)

        _, hourList = zip(*sortedList)
        # print(hourList)
        EnterVehicledict[groupDate]=sortedList
        # for date,value in EnterVehicledict.items():
        #     print(date,value)

    for groupSon in list(pdExitGroupByDate):
        pdEnterByDay = groupSon[1]
        groupDate = groupSon[0]
        hourCounts = pdEnterByDay["Hour"].value_counts()
        hourCountsList = list(hourCounts.items())
        hourList, _ = zip(*hourCountsList)
        for i in range(24):
            if not i in hourList:
                tempTuple = (i, 0)
                hourCountsList.append(tempTuple)
        sortedList = sorted(hourCountsList, key=lambda x: x[0])
        # print(groupDate,sortedList)
        _, hourList = zip(*sortedList)
        ExitVehicledict[groupDate] = sortedList
        # for date, value in ExitVehicledict.items():
        #     print(date, value)
        # _, hourList = zip(*sortedList)

        # plt.plot(hourList)

    newKys=sorted(ExitVehicledict.keys(),key=cmp_to_key((date_compare)))
    # print(ExitVehicledict[newKys])
    # for key in newKys:
    #     print(key,ExitVehicledict[key])
    print("down")
    for key  in newKys:
        dateDayKey=datetime.datetime.strptime(key,r"%Y/%m/%d")
        strTime=dateDayKey.strftime(r"%Y-%m-%d")
        # print(dateDict[strTime])
        if  strTime not in dateDict.keys():
            continue
        remainVehicle=dateDict[strTime]

        listTuple = EnterVehicledict[key]
        _,newnewlist=zip(*listTuple)
        nparray = np.array(list(newnewlist))
        # print(nparray,nparray.max())
        # value = nparray.max()*0.7
        # index = np.argwhere(nparray>value)
        # index = np.squeeze(index)
        # print(key ,index)
        v = list(map(lambda x: x[0][1] - x[1][1], zip(EnterVehicledict[key], ExitVehicledict[key])))  
        vArray=np.array(v)
        #################################################昼忙夜闲 昼闲夜盲 预测##################################################
        # vArray=getNeed(vArray,remainVehicle)
        # print(vArray) 
        # inflowPeakTime=np.argmax(vArray)
        # outflowPeakTime=np.argmin(vArray)
        # print(inflowPeakTime,outflowPeakTime)
        # if (inflowPeakTime >=18 or inflowPeakTime<=6):
        #     if (outflowPeakTime<18 and outflowPeakTime >6):
        #         print("昼闲夜忙")
        #     else:
        #         print("none")
        # if (inflowPeakTime <18 and inflowPeakTime>6):
        #     if (outflowPeakTime>=18 or outflowPeakTime <=6):
        #         print("昼忙夜闲")
        #     else:
        #         print("none")
        #######################################################################################################################
        


        
        # print(inflowPeakTime,outflowPeakTime)
        # # if (outflowPeakTime>inflowPeakTime):
        # print(inflowPeakTime,outflowPeakTime,"昼忙夜闲")
        # else:
        #     print(inflowPeakTime,outflowPeakTime,"昼闲夜忙")
        
        print("\n")
        ###############################################流入高峰时间，流出高峰时间##################################################

        v=vArray
        v_max = v.max()
        v_min=v.min()
        v_max_value = v_max*0.5
        v_min_value = v_min*0.5
        peakInflow=np.argwhere(v>v_max_value) 
        outflowPeak=np.argwhere(v<v_min_value)
        peakInflow=np.squeeze(peakInflow)
        outflowPeak=np.squeeze(outflowPeak)
        list1,list2=zip(*EnterVehicledict[key])
        print("EnterArray is {}".format(list(list2)))
        list1,list2=zip(*ExitVehicledict[key])
        print("ExiterArray is {}".format(list(list2)))
        print(v)
        print("peakInflow is {}".format(peakInflow))
        print("outflowPeak is {}".format(outflowPeak))
        print("maxindex is  {}".format(np.argmax(v)))
        print("minindex is  {}".format(np.argmin(v)))
        print("\n\n")
        # netInflowOfVehicles
        ########################################################################################################################
       
        # negativeNum=v[np.argwhere(v<0)]
        # print(negativeNum)
        # remainVehicle = 0
        # v = list(map(lambda x: x[0][1] - x[1][1], zip(EnterVehicledict[key], ExitVehicledict[key])))
    #     timelist=[i for i in range(24)]
    #     dateList=[key for i in range(24)]
    #     vArray=np.array(v)
    #     newArray=getNeed(vArray,remainVehicle)
    #     timeTuple = list(zip(dateList, timelist, newArray.tolist()))
    #     newPdf=pd.DataFrame(timeTuple,columns=["Date","Hour","VehicleNum"])
    #     newPdf["week_day"] = newPdf["Date"].apply(getWeekDay)
    #     newPdfCsvpath=os.path.join(vehileHourNumSavePath,csvName)
    #     if not os.path.exists(newPdfCsvpath):
    #         newPdf.to_csv(newPdfCsvpath)
    #     else:
    #         newPdf.to_csv(newPdfCsvpath,mode="a",header=False)
    #     print(newPdf)
    #     print(key,newArray)
    #     plt.plot(newArray)
    #     # print(key,v)
    # plt.title(csvName)
    # plt.show()
        # print(key,list(value))