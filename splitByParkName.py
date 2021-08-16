import pandas as pd
import os
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

savePath=r"H:\@chengfu\车场数据\later\new\exit"

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


str1="2020-12-04 11:59:34"

# print(getNumber(str1))

pd_csv=pd.read_excel(r"H:\@chengfu\车场数据\later\20210201-20210207车场数据\2021-02-01出车.xlsx",usecols=["park_id","time"])
newData=group = pd_csv.groupby(["park_id"],as_index=False)

DataLen=len(list(newData))
DataLen=1
print(len(list(newData)))
sum=0
for i in range(len(list(newData))):
    myData=list(newData)[i][1]
    sum+=len(myData)


# myData["time_half"]=myData["time"].apply(lambda  x:x[:13])
    myData["date_day"]=myData["time"].apply(lambda  x:x[:10])
    myData["Hour"]=myData["time"].apply(lambda  x:int(x[10:13]))
    myData=myData.drop(["time"],axis=1)
    print(myData)

    parkId=myData["park_id"]
    print(str(myData["park_id"].values[0]))
    print(myData)
    csvName = str(myData["park_id"].values[0])+".csv"
    csvPath=os.path.join(savePath,csvName)
    myData.to_csv(csvPath,mode='a',header=False)
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