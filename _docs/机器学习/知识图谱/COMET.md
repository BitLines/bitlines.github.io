---
layout:     post
title:      COMET 介绍
subtitle:   'Commonsense Transformers for Automatic Knowledge Graph Construction'
date:       2020-06-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 知识图谱
---

# COMET 介绍
COMET 全称 Commonsense Transformers for Automatic Knowledge Graph Construction  
论文地址：https://arxiv.org/pdf/1906.05317.pdf


概括起来是，关系三元组 ，其中  是关系头部，是关系，是关系尾部。使  作为语言模型输入，使用文本生成预测。
## 基础介绍

使用 GPT 训练一个常识知识图谱构建模型。数据集是比较有特色的，关系中的实体都是一句话表达的。

## 模型介绍

### 模型结构

模型结构如下图，常规的Transformers。输入向量是词向量+位置向量。
模型输入  
![image](https://user-images.githubusercontent.com/80689631/113085885-3b307f00-9213-11eb-928e-e90d90e7fd9b.png)


模型输入是 $X=\{X^s, X^r, X^o\}$ ，其中 $X^s$ 是关系头部，$X^r$ 是关系，$X^o$ 是关系尾部。如下图  
![image](https://user-images.githubusercontent.com/80689631/113086008-661ad300-9213-11eb-842f-0c04439bb830.png)

训练目标
训练目标是给定 关系三元组中的 $[X^s,X^r]$ ，使用文本生成预测 $X^o$。
$$\mathcal{L}=-\sum_{t=|s|+|r|}^{|s|+|r|+|o|}{log P(x_t|x_{<t})}$$


## 实验结果

### 参数设置
- GPT 12 层
- 768 hidden size
- 12 attention heads
- dropout prob 0.1
- batch size 64

### 数据集
- ATOMIC
- ConceptNet

### 评价指标
- 训练集种子的比例1% 10% 50%
- PPL BLEU-2
- LSTM GPT
- AMT 人工评价