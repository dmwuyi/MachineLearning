#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2017/6/5 22:23
# @Author  : dmwuyi
# @Github  : https://github.com/dmwuyi
# @File    : DecisionTree.py
# @Description : 决策树构造流程如下：
'''
def createBranch():
    检测数据集中的每个子项是否属于同一分类：
          If so return  类标签
          Else
                寻找划分数据集的最好特征
                划分数据集
                创建分支节点
                    for 每个划分的子集
                        调用函数createBranch并增加返回结果到分支节点中
                 return 分支节点
'''

class DecisionTree:

    def __init__(self, iterCnt = 50):
        self.iterCnt = iterCnt
        self.initPlt()

    def calcEntropy(self, dataSet):
        '''
        计算香农熵： 度量的是数据的有序程度，越高则越无序（混合数据越多）
        :param dataSet: 数据集  其中最后一列为标签信息
        :return: 香农熵
        '''
        n = len(dataSet)
        labelCount = {}
        for da in dataSet:
            curLabel = da[-1]
            if curLabel not in labelCount.keys():
                labelCount[curLabel] = 0
            labelCount[curLabel] += 1
        ent = 0.0
        from math import  log2
        for key in labelCount.keys():
            prob = float(labelCount[key]) / n
            ent -= prob* log2(prob)
        return ent

    def splitDataSetByAxis(self, dataSet, axis, value):
        '''
        按照给定位置的特征划分标准 将数据进行划分处理
        :param dataSet:
        :param axis: 需要划分的特征位置
        :param value: 特征划分标准
        :return:
        '''
        retDataSet = []
        for da in dataSet:
            if da[axis] == value:   # 只能处理离散值
                newDa = da[:axis]
                newDa.extend(da[axis+1:])
                retDataSet.append(newDa)
        return retDataSet

    def chooseBestFeatureToSplit(self, dataSet):
        numFeatures = len(dataSet[0]) - 1
        baseEnt = self.calcEntropy(dataSet)
        bestInfoGain = 0.0 # 存放最好的信息增益值
        bestFeature = -1
        for i in range(numFeatures):
            columnList = [tmp[i] for tmp in dataSet]
            columVauleSet = set(columnList)
            tmpEntropy = 0.0
            for value in columVauleSet:   # 统计出按照每个特征 按照某个元素划分的熵*权重
                subDataSet = self.splitDataSetByAxis(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                tmpEntropy += prob * self.calcEntropy(subDataSet)
            infoGain = baseEnt - tmpEntropy   # 注意熵越低越好，熵
            if infoGain> bestInfoGain:   # 信息增益越大越好
                bestInfoGain = infoGain
                bestFeature = i
        return bestFeature

    def majorityCnt(self, classList):
        '''
        当某些数据按照所有属性划分完毕后，叶子节点依然包含多种类别，此时采用投票表决来决定叶子节点的类别
        :param classList:  所有元素的类名
        :return: 占最多个数的类名
        '''
        classCnt = {}
        for vote in classList:
            if vote not in classCnt.values():
                classCnt[vote] = 0
            classCnt[vote] += 1
        # 排序
        import  operator   # 按照classCnt元素中的第二个值大小进行排序
        sortedClassCnt = sorted(classCnt.items(), key = operator.itemgetter(1),reverse= True)
        return sortedClassCnt[0][0]

    def createTree(self, dataSet, labels):
        '''
        创建简单决策树
        :param dataSet: 数据集
        :param labels: 标签集(特征集)
        :return: 构建的树
        '''
        classList = [da[-1] for da in dataSet]
        if classList.count(classList[0]) == len(classList):  #此时数据中只剩下一个类别  无需划分
            return classList[0]
        if len(dataSet[0]) == 1:  # 此时 所有特征处理完毕，只剩下最后的标签信息
            return self.majorityCnt(classList)
        bestFeature = self.chooseBestFeatureToSplit(dataSet)  # 通过信息增益选取最好特征进行划分
        bestFeatureLabel = labels[bestFeature]  # 获取最好特征的标签名
        tree = {bestFeatureLabel:{}}  # 创建树结构（字典的形式不断存放子节点信息）
        del(labels[bestFeature]) # 从当前特征集中删掉最好特征
        featValues = [da[bestFeature] for da in dataSet] # 最好特征中对应的所有可能值
        featValuesSet = set(featValues)
        for value in featValuesSet:   # 为特征中的每一个可能值构建一个子节点
            subLabels = labels[:]
            tree[bestFeatureLabel][value] = self.createTree(self.splitDataSetByAxis\
                                                (dataSet, bestFeature, value), subLabels)
        return tree

    def getNumLeafs(self, tree):
        '''
        计算决策树的叶子节点个数
        :param tree:
        :return:
        '''
        numLeafs = 0
        secondDict = tree[list(tree.keys())[0]]
        for key in secondDict.keys():
            if isinstance(secondDict[key], dict):
                numLeafs += self.getNumLeafs(secondDict[key])
            else:
                numLeafs += 1
        return numLeafs
    def getTreeDepth(self, tree):
        '''
        计算树的深度
        :param tree:
        :return:
        '''
        maxDepth = 0
        secondDict = tree[list(tree.keys())[0]]
        for key in secondDict.keys():
            thisDepth = 0
            if isinstance(secondDict[key], dict):
                thisDepth = 1+ self.getTreeDepth(secondDict[key])
            else:
                thisDepth += 1
            if thisDepth> maxDepth: maxDepth = thisDepth
        return maxDepth

#####################  绘图区代码  （绘图没学，直接拿书上的 后面补学） #####################
    def initPlt(self):
        import matplotlib.pyplot as plt
        self.decisionNode = dict(boxstyle="sawtooth", fc="0.8")
        self.leftNode = dict(boxstyle="round4", fc="0.8")
        self.arrow_args = dict(arrowstyle="<-")


    def plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        self.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                    xytext= centerPt, textcoords='axes fraction', va= "center",\
                    ha="center", bbox=nodeType, arrowprops=self.arrow_args)

    def plotMidText(self, subPt, parentPt, text): # 在父子节点间填充文本信息
        xMid = (parentPt[0] - subPt[0])/ 2.0 + subPt[0]
        yMid = (parentPt[1] - subPt[1])/ 2.0 + subPt[1]
        self.ax1.text(xMid, yMid, text)

    def plotTree(self, tree, parentPt, nodeTxt):
        numLeaf = self.getNumLeafs(tree)
        depth = self.getTreeDepth(tree)
        subPt = (self.xOff + (1.0 + float(numLeaf))/ 2.0/ self.totalW, \
                     self.yOff)
        self.plotMidText(subPt, parentPt, nodeTxt)
        self.plotNode(list(tree.keys())[0], subPt, parentPt, self.decisionNode)
        self.yOff = self.yOff - 1.0/ self.totalD
        secondDict = tree[list(tree.keys())[0]]
        for key in secondDict.keys():
            if isinstance(secondDict[key], dict):
                self.plotTree(secondDict[key], subPt, str(key))
            else:
                self.xOff = self.xOff + 1.0/ self.totalW
                self.plotNode(secondDict[key], (self.xOff, self.yOff), subPt, self.leftNode)
                self.plotMidText((self.xOff, self.yOff), subPt, str(key))
        self.yOff = self.yOff + 1.0/ self.totalD

    def createPlot(self, inTree):
        import matplotlib.pyplot as plt
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self.ax1 = plt.subplot(111, frameon=False, **axprops)
        self.totalW = float(self.getNumLeafs(inTree))
        self.totalD = float(self.getTreeDepth(inTree))
        self.xOff = -0.5/ self.totalW; self.yOff = 1.0
        self.plotTree(inTree, (0.5, 1.0), '')
        # 显示中文
        import dt.util as myutil
        myutil.set_chinese()

        plt.show()

#####################  绘图区代码结束  #####################

########## Test\Run #################
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels
if __name__ == '__main__':
    dt = DecisionTree()
    dataSet, labels = createDataSet()
    print( dt.calcEntropy(dataSet))
    print( dt.chooseBestFeatureToSplit(dataSet))
    tree = dt.createTree(dataSet, labels)
    print( tree)
    numLeafs = dt.getNumLeafs(tree)
    print('numLeafs: ', numLeafs)
    numDepth = dt.getTreeDepth(tree)
    print("numDepth: ", numDepth)
    dt.createPlot(tree)
















