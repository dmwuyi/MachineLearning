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

    def createTree(self, dataSet):
        classList = [da[-1] for da in dataSet]
        if classList.count(classList[0]) == len(classList):  #此时数据中只剩下一个类别  无需划分
            return classList[0]
        if len(dataSet[0]) == 1:  # 此时 所有特征处理完毕，只剩下最后的标签信息
            return self.majorityCnt(classList)

        return 0


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
    print( dt.calcEntropy(createDataSet()[0]))
    print( dt.chooseBestFeatureToSplit(createDataSet()[0]))

















