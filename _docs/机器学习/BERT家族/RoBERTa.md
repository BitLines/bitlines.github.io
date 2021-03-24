---
layout:     post
title:      RoBERTa 介绍
subtitle:   'A Robustly Optimized BERT Pretraining Approach'
date:       2021-03-02
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# RoBERTa 介绍

论文原文地址： https://arxiv.org/pdf/1907.11692.pdf

## RoBERTa 简介
RoBERTa 全称 A Robustly Optimized BERT Pretraining Approach。 文章主要是介绍对原始 BERT 预训练方法的修改，来提高后续任务效果。
主要提高的方案有4种：
1. 动态掩码：Dynamic Masking
2. 不带NSP的整句预训练： Full-Sentences without NSP
3. 增大批量大小：large mini-batches
4. 更大的BPE词典：larger BPE 词典

## 训练过程分析

训练过程分析主要是做一些对比实验，从上述的 4 个方面控制变量做消融实验。

### Static vs. Dynamic Masking

原始的 BERT 实现的 MLM(Masked Language Model)，其实现逻辑是在预处理阶段对词进行随机替换，造成了静态 Mask，也就是一条数据在多个epoch里面，Mask的情况是相同的。 动态 Mask 是在模型迭代过程中，对每条样本的词进行随机替换，这样在不同的epoch上，同一条样本的Mask结果不同。对比实验如下图，可以看到动态Mask比静态Mask 略有提升。

![image](https://user-images.githubusercontent.com/80689631/112106881-29365700-8be9-11eb-9fca-78e1b6d83a56.png)


### Model Input Format and Next Sentence Prediction

原始 BERT 的预训练还加入了 NSP 任务(Next Sentence Prediction)，其背后的动机是很多下游的 NLP 任务都是双句子作为输入的（例如机器阅读，文本匹配等），如果在预训练阶段能够学习一定的句子间语义关系的信息，那可能会提高下游任务的性能。 继 BERT 之后的一些论文对 NSP 是有争议的，有些论文指出 NSP 确实对下游任务有提升，而有些则质疑 NSP 对下游任务的性能不增反降。 RoBERTa 构造了几组实验来证实NSP到底咋样。实验设置为：

- SEGMENT-PAIR+NSP: 带有NSP，与原始 BERT 相同，随机取上下文和下一句，50%下一句是连贯的，50%下一句是随机采样的。
- SENTENCE-PAIR+NSP: 带有NSP，只选取两个句子，50% 两个句子是前后句关系， 50% 其他。
- FULL-SENTENCES: 不带NSP，尽量拼满 512 个token, 如果文章结束，则继续下一个文章。
- DOC-SENTENCES: 不带NSP，尽量拼满 512 个token, 如果文章结束则停止。

实验结果 DOC-SENTENCES 最佳  
![image](https://user-images.githubusercontent.com/80689631/112113930-6a7f3480-8bf2-11eb-9faa-9352704adf3b.png)

### Training with large batches

BatchSize 也是一个重要的参数，选取 256，2048 和 4096 对比实验。 结果如下，结论是选择 2048 会好很多。

![image](https://user-images.githubusercontent.com/80689631/112109767-ebd3c880-8bec-11eb-9818-7a27f46dd447.png)

### Text Encoding

Byte-Pair Encoding (BPE) 是一个字符和词之间的一种编码方式（中文都是单个字符，并不存在这个问题），原始 BERT 词表是 30K，探索更大的 BPE 词表，本文做的一个尝试是加大到 50K。


## 最后实验结果 

dev set 结果

![image](https://user-images.githubusercontent.com/80689631/112114772-656eb500-8bf3-11eb-8f34-3ed2fe89f089.png)

下游任务结果 GLUE  
![image](https://user-images.githubusercontent.com/80689631/112114692-4ff98b00-8bf3-11eb-89fd-8b33ee561f19.png)  

