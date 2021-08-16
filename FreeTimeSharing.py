import pandas as pd
import numpy as np
import os
import pickle
import sys
import io
from nparrayCaculate import getWeekDay
from nparrayCaculate import allFilePath
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor as XGBR
import shutil
from geopy.distance import geodesic

pd.options.display.max_rows = None
pd.options.display.max_columns = None



def  getParkRatio(saveCsvPath):
    parkNumDict ={}
    # saveCsvPath = r"E:\pytorch\HikiPark\0702\data\test_0528\test"
    
    csvFilelist =[]
    allFilePath(saveCsvPath,csvFilelist)
    
    for csvFile in csvFilelist:
        maxList=[]
        if csvFile.endswith(".csv"):
            pd_csv = pd.read_csv(csvFile)
            everyDayPd=pd_csv.groupby(["Date"])
            vehicleNum = list(pd_csv["VehicleNum"])
            vehicleNum=np.array(vehicleNum)
            for temp in everyDayPd:
                maxList.append(np.array(list(temp[1]["VehicleNum"])).max())
                # print(temp[0],np.array(list(temp[1]["VehicleNum"])).max())

        parkId = csvFile.split("\\")[-1].split("_")[-1].split(".")[0]
        # if parkId=="10120102217415601000":
        #     print(maxList)
        meanData = np.array(maxList).mean()
        parkNumDict[parkId]=meanData
      
    return parkNumDict

  
    

def getRealparkNum(csvPath):
    pd_new = pd.read_csv("totalParkNum.csv")
    parkGapNum=0
    pariList1=list(pd_new["parkId"])
    pariList1=[str(x) for x in pariList1]
    totalNumList=list(pd_new["totalNum"])
    VehicleNumList=list(pd_new["VehicleNum"])

    newDict = dict(zip(pariList1,totalNumList))

    newDict2 = dict(zip(pariList1,VehicleNumList))

    return newDict,newDict2

def getMax(a,b):
    if a>b:
        return a
    else:
        return b

def getTotalParkNumDict(saveCsvPath):
    myNewDict ={}
    parkNumDict=getParkRatio(saveCsvPath)
    newDict,newDict2=getRealparkNum("totalParkNum.csv")
    for key in newDict.keys():
        ratio = (newDict2[key]-parkNumDict[key])/parkNumDict[key]
        if ratio >5 or ratio <=0.5:
            myNewDict[key]=parkNumDict[key]
        elif ratio <=5 and ratio >0.5:
            myNewDict[key]=newDict2[key]
        else:
            myNewDict[key]=parkNumDict[key]
    return myNewDict
  
def getParkRatio(parkId,date):
    modelName = parkId+".dat"
    modelPath= os.path.join("freeTimeModle",modelName)
    reg = pickle.load(open(modelPath, "rb"))

    weekDay=getWeekDay(date)
    weekDayArray=[weekDay for i in range(24)]
    weekDayArray=np.array(weekDayArray)
    hourArray = np.arange(24)
    weekDayArray=weekDayArray.reshape(-1,1)
    hourArray=hourArray.reshape(-1,1)
    # print(hourArray)
    # print(weekDayArray)
    newArray=np.concatenate((hourArray,weekDayArray),axis=1)
    # print(newArray)

    newPredict=reg.predict(newArray)

    return newPredict


def getLatAndLon(parkLotPath):
    pd_csv=pd.read_excel(parkLotPath,usecols=["park_id","lat","lng"])
    pd_csv=pd_csv.loc[:,["park_id","lat","lng"]]  #lag和lng调换位置
    latList = pd_csv["lat"]
    lngList= pd_csv["lng"]
    latLngList = list(zip(latList,lngList))
    parkIdList =list(pd_csv["park_id"])
    parkIdList=[str(x) for x in parkIdList]
    # print(list(latLngList))
    myDict = dict(zip(parkIdList,latLngList))
    return myDict

def getDistance(parkId1,parkId2,LatAndLonDict):
    return geodesic(LatAndLonDict[parkId1],LatAndLonDict[parkId2])

