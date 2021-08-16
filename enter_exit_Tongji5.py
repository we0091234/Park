import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.pyplot import MultipleLocator
import matplotlib.font_manager as fm
from nparrayCaculate import getParkName
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',100)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-

zhfont = fm.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')

calander=['2021-04-03','2021-04-04','2021-04-05','2021-04-10','2021-04-11']
testCalander=['2021-04-13','2021-04-14']

ParkTimeStrList=["15分钟内","15分钟-2小时","2小时-6小时","6小时-12小时","12小时以上"]
typeList=["zao高峰","wan高峰","医院","潮汐高峰","节假日高峰","Extra"]
parkDict=getParkName()

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

rootpath =r"data/Gaofeng"
TypeNum=0
path=os.path.join(rootpath,typeList[TypeNum])
Entrypath =os.path.join(path,"Entry")
exitPath =os.path.join(path,"Exit")
savePath = r"H:\@chengfu\车场数据\later\test\2\save"
ParkRangePath = r"data/ParkTime"
npArrayCsvFolder=r"data/NpCsv"
allFilePath(Entrypath,fileList)
i =0

for i in range(len(fileList)):
    needArrayMax=0
    needArrayMin=0
    weekArray = np.zeros((1, 24))
    workDayArray = np.zeros((1, 24))
    testDayArray = np.zeros((1, 24))
