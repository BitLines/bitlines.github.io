## DBSCAN 简介
DBSCAN（英文全称 Density-Based Spatial Clustering of Applications with Noise，具有噪声的基于密度的聚类方法）的聚类过程可以用数学的传递闭包来说明。很多同学都忘记了。忘记也没关系，因为他和 K-Means 一样的简单！接下来我们直接来看 DBSCAN 就好了，不再举一些生动的例子了，直接硬撸一些定义。  
DBSCAN 有两个核心的参数：eps 和 MinPts。eps 是球半径，MinPts 是最小邻居数量。

> e-邻域：以样本为中心，eps为半径的球内区域。  
> 核心对象：e-邻域内的样本点数量不小于MinPts个的样本点。  
> 密度直达：点 p1 是核心对象，如果点 p2 在 p1 的e-邻域内，则称 p2 由 p1 密度直达。  
> 密度可达：对于点p1 和p2，如果存在一个序列使 p1, x1, x2, ..., p2 相邻的密度直达，则 p2 可由 p1 密度可达。  

那最后，问题就是寻找密度可达的传递闭包。看下面这个图:  
![image](https://user-images.githubusercontent.com/80689631/111164810-5d9e8780-85d9-11eb-9cf9-047bb549fcbc.png)  
从上图看来，DBSCAN 聚类过程为（不严禁的来讲）：
> 1) 找出1个未归类的核心对象，然后把所有未归类且由该核心对象密度可达的对象与该核心对象归为1类。
> 2) 重复步骤1)，直到不存在任何核心对象为止。此时剩下未归类的对象就是散点或者叫噪声。


更生动的例子，可以去国外大神的网站看看 https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/


```Python
# 这里给大家演示一个使用 sklearn 包中的 DBSCAN 的例子。
# 先安装相关的 pip 包 ``pip install sklearn matplotlib numpy``

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import DBSCAN

# 数据集构造，两个环形
X1, y1 = datasets.make_circles(n_samples=5000, factor=.6, noise=.05)
X2, y2 = datasets.make_blobs(n_samples=1000, n_features=2, centers=[[1.2, 1.2]], cluster_std=[[.1]], random_state=9)

X = np.concatenate((X1, X2))
plt.scatter(X[:, 0], X[:, 1], marker='o')
plt.show()

# 使用 DBSCAN 聚类
y_pred = DBSCAN(eps=0.1, min_samples=10).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.show()
```

运行效果如下图  
![image](https://user-images.githubusercontent.com/80689631/111164480-157f6500-85d9-11eb-884c-280a84eaf754.png)
