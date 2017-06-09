#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2017/6/6 22:33
# @Author  : dmwuyi
# @Github  : https://github.com/dmwuyi
# @File    : util.py
# @Description :

def set_chinese():
	from pylab import mpl
	mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
	mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题