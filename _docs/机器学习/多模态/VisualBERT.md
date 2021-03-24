---
layout:     post
title:      VisualBERT 介绍
subtitle:   'A SIMPLE AND PERFORMANT BASELINE FOR VISION AND LANGUAGE'
date:       2020-02-20
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 多模态
    - BERT
---

# VisualBERT 介绍

VisualBERT 论文名 A SIMPLE AND PERFORMANT BASELINE FOR VISION AND LANGUAGE， 是一种图文预训练方法。  
论文地址： https://arxiv.org/pdf/1908.03557.pdf

## VisualBERT 简介

如果按照 Single Stream 和 Dual Stream 的方式来划分， VisualBERT 属于 Single Stream 方法，也就是对文本模态和图片模态各种经过Embedding之后，拼接起来使用同一个模型一起编码。VisualBERT 使用一个 Transformer 结构联合训练图像和语言两个模态。在外部资源上预训练 VisualBERT 能提高后续具体应用效果。预训练后的模型在transformer的attention上面能粗略的对齐文本和图片区域。  
VisualBERT 模型结构与BERT一样，见下图：  
![image](https://user-images.githubusercontent.com/80689631/112320585-1b1c2f80-8cea-11eb-9ccc-838a4c6117cd.png)


## 方法详解

### 模型结构

VisualBERT 模型结构与 BERT 一样，只是输入的 Embedding 处有差别：
- 文本输入是token。token embedding、segment embedding 和 position embedding。
- 图片输入是各种标准的目标检测器提取 bounding region 的特征。特征也是 token embedding、segment embedding 和 position embedding。
- 文本输入为有序的（有position embedding), 图像输入为无序的（无position embedding），一些特殊的任务（图片区域和文本有显示对齐的输入信号）图片的position embedding 为关联的文本的 position embedding 之和。


### 预训练方法
预训练分为三个阶段：
- Task-Agnostic Pre-Training: 任务领域无关数据集预训练。训练是两个任务联合训练。
    - 任务1 Masked language modeling with the image：把一些词 mask 掉，预测这些词本身；
    - 任务2 Sentence-image prediction：一张图片和两个caption，一个caption为描述，另一个50%概率正确，50%概率错误，做二分类区分这两个情况。
- Task-Specific Pre-Training：任务领域相关数据集进一步预训练。与 Task-Agnostic 方法一样，数据不一样。
- Fine-Tuning：特定任务 finetune。


## 实验

### 模型参数
BERT base：
- 12 layers
- a hidden size of 768
- 12 self-attention heads.( load from pre-trained BERT)
- 对于 object detector， 不同数据集有不同的标准object detector。

### 预训练和下游任务数据集
- Visual Question Answering (VQA 2.0)
- Visual Commonsense Reasoning (VCR)
- Natural Language for Visual Reasoning (NLVR2)
- Region-to-Phrase Grounding (Flickr30K)

### 实验结果
VQA  
![image](https://user-images.githubusercontent.com/80689631/112320984-7f3ef380-8cea-11eb-863a-503c049c03b5.png)

VCR  
![image](https://user-images.githubusercontent.com/80689631/112321008-82d27a80-8cea-11eb-96be-014d4858b939.png)

NLVR2  
![image](https://user-images.githubusercontent.com/80689631/112321021-86fe9800-8cea-11eb-919e-4f7c3739efd1.png)
