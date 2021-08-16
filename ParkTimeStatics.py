import pandas as pd
import os
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np
from matplotlib.pyplot import MultipleLocator
import matplotlib.font_manager as fm
from nparrayCaculate import getParkName
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-

zhfont = fm.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')

pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

filePath = r"data/ParkTime"
savePath=r"H:\@chengfu\车场数据\later\20210331-20210414车场数据\ParkTime\3"

parkDict=getParkName()
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

ParkTimeStrList=["15分钟内","15分钟-2小时","2小时-6小时","6小时-12小时","12小时以上"]
# print(getNumber(str1))
xlsFileList=[]
allFilePath(filePath,xlsFileList)

cnt = 0
# for i_xls in range(1):
for i_xls in range(len(xlsFileList)):
    xlsfile=xlsFileList[i_xls]
    print(xlsfile)

    pd_csv=pd.read_csv(xlsfile)
    newData = pd_csv.groupby(["ParkRange","park_id"],as_index=False).count()
    print(newData)
    sizes=list(newData["park_time"])
    # orilist=[0]*5
    orilist=np.zeros((5),dtype=int)

    newList=list(newData["ParkRange"])

    orilist[newList]=sizes
    # print(orilist)
    # print(list(newData["park_time"]))
    # sizes = [46,253,321,66] #每块值
    parkId=list(pd_csv["park_id"])[0]
    plt.figure(figsize=(6,9))
    colors = ['red','yellowgreen','lightskyblue','yellow'] #每块颜色定义
    explode = (0,0,0.02,0) #将某一块分割出来，值越大分割出的间隙越大
    plt.title(parkDict[parkId])
    # plt.pie(sizes, explode=explode, labels=ParkTimeStrList, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.pie(orilist,labels=ParkTimeStrList,autopct='%1.1f%%')
    #patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.legend()
    plt.show()

    # DataLen=len(list(newData))
    # DataLen=1
    # print(len(list(newData)))
    # sum=0
    # for i in range(len(list(newData))):
    #     myData=list(newData)[i][1]
    #     sum+=len(myData)
    #
    #
    # # myData["time_half"]=myData["time"].apply(lambda  x:x[:13])
    #     myData["ParkRange"]=myData["park_time"].apply(parkTimeRange)
    #     myData["date_day"]=myData["time"].apply(lambda  x:x[:10])
    #     myData["Hour"]=myData["time"].apply(lambda  x:int(x[10:13]))
    #     myData=myData.drop(["time"],axis=1)
    #     # print(myData)
    #     newPdEnter = myData.groupby(["ParkRange","park_id"], as_index=False).count()
    #     newPdEnter = newPdEnter.drop(["date_day","Hour"], axis=1)
    #     # print(newPdEnter)
    #     parkId=myData["park_id"]
    #     print(str(myData["park_id"].values[0]))
    #     # print(myData)
    #     csvName = str(myData["park_id"].values[0])+".csv"
    #     csvPath=os.path.join(savePath,csvName)
    #     if os.path.exists(csvPath):
    #         myData.to_csv(csvPath,mode='a',header=False)
    #     else:
    #         myData.to_csv(csvPath)
    # print(sum)



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