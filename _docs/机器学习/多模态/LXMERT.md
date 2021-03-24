---
layout:     post
title:      LXMERT 介绍
subtitle:   'Learning Cross-Modality Encoder Representations from Transformers'
date:       2020-02-20
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 多模态
    - BERT
---

# LXMERT 介绍

LXMERT 全称 Learning Cross-Modality Encoder Representations from Transformers， 是一种图文预训练方法。  
论文地址： https://arxiv.org/pdf/1908.07490.pdf

## LXMERT 简介

如果按照 Single Stream 和 Dual Stream 的方式来划分， LXMET 属于 Dual Stream 方法，也就是对文本模态和图片模态在网络低层先进行各自的编码，然后在网络的高层进行交叉融合。
LXMERT 主体还是 Transformer，先分别对文本和图像用 Self-Attention 编码，再用 Cross-Attention 交叉编码。 整体模型结构如下图：  
![image](https://user-images.githubusercontent.com/80689631/112311249-79dcab80-8ce0-11eb-9849-7b34f8c68d34.png)

## 方法详解

### 模型结构
输入向量：
- 文本输入是token：token embedding 和 position embedding。
- 图片输入是各种标准的目标检测器提取 bounding region 的特征。特征也是 token embedding 和 position embedding。 position embedding 取区域的位置信息（左上和右下的 x1, y1, x2, ye）。一个图片选36个object

模型结构：
- Object-Relationship Encoder 层和 Language Encoder，分别对文本和图片部分使用SelfAtt编码
- Cross-Modality Encoder 层：文本以文本为Q，图片为KV，做att编码，图片反之。然后文本和图片分别SelfAtt。

模型输出得到3个部分的编码结果：图片每个object编码，文本每个token编码，和文本CLS 双模态表示编码，CLS是在文本部分。

### 预训练方法

预训练方法可以用下图来描述，里面包含3个任务：Masked Cross-Modality LM，Masked Object Prediction，Cross-Modality Mathcing  
![image](https://user-images.githubusercontent.com/80689631/112312609-f02ddd80-8ce1-11eb-8acf-4c4ea9be3f16.png)


预训练的3个任务详细介绍如下：
- **Language Task** : Masked Cross-Modality LM，以 0.15 概率 mask 一个词，然后预测这个词。
- **Vision Task** : Masked Object Prediction，以 0.15 概率 mask 一个图片object，然后预测这个 object 的属性
- **Cross-Modality Tasks** : 分两个任务，一个是0.5概率替换文本分类是否被替换，另一个是Image Question Answering ，给定问题和图片预测答案。


## 实验

### 模型参数
- Language Encoder 9层
- Object-Relationship Encoder 5层
- Cross-Modality Encoder 5层，（可以看到最多是5+9=14层）
- hidden size 768.
- 图像 101-layer Faster R-CNN from scratch 
- pretrain Adam lr $1e^{-4}$, 20 epochs
- finetune lr $1e^{-5}$, 4 epochs

### 预训练数据集
- Visual Question Answering (VQA 2.0)
- Visual Genome
- MS COCO

### 下游任务
- VQA
- GQA
- NLVR2

### 实验结果

![image](https://user-images.githubusercontent.com/80689631/112312738-16537d80-8ce2-11eb-9a25-702555195b0a.png)