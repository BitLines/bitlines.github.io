---
layout:     post
title:      Dropout 介绍
subtitle:   'A Simple Way to Prevent Neural Networks from Overfitting'
date:       2017-03-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 模型正则化
    - 机器学习
---

# Dropout 介绍

Dropout 论文名 Dropout: A Simple Way to Prevent Neural Networks from Overfitting，有人说是一种模型调参的Trick，也有人认为是一种集成（emsemble）学习手段，还有人说是一种模型正则化方法。  
论文地址： https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf

## Dropout 简介

在机器学习的模型中，如果模型的参数太多，而训练样本又太少，训练出来的模型很容易产生过拟合的现象。过拟合具体表现在：模型在训练数据上预测准确率较高；但是在测试数据上预测准确率较低。

机器学习炼丹大法很多都是在过拟合和欠拟合之间不断对撞。一个简单的防止过拟合的方法就是简单的多模型投票机制，让三个臭皮匠顶一个诸葛亮。 Dropout 可以看作是一种多模型投票方法。 Dropout可以比较有效的缓解过拟合的发生，在一定程度上达到正则化的效果。 有些人把Dropout看做一种调参的Trick，而有些人觉得是一个很巧的理论方法，这就仁者见仁智者见智了。

Dropout 的作用机制很简答，在训练阶段，让神经网络的隐藏层单元独立的以 $1-p$的概率不工作（输出设置为0），然后让其他工作的神经元输出倍乘 $1/p$，在反向传播的时候那些不工作的隐藏层单元同样不回传梯度。这样在训练阶段的每个batch中，相当于神经网络的一个子网络在起作用。有点像我们在每个 Batch 中从大的神经网络中抽样出一个子网络，然后使用子网络进行学习。 在预测阶段，所有隐藏层单元都在工作，相当于所有子网络做了平均一样。

过程见下图  
![image](https://user-images.githubusercontent.com/80689631/112283041-ada8d880-8cc2-11eb-9c40-95d9e8027fe6.png)

## Dropout 工作流程

其实在代码实现的时候，dropout 的实现类似于一种特殊的激活函数。每个隐藏单元以概率 $1-p$ 输出为0，以概率 $p$ 输出 $x/p$，就像下面的图一样。

![image](https://user-images.githubusercontent.com/80689631/112283170-d16c1e80-8cc2-11eb-8d69-3e963e880003.png)

那形式化的描述原文给的是这样的：

![image](https://user-images.githubusercontent.com/80689631/112283500-2d36a780-8cc3-11eb-974b-5dfb0c4a80e0.png)  
![image](https://user-images.githubusercontent.com/80689631/112283520-3162c500-8cc3-11eb-934d-f8bf582f4f0b.png)

## 实验

论文建议 dropout 概率 $p$ 的取值在输入层接近 1，在隐藏层介于 0.5 到 1 之间。

实验结果非常Nice，直贴一个图意思意思吧  
![image](https://user-images.githubusercontent.com/80689631/112284266-062ca580-8cc4-11eb-96d7-c662b45d0152.png)

## 为什么 Dropout 起作用？
以下是我个人见解  
1. **一种隐式的多模型 emsemble 方法：** 在训练阶段的每个batch中，dropout的机制是从大的神经网络中抽样出一个子网络，然后使用子网络进行学习，在预测阶段所有子网络取平均来输出，是一种隐式的多模型集成方案。
2. **一种特殊的数据增强方法：** 如果把输入层做了dropout，相当于在样本中加入了一定的噪声干扰，相当于数据增强方法。
3. **降低网络同层神经元之间的共适应关系：**  因为dropout程序导致两个神经元不一定每次都在一个dropout网络中出现。这样权值的更新不再依赖于有固定关系的隐含节点的共同作用，阻止了某些特征仅仅在其它特定特征下才有效果的情况 。
