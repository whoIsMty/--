import pandas as pd


# 需要把sample改一下
path = r"C:\Users\Leo\Desktop\Proteins.xlsx"
sample = "AT1	BT1	CT1	DT1	AT2	BT2	CT2	DT2	AT3	BT3	CT3	DT3".split("\t")
df = pd.read_excel(path,names=None,header=0)
min_list = []
for sn in sample:
    seriessub = df[df[sn]>0].loc[:,sn]
    min_ = min(seriessub)
    min_list.append(min_)
print(min_list)
print("half of min is {min}".format(min=min(min_list)/2))