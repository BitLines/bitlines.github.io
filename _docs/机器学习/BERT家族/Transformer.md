---
layout:     post
title:      Transformer 介绍
subtitle:   'Attention Is All You Need'
date:       2021-02-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

## Transformer 介绍

Transformer 出自论文 Attention Is All You Need，从字面意思就是我们只要注意力就够了，什么CNN/RNN/LSTM之类的都靠边站。Transformer 发表于 NIPS，是一篇非常优秀的论文，从此开启了一种非常标准化的文本或者其他模态数据的编码方式。论文中的图片和公式描述简洁清晰，实验在英德翻译语料上测试。

论文地址： https://papers.nips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf

### Transformer 简介
Transformer 是第一个纯粹只使用注意力进行文本编码的，Self-Attention 的好处可以捕捉词之间的长依赖。

### 模型结构

Transformer 结构如下图所示：

![image](https://user-images.githubusercontent.com/80689631/113374704-449b2200-93a0-11eb-9be4-263325a70ac2.png)

整个Transformer 分为两个部分，Encoder部分和Decoder部分。input token先经过N个Encoder Block，之后output token再经过N个Decoder Block。上图左半边 对input编码，为Encoder部分；右半边 一边对 Output 编码一边生成下一个token 为 Eecoder部分。

每个Encoder和Decoder组成如下：
- Encoder 中，分别为 Multi-Head Attnetion，Add&Norm，Feed-Forward, Add&Norm。
- Decoder 中，分别为 Self Multi-Head Attnetion，Add&Norm，Input-Output Multi-Head Attnetion,Add&Norm，Feed-Forward, Add&Norm，Linear，Softmax。

#### Scaled Dot-Product Attention

单头注意力的计算公式：


$$
\textup{Attention}(Q, K, V ) = \textup{softmax}(\frac{QK^T}{\sqrt{d_k}})V
$$

其中Q，K，V是Attention的输入，Q 是 query，K 是 key，V 是 value。Attention 的作用是把 V 的信息累加到 Q上，累加的权重由 Q 和 K计算得到。

#### Multi-Head Attention

多头注意力要比单头注意力好，内在原理可以近似理解成
1. 多头注意力有点多个臭皮匠投票的感觉
2. 每个注意力头可关注到的局部信息不一样，然后把不同信息进行融合
3. 多头对比单头非线性表征能力更强

多头注意力公式如下：

$$
\textup{MultiHead}(Q,K,V)=\textup{Concat}(head_1,...,head_h)W^O
$$

$$
\textup{where}\ head_i=\textup{Attention}(QW_i^Q,KW_i^K,VW_i^V)
$$

在实际实现的时候，768维的向量切分成12份，然后再最前面stack起来，变成 12*64 的二维向量。

#### Position-wise Feed-Forward Networks

这其实就是2层的DNN，激活函数采用 ReLU：

$$
FFN(x) = max(0, xW_1 + b_1)W_2 + b_2 
$$

#### Position Embedding
Self-Attention是一个全连接的图结构，每个token可以连接到其他token，里面没有关于词位置信息，因此模型学习的上限就是一个高级的词袋。那怎么加入位置信息呢：位置向量！位置向量由两种方案，1种是 learnable 的向量在训练过程中更新，另一种fix的向量和词组合，让词自己学习位置信息。 原始的Transformer采用的是Fix的向量，后续的变种大多数改进采用了可学习的向量方式。

那具体来看，使用的向量是一个三角函数：

$$
PE(pos,2i) = sin(pos/10000^{2i/d_{model}})
$$

$$
PE(pos,2i+1) = cos(pos/10000^{2i/d_{model}})
$$

其中 $pos$ 是词位置， $i$ 是维度，$d_{model}$是模型的隐藏层size。为什么使用三角函数呢？是因为三角函数有线性关系

$$
\sin(x+y)=\sin(x)\cos(y)+\cos(x)\sin(y)
$$

这样距离为k的两个位置的位置向量就满足了线性关系。

### 实验

数据集
WMT 2014 English-German 4.5 million sentence pairs

参数
- Adam optimizer with $\beta_1 = 0.9, \beta_2 = 0.98$ and $\epsilon=10−9$
- $P_{drop} = 0.1$
- Encoder 层数 N = 6
- Decoder 层数 N = 6
- 隐藏层 $d_{model}$ = 512
- 注意力头数 h = 8
- 映射层 d = 2048

训练使用了 Label Smoothing 技巧。

实验结果

![image](https://user-images.githubusercontent.com/80689631/113384204-23dec680-93b8-11eb-8d30-c63835e6e05d.png)