---
layout:     post
title:      Boostring 介绍
subtitle:   '提升方法，包括AdaBoost/GBDT/XGBoost等'
date:       2017-06-10
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 集成学习
---

## Boostring 简介

Boosting是一种提高任意给定学习算法准确度的方法。

很赞的原因学习资料可以参考：<http://www.machine-learning.martinsewell.com/ensembles/boosting/FreundSchapire1996.pdf>

Boosting 的提出与发展离不开Valiant和 Kearns两位大牛的不懈努力。 两位大佬最早提出了强学习器和弱学习器的概念：
- 弱学习器：识别错误率小于1/2（即准确率仅比随机猜测略高的学习算法）
- 强学习器：识别准确率很高并能在多项式时间内完成的学习算法

Boosting 算法是一种把若干个弱学习器整合为一个强学习器的方法，也就是一种集成学习方法（Ensemble Method）。比较简单的集成分类方法在 Boosting 之前出现过 Boostrapping 和 Bagging 方法。

### AdaBoost (Adaptive Boosting)算法

AdaBoost 通过改变样本的分布突出错分类（通过样本的权重来改变分布），并进而训练弱分类器得到弱分类器的权重，最终根据权重整合在一起得到最终的强分类器。

AdaBoost方法大致有：Discrete Adaboost， Real AdaBoost，LogitBoost 和 Gentle AdaBoost等。所有的方法训练的框架的都是相似的。

#### Discrete Adaboost
通常使用最多的应该是Discrete AdaBoost（离散的AdaBoost）即AdaBoost.M1算法，主要因为它的简单却不俗的表现。原文中的伪代码

![image](https://user-images.githubusercontent.com/80689631/115214166-d17e0380-a134-11eb-948c-b59d9343df2c.png)

在 AdaBoost.M1 算法迭代的过程中，会产生出一系列的误差值 $\epsilon_1,...,\epsilon_T$，如果 $\epsilon_t \le 1/2$，令 $\gamma_t = 1/2 - \epsilon_t$，那么 $h_{fin}$ 最终分类误差的上届满足：

$$
\frac{1}{m}|\{i:h_{fin}(x_i) \ne y\}| \le \prod_{t=1}^{T}\sqrt{1-4\gamma_t^2} \le \exp(-2\sum_{t=1}^T\gamma_t^2)
$$

该理论表明，只要AdaBoost.M1中的弱分类器的错误率略低于1/2，那么最终分类器中的分类错误数就将以指数速度下降至0。但是 AdaBoost 却不能处理 $\epsilon_t \gt 1/2$ 的情况，也就是说弱分类器如果错误率大于1/2，AdaBoost将会失效。


#### Real Adaboost

Discrete AdaBoost 的每一个弱分类器的输出结都是单个的类标，并没有属于某个类的概率，略显粗糙。
而且 Adaboost.M1 算法要求错误率 $\epsilon_t \le 1/2$ 其实并不很好控制。我们知道随机猜测时的分类错误率为 $1−\frac{1}{k}$ ，其中k为类别数。因此k=2即二分类问题时，我们仅需要弱分类器比随机猜测的结果略好即可。但是当k>2即面对多分类问题时，这个条件就显得有点苛刻了。
为了解决这两个问题，Freund 和 Schapire 在 AdaBoost.M1 的基础上提出了泛化的 AdaBoost.M2 即 Real Adaboost 算法。
原文中的伪代码如下

![image](https://user-images.githubusercontent.com/80689631/115214328-fa05fd80-a134-11eb-9824-b62b5049ab82.png)


### GBDT

另一种boosting方法GBDT(Gradient Boost Decision Tree)，则与AdaBoost不同，GBDT每一次的计算是都为了减少上一次的残差，进而在残差减少（负梯度）的方向上建立一个新的模型。

boosting集成学习由多个相关联的决策树联合决策，什么叫相关联？举个例子

有一个样本[数据->标签]是：[(2，4，5)-> 4]
第一棵决策树用这个样本训练的预测为3.3
那么第二棵决策树训练时的输入，这个样本就变成了：[(2，4，5)-> 0.7]
也就是说，下一棵决策树输入样本会与前面决策树的训练和预测相关
很快你会意识到，Xgboost为何也是一个boosting的集成学习了。

而一个回归树形成的关键点在于：

分裂点依据什么来划分（如前面说的均方误差最小，loss）；
分类后的节点预测值是多少（如前面说，有一种是将叶子节点下各样本实际值得均值作为叶子节点预测误差，或者计算所得）
至于另一类集成学习方法，比如Random Forest（随机森林）算法，各个决策树是独立的、每个决策树在样本堆里随机选一批样本，随机选一批特征进行独立训练，各个决策树之间没有啥关系。本文暂不展开介绍。

说到Xgboost，不得不先从GBDT(Gradient Boosting Decision Tree)说起。而且前面说过，两者都是boosting方法（如图所示：Y = Y1 + Y2 + Y3）



## 参考文献
1. [Experiments with a New Boosting Algorithm](http://www.machine-learning.martinsewell.com/ensembles/boosting/FreundSchapire1996.pdf)

