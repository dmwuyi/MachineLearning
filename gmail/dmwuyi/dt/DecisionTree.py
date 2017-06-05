#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2017/6/5 22:23
# @Author  : dmwuyi
# @Github  : https://github.com/dmwuyi
# @File    : DecisionTree.py
# @Description : 决策树构造流程如下：
'''
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

    def __init__(self, iterCnt):
        self.iterCnt = iterCnt