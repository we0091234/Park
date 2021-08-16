import  numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nparrayCaculate import getWeekDay
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor as XGBR
from nparrayCaculate import allFilePath
import pickle
import os
import datetime
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

def paintPic(group):
    plt.figure(figsize=(10, 5))
    p = group.boxplot(return_type='dict')  # 画箱线图，直接使用DataFrame的方法
    x = p['fliers'][0].get_xdata()  # 'flies'即为异常值的标签
    y = p['fliers'][0].get_ydata()
    y.sort()
    for i in range(len(x)):
        if i > 0:
            plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.05 - 0.10 / (y[i] - y[i - 1]), y[i]))
        else:
            plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.10, y[i]))
    # plt.show()
    return y

def trainByParkId(csvFile):
    # csvFile =r"data\newData\Entry\10118020617152601000.csv"
    saveModelPath=r"E:\MachineLearning\Park\HKPark_0526\data\model"
    #E:\pytorch\HikiPark\HKPark_0524\data\newData\Entry\10118013020030601000.csv
    parkId=csvFile.split("\\")[-1].split(".")[0]
    pd_csv=pd.read_csv(csvFile,usecols=["date_day","time"])
    # pd_csv=pd_csv[pd_csv["park_time"]>0]
    counter=pd_csv["date_day"].value_counts()
    counterSort=list(counter.items())
    print(counterSort)
    s=sorted(counterSort,key=lambda x:x[0])
    print(s)
    # date,value=zip(*s)
    #
    # plt.plot(date,value)
    # plt.show()
    # # print(date,value)

    group = pd_csv.groupby(["date_day"], as_index=False).count()
    # print(group)
    y=paintPic(group)


    # print(group[group['time'].isin(y)])

    group.drop(group[group['time'].isin(y)].index, inplace=True)

    y=paintPic(group)
    # print(group[group['time'].isnull()])

    # print(group)
    # plt.plot(group["date_day"],group["time"])
    group["week_day"]=group["date_day"].apply(getWeekDay)

    group["date_day"]=pd.to_datetime(group["date_day"])
    group=group.sort_values(by="date_day")
    group["is_holiday"]=group["week_day"].apply(lambda x: 1 if x==6 or x==7 else 0)
    print(group)


    x=group[["week_day","is_holiday"]]
    print(x.values)

    y=group["time"]

    # x.index=range(x.shape[0])
    print(y)

    x_length=x.shape[0]
    split=int(x_length*0.9)
    X_train,X_test=x[:split],x[split:]
    y_train,y_test=y[:split],y[split:]

    reg_result=[]
    names=[]
    prediction=[]
    reg=XGBR(n_estimators=100).fit(X_train,y_train)
    saveModelName=csvFile.split("\\")[-1].split(".")[0]
    saveModelPathFile=os.path.join(saveModelPath,saveModelName)+".dat"
    pickle.dump(reg,open(saveModelPathFile,"wb"))
    # reg = pickle.load(open(saveModelPathFile, "rb"))
    # reg=RandomForestRegressor().fit(X_train,y_train)
    y_pred=reg.predict(X_test)
    plt.plot(y_pred,"r",label="prediction")
    plt.plot(list(y_test),"g",label="true")
    plt.legend()
    # plt.show()
    # for t1,t2 in zip(y_test,y_pred):
    #     print(t1,t2)
    for t1,t2 in zip(y_test,y_pred):
        print(t1,t2)
    print("")
    # plt.show()
def teDateDay(dateDay,parkId):
    parkNum = 0
    model=r"data/model/Enter_"+parkId+".dat"
    if not os.path.exists(model):

        return parkNum
    reg=pickle.load(open(model, "rb"))
    weekDay=getWeekDay(dateDay)
    is_holiday=(lambda  x: 1 if x==6 or x==7 else 0)(weekDay)
    featureList=np.array([weekDay,is_holiday]).reshape(-1,2)
    predictfe=reg.predict(featureList)
    parkNum=predictfe[0]
    res = {"parkNum": float(parkNum)}
    return  res
if __name__=='__main__':
    # filePath=r"E:\MachineLearning\Park\HKPark_0526\data\save0627"
    # fileList=[]
    # allFilePath(filePath,fileList)
    # for csvFile in fileList:
    #     if "Exit" in csvFile:
    #         continue
    # # csvFile=r"E:\MachineLearning\Park\HKPark_0526\data\save0627\Enter_10120032921114502000.csv"
    #     trainByParkId(csvFile)
    dateDay = r"2021-06-26"
    parkNum=teDateDay(dateDay,"10120030821200902000")
    print(parkNum)


