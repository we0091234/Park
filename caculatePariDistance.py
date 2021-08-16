import pandas as pd
from geopy.distance import geodesic

pd_csv=pd.read_excel(r"I:\MachineLearning\Park\HKPark_0526\data\车场\车场数据.xlsx",usecols=["park_id","lat","lng"])
print(pd_csv)
pd_csv=pd_csv.loc[:,["park_id","lat","lng"]]
print(pd_csv)

# lngLat=zip(list(pd_csv["lng"]),pd_csv["lat"])
print(pd_csv.values[:1,1:],pd_csv.values[4:5,1:])

print(geodesic((pd_csv.values[:1,1:]), (pd_csv.values[6:7,1:])).km)