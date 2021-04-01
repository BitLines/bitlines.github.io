---
layout:     post
title:      Mean Teacher 介绍
subtitle:   'Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results'
date:       2020-03-22
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 半监督学习
    - 模型正则化
---

# Mean Teacher 介绍

Mean Teacher 论文名 Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results，是一种使用知识蒸馏技术的半监督学习方法。  
论文原文地址： https://arxiv.org/pdf/1703.01780.pdf

## Mean Teacher 简介

Mean Teacher 是一种半监督学习方法，是在方法 $\Pi$-Model 和 Temporal Ensembling 之上做了一些改进。 $\Pi$-Model 和 Temporal Ensembling 方法都是用了单个模型，而 Mean Teacher 是用了两个模型。 Teacher 的学习方法是参数进行动量更新。Student 则是普通的学习方式。

### 回顾 $\Pi$-Model 和 Temporal Ensembling
我们来先回顾一下 $\Pi$-Model 和 Temporal Ensembling。
- $\Pi$-Model 对一个 Batch 的数据做两次不同数据增强（例如两次不同的噪声），然后把两次不同数据增强后结果分别输入到同一个模型中，最终的损失函数对于有类标的样本是一个数据增强和类标的交叉熵，另一个是两个数据增强输出的最小二乘损失，对于无类标样本是两个数据增强输出的最小二乘损失。
- Temporal Ensembling 和 $\Pi$-Model 基本上是一样的，区别在于一个样本在一个epoch中只需要进行一次数据增强即可。Temporal Ensembling 为每个样本设置了一个记忆单元，用动量更新的方法记忆历史学习过程中的概率分布。最终的损失函数对于有类标的样本是一个和类标的交叉熵，另一个是和记忆单元的最小二乘损失，对于无类标样本是和记忆单元的最小二乘损失。

过程如下图  
![image](https://user-images.githubusercontent.com/80689631/112275288-6cacc600-8cba-11eb-88dc-567e09e7dafa.png)

### Mean Teacher
在 Mean Teacher 这篇论文中，加入了知识蒸馏中 Teacher 和 Student 的概念来解释其方法。这里面的 Student 表示直接和正确类标计算交叉熵的一组数据增强输入，另外一组只计算最小二乘损失的数据增强输入为 Teacher（因为 Teacher 不再从原始输入中学习了嘛）。 在 Temporal Ensembling 方法中，对每个样本使用一个记忆单元来记忆 Teacher 在历史的 epoch 中的分类行为，Student 模型学习的目标一个是正确类标，另一个则是历史的Teacher们。在 Mean Teacher 方法中，不再是使用一个模型，而是采用两个模型了。Student 的学习目标一个是正确类标的交叉熵，另外一个是和Teacher输出的最小二乘损失。而Teacher的更新方法是把 Student 的全部参数拿过来进行指数动量平均 EMA (exponential moving average)，结构图如下  
![image](https://user-images.githubusercontent.com/80689631/112303564-611bc800-8cd7-11eb-8135-bea3845d5d9c.png)


形式化描述，Student 和 Teacher 的损失函数为：

$$
J(\theta)=\mathbb{E}_{x,\eta,\eta'}[||f(x,\theta',\eta')-f(x,\theta,\eta)||^2]
$$

其中 $\theta$和$\theta'$分别是 Student 和 Teacher 的模型参数，$\eta$和$\eta'$分别是 Student 和 Teacher 的噪声扰动，Teacher 模型参数的更新方法是

$$
\theta_t'=\alpha\theta_{t-1}'+(1-\alpha)\theta_t
$$


## 实验结果

参数设置
- $\alpha$ 开始为0，前80个epoch采用 ramp up 到其最后的值，实验把其作为超参尝试了很多。

实验结果  
![image](https://user-images.githubusercontent.com/80689631/112307199-a04c1800-8cdb-11eb-9251-bdf0f572f686.png)
