import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pandas.io.parsers import read_csv
from nparrayCaculate import getNumOfParkingSpace
EnterExitCsvFilePath =r"data\test_0528\2"
# parkDict=getNumOfParkingSpace()
# i =0
# fileList = os.listdir(EnterExitCsvFilePath)
# parkGapList=[]
# for file in fileList:
#     filePath =os.path.join(EnterExitCsvFilePath,file)
#     if "Exit" in file:
#         continue
#     i+=1
#     parkId = file[file.find("_")+1:].split('.')[0]
#     parkNumOfRegist=parkDict[parkId]
    
#     pd_csv=pd.read_csv(filePath)
#     parkNumReal=pd_csv["VehicleNum"].max()
#     testList=[parkId,parkNumOfRegist,parkNumReal]
#     testListTuple=tuple(testList)
#     parkGapList.append(testListTuple)
    # print("parkId:%s biaoji:%d Real:%d"%(parkId,parkNumOfRegist,parkNumReal))
    # print(i)

# print(parkGapList)
# pd_New = pd.DataFrame(parkGapList,columns=["parkId","totalNum","VehicleNum"])
# pd_New.to_csv("totalParkNum.csv")
def getParkGap(parkId:str=None,pDate:str=None):


    pd_new = pd.read_csv(r"totalParkNum.csv")
    print(pd_new.head())
    pariList1=list(pd_new["parkId"])
    totalNumList=list(pd_new["totalNum"])
    VehicleNumList=list(pd_new["VehicleNum"])

    realGapDict={}
    for  x,y,z in zip(pariList1,totalNumList,VehicleNumList):
        if y>z:
            realGapDict[str(x)]=0
        else:
            realGapDict[str(x)]=z-y
    print(realGapDict)
    # print(realGapDict[parkId])
    print(realGapDict[parkId])


if __name__=="__main__":
    getParkGap("10118020617152601000","2021-06-08")

    # pass