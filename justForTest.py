import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt
from nparrayCaculate import getParkName
csvPath=r"I:\MachineLearning\Park\HKPark_0526\data\test_0528\2\Enter_10118020710141001000.csv"
ps_csv=pd.read_csv(csvPath)

weekCsv=ps_csv.groupby(["week_day"])
i=0
for temp2 in weekCsv:
    print(temp2)
    everyDayPd=temp2[1].groupby(["Date"])
    plt.figure()
    plt.xlim(0, 24)
    plt.ylim(0, 900)
    for temp1 in everyDayPd:
        print(temp1[0],temp1[1])
        plt.plot(list(temp1[1]["VehicleNum"]))
    plt.title(str(temp2[0]))
plt.show()



    # i+=1
    # if i>=1:
    #     break
