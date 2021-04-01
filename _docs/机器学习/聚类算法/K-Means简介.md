---
layout:     post
title:      K-Means 简介
subtitle:   一种基于质心的聚类方法
date:       2021-03-02
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 聚类算法
---

# K-Means 简介

K-Means 是非常简单，但是非常强力是聚类算法。K-Means 运行速度极快，很容易支持用于分布式系统(map-reduce)和大规模数据聚类。

## 牧师-村民问题
了解 K-Means之前，先看一个有趣的问题：牧师-村民问题。

牧师-村民问题：说有4个牧师想要给村庄中的所有村民讲课。4个牧师分别在村庄选择一个位置，村民自行就近寻找牧师听课。求问4个牧师如何选择授课位置，使村民平均行走距离最小。这就是 k-means 问题：在空间中寻找 k 个聚类中心点，使所有样本到达各自最近聚类中心点的距离之和最小。

> 求解这个问题之前，再问大家另一个有意思的问题。一个鞭炮在地面爆炸，以爆竹位置为坐标轴0点，求爆竹纸片落地的概率分布。这个问题直接用数学公式计算是非常困难的，原因是要考虑的因素非常多，物理系统也很复杂。但是实际上可以直接买100个鞭炮（虽然有点贵），做引爆实验后进行数据测量和统计。
> 很多算法问题的求解也不是直接“硬”去计算，也经常采用采样算法和梯度下降等手段求解。

回归到牧师-村名问题，其中一种求解方法也不是直接计算，而是在最开始的时候让4个牧师随机找个位置授课（通常是各选取一个村民的位置），再逐步迭代求解的。我们以**魔兽世界**中奥格瑞玛地图举例。具体步骤：

step 1. 4个牧师首选随机选择4个地方授课（图中为1 2 3 4个黄点）  
![image](https://user-images.githubusercontent.com/80689631/111160872-7e64de00-85d5-11eb-9fa1-71664aeac5d7.png)

step 2. 村民就近选择牧师听课，4个牧师可以把空间划分为4个部分。然后牧师收集每个村民的家庭位置，计算位置质心，重新决定下一次授课位置，新位置为图中绿色的点。  
![image](https://user-images.githubusercontent.com/80689631/111160928-8b81cd00-85d5-11eb-8acb-3f834b0b7671.png)

更加直观的例子：https://www.naftaliharris.com/blog/visualizing-k-means-clustering/

回归到 K-means，其算法步骤可以描述为：
> 1. 选择初始化的 $k$ 个样本作为初始聚类中心  ；
> 2. 针对数据集中每个样本 $p$ 计算它到 $k$ 个聚类中心的距离并将其分到距离最小的聚类中心所对应的类中；
> 3. 针对每个类别 $c$，重新计算它的聚类中心 $c'$（即属于该类的所有样本的质心）；
> 4. 重复上面 2 3 两个步骤，直到达到某个中止条件（迭代次数、最小误差变化等）。


```Python
# 这里给大家演示一个使用 sklearn 包中的 K-Means 的例子。
# 先安装相关的 pip 包 ``pip install sklearn matplotlib numpy``

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

# 数据集构造，两个环形
X1, y1 = datasets.make_circles(n_samples=5000, factor=.6, noise=.05)
X2, y2 = datasets.make_blobs(n_samples=1000, n_features=2, centers=[[1.2, 1.2]], cluster_std=[[.1]], random_state=9)

X = np.concatenate((X1, X2))
plt.scatter(X[:, 0], X[:, 1], marker='o')
plt.show()

# 使用 k-means 聚类
y_pred = KMeans(n_clusters=3).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.show()
```

运行效果如下图  
![image](https://user-images.githubusercontent.com/80689631/112314012-7ac30c80-8ce3-11eb-908f-2b131abe0455.png)