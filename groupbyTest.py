import pandas as pd

df=pd.DataFrame({"货号":['A','B','B','A','B'],\
                 '平台':['淘宝','淘宝','京东','京东','淘宝'],\
                 '销量':[1,2,3,4,5]})

newdata=df.groupby(["货号","平台"]).count()

print(newdata)