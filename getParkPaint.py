import numpy as np
import pandas as pd
from nparrayCaculate import getParkName
import os
import sklearn
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

filePath =r"data/Gaofeng/Extra/Exit"
newFilePath =r"data/save1/Exit"

fileList=os.listdir(filePath)
dictList=[]
# plateNoList=[]

def PlateBendi(plateList):
    pass
for  file in fileList:
    dict={}
    parkId=file.split(".")[0]
    csvPath=os.path.join(filePath,file)
    csvPath1=os.path.join(newFilePath,file)
    # if  os.path.exists(）
    dict["编号"]=parkId
    dict["地址"]=getParkName()[int(parkId)].split("：")[0]
    dict["潮汐规律"]="无"
    dict["车流高峰"]="无"
    dict["流入高峰"]="6:00-09:00"
    dict["流出高峰"]="16:00-18:00"

    plate_csv=pd.read_csv(csvPath1,usecols=["plate_no"])
    # print(plate_csv)
    plateList=list(plate_csv["plate_no"])
    # plateNoList+=plateList

    localPlateNum=0
    nonLocalPlateNum=0
    # print(plateList)
    # print(len(plateNoList))
    for temp in plateList:
        if temp[0]=="浙" and temp[1]=="F":
            localPlateNum+=1
        else:
            # print(temp)
            nonLocalPlateNum+=1
    print(localPlateNum,nonLocalPlateNum)
    dict["本地车(辆)"]=localPlateNum
    dict["外地车(辆)"]=nonLocalPlateNum
    dict["本地车占比"]='percent: {:.2%}'.format(localPlateNum/(len(plateList)))
    dict["外地车占比"] = 'percent: {:.2%}'.format(nonLocalPlateNum / (len(plateList)))
    dictList.append(dict)
    # print(dict)

# print(dictList)
df1 =pd.read_csv(r"painter.csv",encoding="gbk")
print(df1)
df1=sklearn.utils.shuffle(df1)
df1.to_csv("painter_new.csv")
#
# print(df)