if __name__ == "__main__":
    modelPath = r"freeTimeModle"
    modelList = []
    allFilePath(modelPath,modelList)
    i = 0
    LatAndLonDict=getLatAndLon(r"data\车场\车场数据.xlsx")
    AllfreeAndBusyTimeDict={}
    for modelFile in modelList:
        freeAndBusyTimeDict={}
        parkId = modelFile.split("\\")[-1].split(".")[0]
        predictArray=getParkRatio(parkId,"2020/07/09")
        predictArray = np.array(predictArray)
        buasyTimeArray = np.where(predictArray>0.7)
        freeTimeArray =np.where(predictArray<0.5)
        freeAndBusyTimeDict["free"]=freeTimeArray
        freeAndBusyTimeDict["busy"]=buasyTimeArray
        AllfreeAndBusyTimeDict[parkId]=freeAndBusyTimeDict
        # print("{} freeTime is {}".format(parkId,np.where(predictArray<0.5)))
        i+=1
        # if i>1:
        #     break
        # for otherModel in modelList:
        #     otherParkId=otherModel.split("\\")[-1].split(".")[0]
        #     if otherModel==modelFile:
        #         continue
        #     print("{} 和{} 距离is {}".format(parkId,otherParkId,getDistance(parkId,otherParkId,LatAndLonDict)))
    myParkId = '10118020617152601000'
    distanceLimit = 5
    busyArray = AllfreeAndBusyTimeDict[myParkId]["busy"][0]
    # print("haha")
    for key in AllfreeAndBusyTimeDict.keys():
        if key == myParkId:
            continue
        ParkLotDistance =  getDistance(myParkId,key,LatAndLonDict)
        # disKm = ParkLotDistance["km"]
        floatDis=ParkLotDistance.km
        print(type(floatDis))
        if floatDis <distanceLimit:
            freeArray = AllfreeAndBusyTimeDict[key]["free"][0]
            print(freeArray)
            for busyTime in busyArray:
                if busyTime in freeArray:
                    print("{} 时段{} is busy,{} is free distance is {}".format(myParkId,busyTime,key,floatDis))
                    print("{} 时段{} is busy,{} is free distance is {}".format(myParkId,busyTime,key,floatDis))
    # parkCsvPath = r"I:\MachineLearning\Park\HKPark_0526\data\test_0528\2_new"
    # testPath = r"I:\MachineLearning\Park\HKPark_0526\data\test_0528\test"
    # saveModelPath=r"I:/MachineLearning/Park/HKPark_0526/data/test_0528/test/saveMocel"
    # myDict=getTotalParkNumDict(parkCsvPath)
    # fileList=[]
    # allFilePath(testPath, fileList)
   
    # for csvFile in fileList:
    #     rightLabel = 0
    #     parkId = csvFile.split("\\")[-1].split("_")[-1].split(".")[0]
    #     pd_csv = pd.read_csv(csvFile)
    #     pd_csv["ratio"]=pd_csv["VehicleNum"].apply(lambda x: int(x)/myDict[parkId])
    #     pd_csv["is_busy"]=pd_csv["ratio"].apply(lambda x: 1 if x >0.9 else 0)
    #     # print(pd_csv[:200])
    #     newPdcsv=pd_csv[["Hour","week_day"]]
    #     x=newPdcsv
    #     y=pd_csv[["ratio"]]
    #     x_length = newPdcsv.shape[0]
    #     # print(x_length)
    #     split=int(x_length*0.9)
    #     X_train,X_test=x[:split],x[split:]
    #     y_train,y_test=y[:split],y[split:]
    #     reg=XGBR(n_estimators=100).fit(X_train,y_train)

    #     saveModelName=parkId
    #     saveModelPathFile=os.path.join(saveModelPath,saveModelName)+".dat"
    #     pickle.dump(reg,open(saveModelPathFile,"wb"))
    #     # reg = pickle.load(open(saveModelPathFile, "rb"))
    #     # print(X_train.values.shape)
    #     yTestList = list(y_test["ratio"])
    #     Xdate = list(X_test["Hour"])
    #     y_pred=reg.predict(X_test)
    #     # print(y_pred,y_test)
    #     for i in range(X_test.shape[0]):
    #         PredLabel =y_pred[i]>0.9
    #         RealLabel =yTestList[i]>0.9
    #         if PredLabel==RealLabel:
    #             rightLabel+=1
    #         print(Xdate[i],y_pred[i],yTestList[i])

    #     # weekDay=getWeekDay("2021/07/04")
    #     # # print(weekDay)
    #     # weekDayArray=[weekDay for i in range(24)]
    #     # weekDayArray=np.array(weekDayArray)
    #     # hourArray = np.arange(24)
    #     # weekDayArray=weekDayArray.reshape(-1,1)
    #     # hourArray=hourArray.reshape(-1,1)
    #     # # print(hourArray)
    #     # # print(weekDayArray)
    #     # newArray=np.concatenate((hourArray,weekDayArray),axis=1)
    #     # # print(newArray)

    #     # newPredict=reg.predict(newArray)

    #     # # print(newPredict)
       

    #     print("{} 正确率 is {}".format(parkId,rightLabel/X_test.shape[0]))
    
        

