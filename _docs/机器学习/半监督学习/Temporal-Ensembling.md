---
layout:     post
title:      Temporal Ensembling 介绍
subtitle:   'TEMPORAL ENSEMBLING FOR SEMI-SUPERVISED LEARNING'
date:       2020-03-22
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 半监督学习
    - 模型正则化
---

# Temporal Ensembling 介绍

Temporal Ensembling 论文名 TEMPORAL ENSEMBLING FOR SEMI-SUPERVISED LEARNING，是一种使用知识蒸馏技术的半监督学习方法。  
论文原文地址： https://arxiv.org/pdf/1610.02242.pdf

## Temporal Ensembling 简介

在机器学习领域中已经被证实的一个经验是多个模型的 ensemble 决策会提升模型效果。 一些隐式的 ensemble 方法也是有效的，例如 Dropout, Dropconnect, Stochastic depth 等。 本论文提出来 两个方法 $\Pi$-Model 和 Temporal Ensembling 来提升半监督学习的效果。 这个方法的优势在于方法是模型无关的（可以是任何模型）， 通过数据增强和类标对齐等方法来在时序上做模型融合。两个方法整体见下图。

![image](https://user-images.githubusercontent.com/80689631/112275288-6cacc600-8cba-11eb-88dc-567e09e7dafa.png)


## 详细介绍

$\Pi$-Model 和 Temporal Ensembling 都用到了数据增强方法。数据增强方法文中介绍了2种
- 网络输入层加入高斯白噪声
- 利用机器翻译+反向翻译


### $\Pi$-Model

$\Pi$-Model 其实很简单，在一个数据 Batch 中，先对输入数据做两次数据增强，然后把两次不同数据增强的得到的结果分别输入到同一个模型中，最终的损失函数对于有类标的样本是，一个数据增强和类标的交叉熵，另一个是两个数据增强输出的最小二乘损失，对于无类标样本是两个数据增强输出的最小二乘损失。 
具体如下

![image](https://user-images.githubusercontent.com/80689631/112275311-720a1080-8cba-11eb-81bc-dff2f77991f4.png)


### Temporal Ensembling

Temporal Ensembling 和 $\Pi$-Model 基本上是一样的，区别在于一个样本在一个epoch中只需要进行一次数据增强即可。Temporal Ensembling 为每个样本设置了一个记忆单元，用动量更新的方法记忆历史学习过程中的概率分布。最终的损失函数对于有类标的样本是一个和类标的交叉熵，另一个是和记忆单元的最小二乘损失，对于无类标样本是和记忆单元的最小二乘损失。

![image](https://user-images.githubusercontent.com/80689631/112275331-78988800-8cba-11eb-8a14-7ea0002907ea.png)

可以看到与 $\Pi$-Model 不同的是， Temporal Ensembling用一个大矩阵 $Z$ 来记录每个样本的一个输出。Z 是通过 EMA（exponential moving average） 方法更新的。

## 实验结果

参数设置
- temporal ensembling $\alpha = 0.6$
- w(t) ramps up, starting from zero, along a Gaussian curve during the first 80 training epochs.


实验结果如下图  
![image](https://user-images.githubusercontent.com/80689631/112278128-7a177f80-8cbd-11eb-8d7f-c51cdeef3a02.png)

## 其他参考 

1. Dropout: https://www.jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf
2. Dropconnect: http://proceedings.mlr.press/v28/wan13.pdf
3. Stochastic depth: https://arxiv.org/pdf/1603.09382
