# -*- coding: utf-8 -*-
# 参见 http://blog.csdn.net/xieyan0811/article/details/78581974

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 用feature把dataSet按value分成两个子集
def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[np.nonzero(dataSet[:,feature] > value)[0],:]
    mat1 = dataSet[np.nonzero(dataSet[:,feature] <= value)[0],:]
    return mat0,mat1

# 求给定数据集的线性方程
def linearSolve(dataSet):
    m,n = np.shape(dataSet)
    X = np.mat(np.ones((m,n))); # 第一行补1，线性拟合要求
    Y = np.mat(np.ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1];
    Y = dataSet[:,-1] # 数据最后一列是y
    xTx = X.T*X
    if np.linalg.det(xTx) == 0.0:
        raise NameError('This matrix is singular, cannot do inverse,\n\
        try increasing dur')
    ws = xTx.I * (X.T * Y) # 公式推导较难理解
    return ws,X,Y

# 求线性方程的参数
def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

# 预测值和y的方差
def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(np.power(Y - yHat,2))

def chooseBestSplit(dataSet, rate, dur):
    # 判断所有样本是否为同一分类
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return None, modelLeaf(dataSet)
    m,n = np.shape(dataSet)
    S = modelErr(dataSet) # 整体误差
    bestS = np.inf
    bestIndex = 0
    bestValue = 0
    for featIndex in range(n-1): # 遍历所有特征, 此处只有一个
        # 遍历特征中每种取值
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (np.shape(mat0)[0] < dur) or (np.shape(mat1)[0] < dur):
                continue # 样本数太少, 前剪枝
            newS = modelErr(mat0) + modelErr(mat1) # 计算整体误差
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < rate: # 如差误差下降得太少，则不切分
        return None, modelLeaf(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    return bestIndex,bestValue

def isTree(obj):
    return (type(obj).__name__=='dict')

# 预测函数,数据乘模型,模型是斜率和截距的矩阵
def modelTreeEval(model, inDat):
    n = np.shape(inDat)[1]
    X = np.mat(np.ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

# 预测函数
def treeForeCast(tree, inData):
    if not isTree(tree):
        return modelTreeEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'], inData)
        else:
            return modelTreeEval(tree['left'], inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'], inData)
        else:
            return modelTreeEval(tree['right'], inData)

# 对测试数据集预测一系列结果, 用于做图
def createForeCast(tree, testData):
    m=len(testData)
    yHat = np.mat(np.zeros((m,1)))
    for i in range(m): # m是item个数
        yHat[i,0] = treeForeCast(tree, np.mat(testData[i]))
    return yHat

# 绘图
def draw(dataSet, tree):
    plt.figure(figsize=[15,10]) # 改变画布大小
    plt.scatter(dataSet[:,0], dataSet[:,1], s=5) # 在图中以点画收盘价
    yHat = createForeCast(tree, dataSet[:,0])
    plt.plot(dataSet[:,0], yHat, linewidth=2.0, color='red')
    plt.show()

# 生成回归树, dataSet是数据, rate是误差下降, dur是叶节点的最小样本数
def createTree(dataSet, rate, dur):
    # 寻找最佳划分点, feat为切分点, val为值
    feat, val = chooseBestSplit(dataSet, rate, dur)
    if feat == None:
        return val # 不再可分
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val) # 把数据切给左右两树
    retTree['left'] = createTree(lSet, rate, dur)
    retTree['right'] = createTree(rSet, rate, dur)
    return retTree

if __name__ == '__main__':
#    df = ts.get_k_data(code = '002230', start = '2017-01-01') # 科大讯飞今年的股票数据
    df = ts.get_k_data(code = '300344', start = '2016-01-01') # 太空板业的股票数据
    e = pd.DataFrame()
    e['idx'] = df.index # 用索引号保证顺序X轴
    e['close'] = df['close'] # 用收盘价作为分类标准Y轴, 以Y轴高低划分X成段，并分段拟合
    arr = np.array(e)
    tree = createTree(np.mat(arr), 100, 10)
    draw(arr, tree)


