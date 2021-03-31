---
layout:     post
title:      TranE 介绍
subtitle:   'Translating Embeddings for Modeling Multi-relational Data'
date:       2017-06-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 知识图谱
---

# TranE 介绍

TransE 全称 Translating Embeddings for Modeling Multi-relational Data，是知识图谱领域较早也是影响力较深远的一篇论文。  
论文地址：https://proceedings.neurips.cc/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf

## 基础介绍

TransE 文章发表于 2013 年，跟 word2vec 是一个年代的东西（不得不说大神们水论文的速度太惊人了），算是关系抽取一个时代里程碑。

TransE 其实用一句话就能简单描述：

**给定关系三元组 $(h, r, t)$，其中 h, t 代表关系的头和尾，r 代表关系，TransE 学习得到 Embedding $(e_h, e_r, e_t)$ 使得对于一个正确的三元组 $e_h + e_r \approx e_t$** 

## 模型介绍
损失函数
$$\mathcal{L}=\sum_{(h,\ell,t) \in S}{\sum_{(h',\ell,t') \in {S'_{(h,\ell,t)}}}{[\gamma + d(h+\ell,t)-d(h'+\ell,t')]_+}}$$

其中 $[x]\_$ 为 $max(0, x)$，$S'_{(h,l,t)}$ 表示负采样，把正确三元组中的 $h$ 或者 $t$ 进行随机替换，变成错误的三元组。

训练过程  
![image](https://user-images.githubusercontent.com/80689631/112713119-67e05000-8f0e-11eb-82fe-0b1c331b916b.png)


## 实验结果

数据集
- Wordnet
- Freebase

参数设置  
 ![image](https://user-images.githubusercontent.com/80689631/112713239-30be6e80-8f0f-11eb-8dae-7ce6a15e6ed5.png)

召回@10实验结果: Wordnet能到89，Freebase能到47%  
 ![image](https://user-images.githubusercontent.com/80689631/112713241-374ce600-8f0f-11eb-8636-893870893943.png)
