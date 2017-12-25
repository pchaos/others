from time import sleep
import SHSZStockCode

# 获取股票代码
stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
output_file = 'BaiduStockInfo.txt'
slist=[]
SHSZStockCode.getStockList(slist, stock_list_url)

for st in slist:
    if st[:3] not in {'sh2', 'sh5', 'sh9',  'sz1', 'sz2'}:
        df = ts.get_k_data(code = st, start = '2017-01-01') # 获取股票数据
        if len(df) > 0:
            # 股票有数据
            e = pd.DataFrame()
            e['idx'] = df.index # 用索引号保证顺序X轴
            e['close'] = df['close'] # 用收盘价作为分类标准Y轴, 以Y轴高低划分X成段，并分段拟合
            arr = np.array(e)
            tree = createTree(np.mat(arr), 100, 10)
            yHat = createForeCast(tree, arr[:,0])
            d=yHat[-2:]
            if d[0]<= d[1]:
                print(1)
            print(len(df), st)
            #sleep(0.5)
