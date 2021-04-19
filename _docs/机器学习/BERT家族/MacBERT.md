---
layout:     post
title:      MacBERT 介绍
subtitle:   'Revisiting Pre-trained Models for Chinese Natural Language Processing'
date:       2021-03-21
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# MacBERT 介绍

MacBERT 全称 MLM
as correction BERT，出自论文 Revisiting Pre-trained Models for Chinese Natural Language Processing。 在百度的 ERNIE 之上做了一些改进。 主要是在中文语料上预训练 BERT。

论文地址：<https://arxiv.org/pdf/2004.13922.pdf>

## MacBERT 简介
MacBERT 仍然延续 ERNIE 思路仍然使用全词 MASK。ERNIE 的在预训练的时候对实体词或者短语进行随机 MASK。 MacBERT 在此基础上主要做了两点改进：
1. 使用词语级别的 N-gram 进行 MASK。
2. 不再使用 [MARK] 符号替换词，而是使用word2vec 寻找的相似词进行随机替换。

## 具体方法

下图展示了中文分词、BERT分词、全词MARK(WWM)、N-gram Mask 和 Mac Mask 的区别：

![image](https://user-images.githubusercontent.com/80689631/113415001-d894da00-93f0-11eb-9a68-6d21c93afc8c.png)

在具体实施过程中为：
1. 采用全词 Mask 和 N-gram Mask 策略，unigram 到 4-gram 的占比分别是 40%，30%，20% 和 10%。
2. 与其使用 [MASK] 这种在 finetune 时候见不到的词进行替换，本文采用相似词进行替换，词语使用分词工具进行切分，相似词使用 word2vec 工具，如果一个 N-gram 被 Mask，词语将被独立进行替换。
3. Mask 占比为全部 token 的 15%，其中 80% 使用相似词进行替换， 10% 使用随机词进行替换， 10% 不替换。


### 实验结果

预训练语料：采用中文维基百科，包含中文简体和繁体。

机器阅读

![image](https://user-images.githubusercontent.com/80689631/113415103-13970d80-93f1-11eb-972e-838bd5e136dc.png)

文本分类

![image](https://user-images.githubusercontent.com/80689631/113415356-9ae48100-93f1-11eb-9bcf-d3954efb3277.png)

句子对分类

![image](https://user-images.githubusercontent.com/80689631/113415362-9f109e80-93f1-11eb-9ecf-4661febdb9d9.png)