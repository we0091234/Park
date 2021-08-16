import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.pyplot import MultipleLocator
import matplotlib.font_manager as fm
from nparrayCaculate import getParkName
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-

zhfont = fm.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')

calander=['2021-04-03','2021-04-04','2021-04-05','2021-04-10','2021-04-11']
testCalander=['2021-04-13','2021-04-14']

parkDict=getParkName()

print(parkDict)

weekArray=np.zeros((1,24))
workDayArray=np.zeros((1,24))
testDayArray=np.zeros((1,24))

def  getNeed(array):
    # sum=500
    # sum=200
    sum=0
    needArray=np.zeros((24),dtype=int)
    for i in range(array.shape[0]):
        sum += array[i]
        needArray[i]=sum
    return needArray

def getCarNum(Group):
    HourList = list(Group["Hour"])
    parkNumList = list(Group["park_id"])
    array1 = np.zeros((24), dtype=int)
    array1[HourList] = parkNumList
    return array1

def allFilePath(rootPath,allFIleList):
    fileList = os.listdir(rootPath)
    for temp in fileList:

# foldname=r"D:\trainTemp\Upcolor\train"
# foldname=r"F:\PedestrainAttribute\onePic"
        if os.path.isfile(os.path.join(rootPath,temp)):
            allFIleList.append(os.path.join(rootPath,temp))
        else:
            allFilePath(os.path.join(rootPath,temp),allFIleList)

fileList =[]
path =r"data\test\Entry"
exitPath =r"data\test\Exit"
savePath = r"H:\@chengfu\车场数据\later\test\2\save"

allFilePath(path,fileList)
i =0
for i in range(1):
# for i in range(len(fileList)):
    allArray=np.zeros((1,24))
    xlsFile=fileList[i]
    npArrayParkDict = {}
    npArrayNeedDict = {}
    npRemainArrayDict={}
    park_id=xlsFile.split("\\")[-1].split(".")[0]
    print(park_id)
    i+=1
    pd_enter=pd.read_csv(xlsFile)
    exitName =os.path.join(exitPath,xlsFile.split("\\")[-1])
    if not os.path.exists(exitName):
        print("%s 不存在"%exitName)
        continue
    # print(i,xlsFile,exitName)
    pd_exit=pd.read_csv(exitName)
    newPdEnter = pd_enter.groupby(["date_day"], as_index=False)
    newPdExit=pd_exit.groupby(["date_day"], as_index=False)
    Enter_dict={}
    Exit_dict={}
    for i in range(len(list(newPdEnter))):
        pd_byDayEnter=list(newPdEnter)[i]
        Enter_dict[pd_byDayEnter[0]]=pd_byDayEnter[1]
    for i in range(len(list(newPdExit))):
        pd_byDayEnter = list(newPdExit)[i]
        Exit_dict[pd_byDayEnter[0]] = pd_byDayEnter[1]

    for key,value in Enter_dict.items():
        group = value.groupby(["date_day", "Hour","park_id"], as_index=False).count()
        EnterGroup= value.groupby(["date_day","Hour"], as_index=False).count()
        # print(EnterGroup)
        if not key in Exit_dict.keys():
            continue
        ExitGroup=Exit_dict[key].groupby(["date_day","Hour"], as_index=False).count()
        # print(ExitGroup)
        # print(park_id)
        EnterArray=getCarNum(EnterGroup)
        ExitArray=getCarNum(ExitGroup)
        # print(EnterArray)
        # print(ExitGroup)
        subArray=EnterArray-ExitArray
        npArrayParkDict[key]=subArray
        # print(subArray)
        needArray=getNeed(subArray)
        capacity=needArray.max()-needArray.min()
        # print(needArray)
        # allArray=needArray
        # allArray=np.concatenate((allArray,needArray))
        npArrayNeedDict[key] = needArray
        reMainPark=800-(needArray+575)
        npRemainArrayDict[key]=reMainPark
        for i in range(reMainPark.shape[0]):
            if reMainPark[i]<0:
                reMainPark[i]=0

        print(reMainPark)
        # # print(EnterArray-ExitArray)
        # plt.plot(EnterArray)
        # plt.plot(ExitArray)
        # plt.plot(subArray)
        # plt.show()
        print(key)

    for key, value in npRemainArrayDict.items():
        if key in calander:
            newValue = value.reshape(-1, 24)
            weekArray = np.concatenate((weekArray, newValue))
            ax = plt.gca()
            x_major_locator = MultipleLocator(1)
            ax.xaxis.set_major_locator(x_major_locator)
            plt.subplot(1, 2, 1)
            plt.title(str(parkDict[int(park_id)]))
            plt.plot(value, label=key)
            plt.xlim(0, 24)
            plt.xlabel('时刻/时', fontsize=14)
            plt.ylabel('数量', fontsize=14)
            plt.legend()
        elif not key in testCalander:
            newValue = value.reshape(-1, 24)
            workDayArray = np.concatenate((workDayArray, newValue))
            plt.subplot(1, 2, 2)
            plt.xlim(0, 24)
            plt.xlabel('时刻/时', fontsize=14)
            plt.ylabel('数量', fontsize=14)
            plt.plot(value, label=key)
        else:
            newValue = value.reshape(-1, 24)
            testDayArray = np.concatenate((testDayArray, newValue))

    # plt.xlabel(park_id)
    # plt.ylabel('停车量/辆')
    # print(parkDict[int(park_id)])
    plt.title(str(parkDict[int(park_id)]))
    plt.legend()
    plt.show()
    # print(allArray[1:])
    # allArray=allArray[1:]
    # submax=np.amax(allArray,axis=1)-np.amin(allArray,axis=1)
    # print(submax.max())
    #
    # print(allArray[0])
    # print()

    weekArray=weekArray[1:]
    workDayArray=workDayArray[1:]
    testDayArray=testDayArray[1:]


    predictWeek=np.mean(weekArray,axis=0)
    predictWorkDay=np.mean(workDayArray,axis=0)
    print(predictWeek)
    plt.title(str(parkDict[int(park_id)]))
    plt.plot(testDayArray[1], label="true")
    plt.plot(predictWorkDay, label="prediction")
    plt.xlabel('时刻/时', fontsize=14)
    plt.ylabel('数量', fontsize=14)
    plt.legend()
    plt.show()


