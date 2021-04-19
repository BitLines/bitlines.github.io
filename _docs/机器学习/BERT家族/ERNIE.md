---
layout:     post
title:      ERNIE 介绍
subtitle:   'Enhanced Representation through Knowledge Integration'
date:       2021-03-17
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# ERNIE 介绍

ERNIE 全称 Enhanced Representation through Knowledge Integration，在中文预训练上对原始 BERT 做了一些改进。

论文地址： <https://arxiv.org/pdf/1904.09223.pdf>

## ERNIE 简介

## 具体方法

下图展示了 BERT 和 ERNIE 的主要区别：

![image](https://user-images.githubusercontent.com/80689631/113415687-54435680-93f2-11eb-97ad-e49acd8300fd.png)

可以看到BERT 对 Token 进行随机 MASK， 而 ERNIE 对 Token/Phrase/Entity 进行随机 MARK。

ERNIE 提高了 3 个级别的 MASK，分别是 Basic、Phrase 和 Entity 级别，如下图：

![image](https://user-images.githubusercontent.com/80689631/113415931-d469bc00-93f2-11eb-8b43-5a3aafa86a41.png)

其中，各种级别详细介绍：
- **Basic-Level Masking** : 句子中 15% 的中文字符被随机替换。
- **Phrase-Level Masking** : 对英文来说就是短语，而对中文来说是多字组成的词或者短语。
- **Entity-Level Masking** : 人名、地名、组织名、产品名等实体词被MASK


### 实验结果

最主要要关注的就是完形填空任务中，对实体词的预测，效果很惊喜：

![image](https://user-images.githubusercontent.com/80689631/113416384-cc5e4c00-93f3-11eb-8763-37b873d8e0c6.png)
