---
layout:     post
title:      Label Smoothing 介绍
subtitle:   '超级简单的模型正则化方法，还不赶快炼丹试试'
date:       2017-03-05
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 模型正则化
    - 机器学习
---

# Label Smoothing 介绍

Label Smoothing 出自论文 Rethinking the Inception Architecture for Computer Vision，这论文虽然是做图像的，但是里面讲到了 Label Smoothing 方法。解决的问题是样本少，采用交叉熵作为损失函数带来的模型过拟合问题。

论文地址： https://arxiv.org/pdf/1512.00567.pdf

## 交叉熵的问题

分类模型大多数采用 softmax 计算每个类别的概率

$$
q_i=\frac{\exp(z_i)}{\sum_{j=1}^{K}\exp(z_j)}
$$

其中 $q_i$ 表示类别i的概率，$z_i$ 表示类别 i 的 logit 值，K 是类别数。

交叉熵计算损失函数公式为：

$$
L=-\sum_{i=1}^{K}p_i\log q_i
$$

其中 $p_i$ 是真实类别 i 的概率，实际中如果 i 是正确的类别，$p_i=1$，否则 $p_i=0$。

训练神经网络时，最小化预测概率和标签真实概率之间的交叉熵，从而得到最优的预测概率分布。而 softmax 在梯度下降更新的时候，会使 正确类标的概率 $q_i$ 无限接近于 1:

$$
z_i =\left\{
    \begin{aligned}
        & +\infty &,\ \textup{if}\ i=y \\
        & 0 &,\ \textup{if}\ i\ne y
    \end{aligned}
\right.
$$

这导致了 $z_i \rightarrow +\infty$。 都正无穷了，你说能不过拟合么？

## Label Smoothing

那怎么解决 $z_i \rightarrow +\infty$ 这种问题的发生呢？Label Smoothing 的做法是加入一个噪声 $\epsilon$，使正确样本的目标学习概率不再是1 ，而是 $1-\epsilon$。


$$
p_i =\left\{
    \begin{aligned}
        &1-\epsilon &,\ \textup{if}\ i=y \\
        &\frac{\epsilon}{K-1}\ &,\ \textup{if}\ i\ne y
    \end{aligned}
\right.
$$

那来看看 z 会有什么变化：

$$
z_i =\left\{
    \begin{aligned}
        & \log{\frac{(K-1)(1-\epsilon)}{\epsilon + \alpha}} &,\ \textup{if}\ i=y \\
        & \alpha &,\ \textup{if}\ i\ne y
    \end{aligned}
\right.
$$

实操中，论文中设置的参数 $\epsilon = 0.1$。 炼丹大师们搞起鸭。