---
layout:     post
title:      HDBSCAN 简介
subtitle:   一种基于密度的聚类方法
date:       2021-03-20
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
mathjax: true
tags:
    - 聚类算法
    - 机器学习
---

# HDBSCAN 简介
HDBSCAN 全称 (Hierachical Density-Based Spatial Clustering of Applications with Noise)， 不严谨的说，是DBSCAN 的升级版（多了一个H嘛），H 代表 hierachical （层次的）。如果在看 HDBSCAN 之前还不了解DBSCAN，那得去补课了。

## 核心距离和相互可达距离
为了理解 HDBSCAN 我们需要了解两个新定义：
- **核心距离(core distance)：**  $core_k(x)$ 定义为距离点第近的点到点的距离。
- **相互可达距离(mutual reachability distance)：** $d_{mreach-k}(a,b)=max\{core_k(a), core_k(b),d(a,b)\}$,其中 $d(a,b)$ 表示点$a$和点$b$的原始距离（如欧式距离，余弦距离等）。

让我们借助下图来理解一下上面两个概念：

![image](https://user-images.githubusercontent.com/80689631/113087340-ffe37f80-9215-11eb-9061-0a318c37da07.png)

图中，核心距离的参数k为6，蓝色圈圈、红色圈圈和绿色圈圈分别是蓝点、红点和绿点的核心距离所覆盖的范围。蓝点和绿点的相互可达距离$d_{mreach-k}($<font color='lightblue'>●</font>,<font color='green'>●</font>$)$=$max\{core_k($<font color='green'>●</font>$), core_k($<font color='lightblue'>●</font>$), d($<font color='lightblue'>●</font>$,$<font color='green'>●</font>$)\}$,=$core_k($<font color='lightblue'>●</font>$)$。

如果 $d_{mreach-MinPts}(a, b) \le \epsilon$，那么点 $a$ 和点 $a$ 都是核心对象，且点 $a$ 和点 $b$ 相互密度直达。

## 重新认识 DBSCAN

细化讲 HDBSCAN 之前，先用新的定义，重新review一下DBSCAN： 
1. 取参数 k 为MinPts，计算相互可达距离邻接矩阵；
2. 删除图中所有长度大于 eps 的边；
3. 求解图的所有最大连通区域，每个最大连通区域为一个聚类类别。

## 最小生成树
借助最小生成树，可以很简单来完成 DBSCAN：先生成一棵最小生成树，然后删除大于 eps 的边，就得到了聚类结果。  
![image](https://user-images.githubusercontent.com/80689631/113087353-083bba80-9216-11eb-8d52-b1ec4ecfae60.png)

再看 HDBSCAN。HDBSCAN 设计的初衷是想要支持不同密度的类簇。DBSCAN在聚类前，需要确定2个参数 MinPts 和 eps ，即确定核心对象的超球体半径和近邻数量。 eps 是一个很不直观的参数，如果不事先观察和分析数据分布，参数 eps 可能难以调节。 而 HDBSCAN 舍弃了 eps 参数，采用新参数 min_cluster_size，这个参数可以理解为 我期望的类簇的最小尺寸是多少？ 怎么样，这个参数简直就是陈独秀！这个参数让你不用事先观察数据分布，只要设置你期望的最小类簇大小即可。 比如，你认为一个标准问题被问了多少次希望被你挖掘出来！太6了。

回到上面的最小生成树。拆解最小生成树的时候，有个暧昧的地方是，删除哪些边，留下哪些边，删除边的标准是什么？这一点，在DBSCAN中是确定的，就选择  eps 作为阈值，大于 eps 的所有边都将删除，而这点在HDBSCAN中却是不同的，这也就是我觉得 HDBSCAN 和 DBSCAN 的根本区别。

最小生成树只是一个没有环的图，这是不行的，我们要把其转化成一个真正的树才能继续计算，产出的树要满足从根节点到任意叶节点路径上的边的长度是递减的！ 这个树的生成过程为：
1. 首先删除最小生成树中所有的边，使所有的点孤立
2. 按照最小生成树的边由小到大，逐次把边加入到树中，每次合并两棵子树，直到最后1条边加入进来把所有点连通。

通过上面的过程产出的树如下图：  
![image](https://user-images.githubusercontent.com/80689631/113087387-1689d680-9216-11eb-8726-0454a696221e.png)

此图，左边坐标是距离，右边坐标是点的数量。

再来看DBSCAN，DBSCAN取某个距离 eps 作为阈值，在图中水平画一条线，保留了水平线之下的子树结构。

## 最小生成树子树提取
HDBSCAN,为了进一步把删除边的范围缩小，可以进一步通过参数min_cluster_size把树化简。我们从上面的这个图中， 自上而下逐个边遍历，每条边视作一个候选切分，在每个切分处，如下做：
1. 如果在此处切分后生成的两棵子树中，存在一棵子树的节点数量小于min_cluster_size，则把这棵子树中的所有点定义为“聚类之外的点(points falling out of a cluster)”，同时把另一个较大的子树标记为父亲的ID。
2. 如果在此处切分后生成的两棵子树的节点数量都大于min_cluster_size，那么把这个候选切分视为一个真正的切分，并保留这个切分。

把所有ID相同的切分合并在一起，可以把上图转化成下面这幅图。  
![image](https://user-images.githubusercontent.com/80689631/113087440-302b1e00-9216-11eb-87df-28495fc1ec46.png)

最后一步就是如何从这个图中选择合适的类簇。说到类簇抽取这一部分，估计是最不直观的地方了。首先引入一个保持变量$\lambda = \frac{1}{dinstance}$，其实就是相互可达距离的反比函数。给定一个类簇，$\lambda _{birth}$  定义为类簇被父类簇切分所生成时，切分边的λ值；$\lambda_{death}$定义为类簇被切分生成子类簇时，切分边的λ。对于每个点p，定义为当点p成为聚类之外的点时，切分边的λ值。进而我们可以定义每个类簇的稳定性(stability):

$$\sum_{p \in cluster}(\lambda_p - \lambda_{birth})$$

一个类簇的稳定性越大，其在图中的表现为面积越大。于是我们期望选择的聚类其实就是希望稳定性越大越好。最简单的选择类簇是否被切分的标准就是，把当前类簇的稳定性和将要切分成的子类簇的稳定性的和进行比较，如果大则不切分，反之需要切分。


自底向上遍历化简树，
1. 如果子树稳定性的和大于当前树的稳定性，则把当前树的稳定性的值设置为子树稳定性的和；
2. 反之，把当前树选择为类簇，并从已选择的类簇中删除其所有子孙。

通过这种方法，最终选择出的聚类类簇如下图。  
 ![image](https://user-images.githubusercontent.com/80689631/113087430-2dc8c400-9216-11eb-9580-6f16c484718d.png)

## 牛刀小试

```Python
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from hdbscan import HDBSCAN

# 数据集构造，两个环形
X1, y1 = datasets.make_circles(n_samples=5000, factor=.6, noise=.05)
X2, y2 = datasets.make_blobs(n_samples=1000, n_features=2, centers=[[1.2, 1.2]], cluster_std=[[.1]], random_state=9)

X = np.concatenate((X1, X2))
plt.scatter(X[:, 0], X[:, 1], marker='o')
plt.show()

# 使用 HDBSCAN 聚类
y_pred = HDBSCAN(min_cluster_size=10, min_samples=5, alpha=1.0).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.show()
```
