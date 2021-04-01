---
layout:     post
title:      FGM 介绍
subtitle:   'ADVERSARIAL TRAINING METHODS FOR SEMI-SUPERVISED TEXT CLASSIFICATION'
date:       2020-03-23
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 对抗学习
    - 模型正则化
    - 自然语言处理
---

# FGM 介绍

FGM 全称 Fast Gradient Method，出自论文 ADVERSARIAL TRAINING METHODS FOR SEMI-SUPERVISED TEXT CLASSIFICATION，是FGSM的改进版本。如果看过FGSM，那改进点主要有两个：
1. 少了个字母S的意思是sign，噪声扰动在FGSM中是取了梯度在每个维度上的符号（-1,0,1），而FGM是取了梯度的单位向量
2. 除了标注数据之外，本文还提出了在未标注数据上的应用方法。在标注数据上训练取名对抗训练（Adversarial training），而在未标注数据上取名虚拟对抗训练（Virtual Adversarial training）

除此之外，FGM 应用于文本分类任务中，而FGSM是用于图像领域的方法。
如果没看过FGSM，也没关系下面详细讲一下。  
论文原文地址： https://arxiv.org/pdf/1605.07725.pdf

## FGM 简介

FGM 在做自然语言处理任务时，在词向量层给每个词的词向量加入一个随机的噪声扰动$r_{adv}$，使得最终模型分类结果对正确类别的概率下降。 $r_{adv}$ 这变量值的作用就是对模型进行攻击，在监督学习中让模型对正确的样本进行误判。在半监督学习中让模型输出的概率分布KL散度变大。

## 详细介绍

FGM 其实既可以用于自然语言处理领域，也可以用于图像领域，是一个通用方案。 但是论文中用于文本分类，选择的模型结构是LSTM，方法是在词向量层加入一个噪声向量。如下图所示。  
![image](https://user-images.githubusercontent.com/80689631/112860215-33bf8780-90e6-11eb-9336-9385607c5e15.png)

把噪声扰动向量直接加到词向量会出现一个问题，就是模型为了对抗噪声，会使词向量的模长越来越大（因为向量变长了，所以噪声相对来说叫小了），因此在词向量出要做一个正则化。论文中的方法是对输入向量进行了一个正态分布的处理，也就是对所有词向量求均值和协方差，再进行缩放。

$$
\bar{v}_k=\frac{v_k-E(v)}{\sqrt{Var(v)}},\textup{where} E(v)=\sum_{j=1}^{K}f_jv_j,Var(v)=\sum_{j=1}^{K}f_j(v_j-E(v))^2
$$

其中$f_j$为词j的频率。

### 对抗训练
对抗训练与 FGSM 基本相同，在输入向量 $x$ 上加入一个噪声扰动 $r_{adv}$ 使得加了噪声后，模型对正确类别的输出概率极小化，公式如下：

$$
-\log\ p(y|x+r_{adv};\theta),\textup{where}\ r_{adv}=\argmin_{r,||r||\le \epsilon} \log p(y|x+r;\hat{\theta})
$$

其中，$r$是噪声扰动，$\hat{\theta}$ 是当前模型参数取常数（在实现的时候其实就是把梯度去掉，pytorch是 with torch.no_gradient()），其实也就是说在求 $r_{adv}$时，应该把模型参数fix住不更新。这个公式其实就是对抗训练中的极小极大问题。极大步是找一个最大化让模型分类错误的噪声，极小化是让模型能正确分类加了噪声的样本。

与 FGSM 不同的是，对于噪声$r_{adv}$ 不再取梯度各维度的符号，而是取单位向量：

$$
r_{adv}=-\epsilon g/||g||_2, \textup{where}\ g=\bigtriangledown_x\textup{log}\ p(y|x;\hat{\theta})
$$

### 虚拟对抗训练
虚拟对抗训练是把对抗噪声的方法用于未标注的数据上，极大化学习的目标是早一个噪声扰动 $r_{v-adv}$使得模型输出的概率分布于原始自然输入的概率分布差异较大（KL散度），那对应的模型学习目标是：

$$
KL[p(\cdot|x;\theta)||p(\cdot|x+r_{v-adv};\hat{\theta})]
$$

$$
\textup{where}\ r_{v-adv}=\argmax_{r,||r||\le \epsilon}KL[p(\cdot|x;\hat{\theta})||p(\cdot|x+r_{v-adv};\hat{\theta})]
$$


## 实验结果

在IMDB情感分类数据集上，效果还不错，看下图

![image](https://user-images.githubusercontent.com/80689631/112857794-ca3e7980-90e3-11eb-8341-ac5e251be1f2.png)


## 后续小记

其实 FGM 还是有局限性的，称为单步对抗，也就是$r_{adv}$计算只迭代一次，一步到位使原始输入$x$偏移 $\epsilon$ 长度。后面的方法 PGM 在训练时求$r_{adv}$进行迭代多步，使模型找到的对抗样本鲁棒。