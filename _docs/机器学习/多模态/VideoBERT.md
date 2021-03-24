---
layout:     post
title:      VideoBERT 介绍
subtitle:   'A Joint Model for Video and Language Representation Learning'
date:       2020-02-20
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 多模态
    - BERT
---

# VideoBERT 介绍

VideoBERT 论文名 A Joint Model for Video and Language Representation Learning， 是一种视频文本预训练方法。  
论文地址： https://arxiv.org/pdf/1904.01766.pdf

## VideoBERT 简介

首先来看看 VideoBERT 能干嘛，先来上个图。  
![image](https://user-images.githubusercontent.com/80689631/112309044-d1c5e300-8cdd-11eb-840d-7ab12488f23f.png)

论文里面介绍了两个例子，上图的上半部分描述的是：给定一道菜的制作步骤，VideoBERT 可以根据步骤的描述来生成一段视频；下半部分描述的是：给定一张图片，VideoBERT 生成后续的一系列图片组成一个连贯的视频。 挺有趣的对吧~ 那我们来看看具体是咋做的呢？

## 方法详解

### 模型结构

VideoBERT 的模型结构和 BERT 基本一样，区别在于输入的 Embedding 上。 模型结构如下图  
![image](https://user-images.githubusercontent.com/80689631/112308444-1ac96780-8cdd-11eb-9fbf-0d027e496fc9.png)

VideoBERT 的 Embedding 分为两种，一种输入是文本的token序列，另一种是视频的图片帧序列：
- 文本输入是token。token embedding、segment embedding 和 position embedding。
- 视频的输入是vedio token。同样也是token embedding、segment embedding 和 position embedding。Video token 的获取方式是先把视频转化成20fps，然后抽取 1.5秒视频（30个图片），然后把所有图片构建成一个词典，用一个预训练好的模型encode成向量。在预训练时，video embedding 是 fixed 不更新。

### 预训练方法

- **text-only**: 采用 masked language model
- **video-only**: 采用 masked language model （video 有词表的，embedding 部分是预训练的图像模型且不更新，分类器部分要更新）
- **video-text**: cls 二分类video-text是否匹配

## 实验
TPU训练的。。模型参数与 $BERT_{LARGE}$一样。
- 层数 24
- 隐藏单元树 1024
- 注意力头 16


### 数据集
• 预训练YouTube，cooking video
• 微调和预测 YouCook II