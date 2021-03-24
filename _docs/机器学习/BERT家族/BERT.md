---
layout:     post
title:      BERT 介绍
subtitle:   'Pre-training of Deep Bidirectional Transformers for Language Understanding'
date:       2021-03-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

## BERT 介绍

论文原文地址： https://arxiv.org/pdf/1810.04805.pdf

### BERT 简介
BERT 简称 Bidirectional Encoder Representations from Transformers，是 NAACL 的 best paper。也是 NLP 领域具有里程碑意义的一篇论文。BERT 的出现可以说是必然的，借鉴了前人很多成功的研究成果：
1. 大规模语料预训练、特定任务finetune（ELMo/GPT等）； 
2. Transformer 的 self-attention 网络结构；
3. MLM 和 NSP 的预训练方法

BERT 与 GPT 和 ELMo 的区别和联系如下图：  
![image](https://user-images.githubusercontent.com/80689631/111260430-b9a9f000-865b-11eb-92c4-3b0521805d04.png)  
可以看到
- BERT 和 GPT 的差别在于 BERT 是Transformer 的Encoder， GPT 是 Transformer 的 Decoder
- BERT 和 Emlo 的差别在于虽然都是双向编码，但是 BERT 采用 Self-Attention编码， ELMo 使用 BiLSTM。

下面这张图可以把BERT的所有内核，囊括了网络结构、预训练和下游任务参数微调等。  
![image](https://user-images.githubusercontent.com/80689631/111248122-4052d300-8644-11eb-9cf2-cd7114168143.png)

下面详细介绍一下

### BERT 模型结构
BERT 的关键技术点有以下几个，后面逐步讲解
1. 模型结构
2. 大规模语料预训练
3. 特定任务语料的finetune

#### 模型结构

如果了解过 Transformer 了，那理解 BERT 的模型结构就非常容易了。 BERT 的模型结构就是 Transformer 的 Encoder 部分。 强烈建议大家去读 NIPS 原文 《[Attention Is All You Need](https://arxiv.org/pdf/1706.03762.pdf)》。 模型结构如下图  
![image](https://user-images.githubusercontent.com/80689631/111251536-67ac9e80-864a-11eb-9915-d39047787523.png)  

与 Transformer Encoder 唯一不同的是输入的向量有所差别。BERT的输入层是 Token 向量、Position 向量 和 Segment 向量。 Position 向量不再是三角函数公式，而是一个可以学习的向量。 如下图所示  
![image](https://user-images.githubusercontent.com/80689631/111251634-9591e300-864a-11eb-88be-8fb1fbab48d0.png)  
此外 BERT 加入了一些特殊 Token，[CLS]、[SEP]、[UNK]等。 [CLS] 添加在所有输入的最开始位置，[SEP] 放在 Segment 分割处（例如 sentence pair 输入时，放在两句的中间）和句子结尾， [UNK] 代表 OOV（Out-of-Vocabulary） 字符。

#### 大规模语料预训练
预训练的任务有两个，分别是 MLM（全称 Masked Language Model，掩码语言模型）和 NSP（全称 Next Sentence Prediction，下一句预测）。

**Task1: MLM（Masked Language Model）**  
MLM 的动机是使模型从语言模型预训练方法中“记忆”一些语言本身的特性，比如词法特征（一些词的词性信息等）、句法特征（词性信息的组合关系）和语义特征（同义词等）。  
MLM 预训练方法是把句子中的一些 Token 随机删除掉，然后在被删除 Token 的位置上预测其本身。具体的是在输入句子中，选择 15% 的位置（例如一句话有100个token，会选择15个位置），进行该位置词的预测。被选中的位置进行如下字符替换操作：
- 随机 80% 的被选中位置，使用特殊 Token [MASK]
- 随机 10% 的被选中位置，使用其他随机 Token 进行替换
- 剩下随机 10% 不进行任何替换

**Task2: NSP（Next Sentence Prediction）**  
NSP 的动机是在一些 NLP 任务中，经常会输入两个句子，例如文本语义相似度、问答匹配、机器阅读等，在预训练如果能够在大规模语料上掌握一些句子之间的关系信息，那下游任务可能会有提升。  
NSP 输入是一个句子对（A,B)，取 [CLS] 位置的向量接一个分类器，判断句子 B 是否为句子 A 的下一句。语料的构造是
- 随机 50%，在真实语料中，B 句在 A 句之后
- 随机 50%, B 句是从语料中随机选取的不在A之后的其他句子。

#### NLP 子任务 finetuning
BERT 的一个很大的特点（我认为就是优点）是不同的 NLP 子任务都用同一个网络结构。

**Sentence Pair Classification Task**：双句子分类，可以用于文本相似度匹配，问答匹配。 取 [CLS] 位置的向量，后面接一个分类器（有的再加一层DNN）  
![image](https://user-images.githubusercontent.com/80689631/111253300-ec4cec00-864d-11eb-9495-4e8f8ef97f45.png)  

**Single Sentence Classification Task**：单句子分类， 取 [CLS] 位置的向量，后面接一个分类器  
![image](https://user-images.githubusercontent.com/80689631/111253382-0edf0500-864e-11eb-8cec-4094604c9e5d.png)  

**Question Answer Task**：预测一个 span 的起始和结束位置（适用于机器阅读、文本标签提取、slot提取等任务）。 例如在机器阅读任务中，把 query 作为第一句，paragraph 作为第二句，预测 paragraph 中的一个span 的起始和结束位置。  
![image](https://user-images.githubusercontent.com/80689631/111253660-86149900-864e-11eb-949c-8cc0444ce97b.png)  

**Single Sentence Tagging Task**：常规的序列标注任务（NER、POSTAG等任务），每个输入 Token 预测一个类别（BIO这样的），其实可以把 BERT 作为 Encoder 上层再接 CRF Layer来使用。  
![image](https://user-images.githubusercontent.com/80689631/111259797-a0ed0a80-865a-11eb-955e-0fb9e02e2b2a.png)


### 实验

BERT 有两种基调的模型 BASE 和 LARGE，参数规模为：
- BERT BASE (L=12, H=768, A=12, Total Parameters=110M)  
- BERT LARGE (L=24, H=1024, A=16, Total Parameters=340M)
其中，L 为网络层数， H 为隐层大小， A 为注意力头数。 可以看到 Base 参数是110M（1亿），Large 参数为 340M（3亿）。

在 pre-train 时， batch size of 256，max tokens 512。33 亿量级词的语料上训练。 Adam learning rate 1e-4, β1 = 0.9, β2 = 0.999, L2 weight decay of 0.01  
在 fine-tune 时， batch size of 16, 32, learning rate 设置 5e-5, 4e-5, 3e-5, and 2e-5，epochs 2,3,4

实验结果可以说是 **霸榜！**  
![image](https://user-images.githubusercontent.com/80689631/111261191-02ae7400-865d-11eb-9010-c9bdc3b219f9.png)
