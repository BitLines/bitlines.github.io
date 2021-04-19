---
layout:     post
title:      ALBERT 介绍
subtitle:   'A LITE BERT FOR SELF-SUPERVISED LEARNING OF LANGUAGE REPRESENTATIONS'
date:       2021-03-19
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# ALBERT 介绍
ALBERT 全称 A Lite BERT，出自论文 A LITE BERT FOR SELF-SUPERVISED LEARNING OF LANGUAGE REPRESENTATIONS，用于解决 BERT 参数过多导致内存占用高同时训练时间长的问题。

论文地址：<https://arxiv.org/pdf/1909.11942.pdf>

## ALBERT 简介
BERT-large 比 BERT-base 效果好这种现象，已经给大家灌输了一个常识，更多的模型参数能使模型效果变得更好。 然而随着模型参数的增加，现在硬件的显存容量已经达到了能支持的极限，同时参数量增加使计算的时间开销更大。

那 ALBERT 就是用于改进参数大的问题的。

## 具体方案
ALBERT 从两个方面对 BERT 的参数进行缩减：
1. Factorized embedding parameterization：把 Token Embedding 进行矩阵分解
2. Cross-layer parameter sharing：多层之间共享参数

此外 ALBERT 还引入了一个新的预训练方法：
1. Inter-sentence coherence loss：句子顺序损失

### Embedding 矩阵分解
常规的 BERT 词向量维数 E 和隐藏层向量维数 H 是相等的 E=H，词向量维护了一个矩阵的大小为 $V \times E$，其中 V 是词表大小。 ALBERT 把词向量矩阵分解成了两个矩阵，尺寸分别是 $V \times E$ 和 $E \times H$，其中 $E \ll H$。

### 层间共享参数
BERT 每层主要有两种参数：Feed Forward 参数和 Attention 参数。ALBERT 之间简单的把两种参数在各层之间都贡献。

### 预训练方法
BERT 采用两个预训练任务进行联合，分别是 MLM（Masked Language Model)和 NSP(Next Sentence Prediction)。很多论文 Argue 说 NSP 任务并不会给下游带来提升，本论文提出的观点 NSP 不能带来提升的原因是其对比MLM来说太简单了。

此论文对句子级别的预训练任务提出了SOP( sentence-order prediction)任务，即使对连续的两个句子，有50%概率保持原样作为正样本，50%概率颠倒他们的顺序作为负样本。

## 实验
实验结果太多了，挑几个重点的来说一下。

### 模型参数量
模型参数量见下图

![image](https://user-images.githubusercontent.com/80689631/113418414-05002480-93f8-11eb-909b-e525b41b8bb7.png)

可以看到比 BERT 少非常多！

### 总体实验结果
总体实验结果见下图

![image](https://user-images.githubusercontent.com/80689631/113418959-1138b180-93f9-11eb-8de1-012fd5523b9e.png)

可以看到 ALBERT 模型可以达到 SOTA 结果。

### 词向量 size 的影响
词向量 size 的影响见下图

![image](https://user-images.githubusercontent.com/80689631/113418763-adae8400-93f8-11eb-8487-55d9ed9ae388.png)

可以看到从 768 缩减到 64 性能损失也不太大。

### 层间参数共享的影响
层间参数共享的影响见下图

![image](https://user-images.githubusercontent.com/80689631/113418753-a9826680-93f8-11eb-8f73-f5d01dc53a82.png)

可以看到全部共享性能损失也不太大。

### Dropout 影响
论文指出 ALBERT 对 Dropout 很敏感，去掉 Dropout 反而是效果提升明显，估计原因是参数量本来就不大，不用防止过拟合把。见下图

![image](https://user-images.githubusercontent.com/80689631/113418525-3f69c180-93f8-11eb-8e5d-67e0fe49a92a.png)

### NSP 和 SOP 对比
NSP 和 SOP 对比，到底咋样，见下图

![image](https://user-images.githubusercontent.com/80689631/113418509-324cd280-93f8-11eb-9481-cae80aac1972.png)

SOP 明显优于 NSP。
