from time import sleep
import SHSZStockCode
import treeForeCast
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 获取股票代码
stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
output_file = 'BaiduStockInfo.txt'
slist=[]
SHSZStockCode.getStockList(slist, stock_list_url)

rightCode=[]
falseCode=[]
kickpoint=[]
ri=0
fii=0
kii=0
for st in slist:
    if st[:3] not in {'sh2', 'sh5', 'sh9',  'sz1', 'sz2'}:
        df = ts.get_k_data(code = st, start = '2017-01-01') # 获取股票数据
        if len(df) > 0:
            # 股票有数据
            e = pd.DataFrame()
            e['idx'] = df.index # 用索引号保证顺序X轴
            e['close'] = df['close'] # 用收盘价作为分类标准Y轴, 以Y轴高低划分X成段，并分段拟合
            arr = np.array(e)
            tree = treeForeCast.createTree(np.mat(arr), 100, 10)
            yHat = treeForeCast.createForeCast(tree, arr[:,0])
            d=yHat[-3:]
            if d[1]<= d[2]:
                rightCode.append(st)
                ri+=1
                if d[1]< d[0]:
                    # 转折点
                    kickpoint.append(st)
                    kii+=1
            else:
                falseCode.append(st)
                fii+=1
            print(ri, fii, kii, st)
            #sleep(0.5)