# for i in range(len(fileList)):
    allArray=np.zeros((1,24))
    xlsFile=fileList[i]
    npArrayParkDict = {}
    npArrayNeedDict = {}
    npRemainArrayDict={}
    park_id=xlsFile.split("\\")[-1].split(".")[0]
    if park_id=="10119112210362202000":
        print(park_id)
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
        if needArrayMax <needArray.max():
            needArrayMax=needArray.max()
        if needArrayMin > needArray.min():
            needArrayMin = needArray.min()
        # print(needArray)
        capacity=needArray.max()-needArray.min()
        # print(needArray)
        # allArray=needArray
        # allArray=np.concatenate((allArray,needArray))
        npArrayNeedDict[key] = needArray
        reMainPark=350-(needArray)
        npRemainArrayDict[key]=reMainPark
        for i in range(reMainPark.shape[0]):
            if reMainPark[i]<0:
                reMainPark[i]=0

        # print(reMainPark)
        # # print(EnterArray-ExitArray)
        # plt.plot(EnterArray)
        # plt.plot(ExitArray)
        # plt.plot(subArray)
        # plt.show()
        # print(key)
    plt.figure()
    icW=0
    icD=0
    for key, value in npArrayNeedDict.items():
        week=0
        day=0

        if key in calander:
            # plt.figure()
            week+=1
            icW+=1
            newValue = value.reshape(-1, 24)
            # print(value.max())
            weekArray = np.concatenate((weekArray, newValue))
            ax = plt.gca()
            x_major_locator = MultipleLocator(1)
            ax.xaxis.set_major_locator(x_major_locator)


            #
            if week==1:

                plt.subplot(2, 1,2)
                plt.title("周末节假日")
                # plt.title(str(parkDict[int(park_id)]))
                plt.xlim(0, 24)
                plt.ylim(needArrayMin, needArrayMax)
                # plt.ylim()
                plt.xlabel('时刻/时', fontsize=14)
                plt.ylabel('净流入量', fontsize=14)
            if icW==2:

                # plt.plot(value, label=key)
                plt.plot(0.5*value, label="predict")
                # plt.plot(value, label="true")
            elif icW==1:
    
                # plt.plot(value, label=key)
                # plt.plot(value, label="predict")
                plt.plot(0.5*value, label="true")


            plt.legend()
        elif not key in testCalander:
            day+=1
            icD+=1
            newValue = value.reshape(-1, 24)
            workDayArray = np.concatenate((workDayArray, newValue))

            #
            if day == 1:
                # plt.figure()
                plt.subplot(2, 1,1)
                plt.title("工作日")
                plt.xlim(0, 24)
                plt.ylim(needArrayMin, needArrayMax)
                plt.xlabel('时刻/时', fontsize=14)
                plt.ylabel('净流入量', fontsize=14)
            if icD==2:
    
                # plt.plot(value, label=key)
                plt.plot(value, label="predict")
            elif icD==1:
    
                # plt.plot(value, label=key)
                plt.plot(value, label="true")
            plt.legend()
        else:
            print(key)
            newValue = value.reshape(-1, 24)
            testDayArray = np.concatenate((testDayArray, newValue))

        # plt.xlabel(park_id)
        # plt.ylabel('停车量/辆')
        # print(parkDict[int(park_id)])

    # plt.legend()

    # weekArray = weekArray[1:]
    # workDayArray = workDayArray[1:]
    # testDayArray = testDayArray[1:]
    # reShapeWorkData=np.transpose(workDayArray)
    # pd_data = pd.DataFrame(testDayArray)
    # # new_data=
    # print(pd_data)
    # # npArrayCsvName=park_id+"_Test.csv"
    # # npArrayCsvPath = os.path.join(npArrayCsvFolder,npArrayCsvName)
    # # pd_data.to_csv(npArrayCsvPath)

    # predictWeek = np.mean(weekArray, axis=0)
    # print(workDayArray)
    # predictWorkDay = np.mean(workDayArray, axis=0)
    # print(predictWeek)

    # plt.subplot(2, 2, 4)
    # ax = plt.gca()
    # x_major_locator = MultipleLocator(1)
    # ax.xaxis.set_major_locator(x_major_locator)
    # plt.xlim(0, 24)
    # plt.ylim(needArrayMin, needArrayMax)
    # plt.title("预测 2021-04-13")
    # plt.plot(testDayArray[-1], label="true")
    # plt.plot(predictWorkDay, label="prediction")
    # plt.xlabel('时刻/时', fontsize=14)
    # plt.ylabel('净流入量', fontsize=14)
    # plt.legend()
    # # plt.show()
    # ##########################################################饼干图###################################################
    # BxlsFile=park_id+".csv"
    # BxlsFilePath=os.path.join(ParkRangePath,BxlsFile)
    # pd_csv = pd.read_csv(BxlsFilePath)
    # newData = pd_csv.groupby(["ParkRange", "park_id"], as_index=False).count()
    # print(newData)
    # sizes = list(newData["park_time"])
    # # orilist=[0]*5
    # orilist = np.zeros((5), dtype=int)

    # newList = list(newData["ParkRange"])

    # orilist[newList] = sizes
    # # print(orilist)
    # # print(list(newData["park_time"]))
    # # sizes = [46,253,321,66] #每块值
    # parkId = list(pd_csv["park_id"])[0]
    # # plt.figure(figsize=(6, 9))
    # plt.subplot(2, 2, 3)
    # colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow']  # 每块颜色定义
    # explode = (0, 0, 0.02, 0)  # 将某一块分割出来，值越大分割出的间隙越大
    # plt.title("停车时间分布")
    # # plt.pie(sizes, explode=explode, labels=ParkTimeStrList, autopct='%1.1f%%', shadow=False, startangle=150)
    # plt.pie(orilist, labels=ParkTimeStrList, autopct='%1.1f%%')
    # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部文本
    # x，y轴刻度设置一致，保证饼图为圆形
    # plt.axis('equal')
    # plt.legend()
    # ##########################################################饼干图###################################################



    # plt.suptitle(str(parkId)+str(parkDict[int(park_id)]))
    plt.legend()
    plt.show()
    # print(allArray[1:])
    # allArray=allArray[1:]
    # submax=np.amax(allArray,axis=1)-np.amin(allArray,axis=1)
    # print(submax.max())
    #
    # print(allArray[0])
    # print()




