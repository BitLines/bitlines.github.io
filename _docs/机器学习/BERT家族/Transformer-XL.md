---
layout:     post
title:      Transformer-XL 介绍
subtitle:   'Attentive Language Models Beyond a Fixed-Length Context'
date:       2021-03-05
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# Transformer-XL 介绍
Transformer-XL 出自论文 Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context。

论文地址：https://arxiv.org/pdf/1901.02860.pdf

## Transformer-XL 简介
Transformer 结构已经是一种标准化的文本编码方法，其优点是能学习词之间的上下文长依赖，对比CNN/RNN等方法有很大提升，然而它的问题有两个：
1. 由于计算效率和显存容量的原因，Transformer 能处理的文本长度有限，一般是512
2. 对长文本进行切分再对每个段落分别训练，一方面打破了上下文环境信息，另一方面 position 向量是绝对位置向量， position 向量作用于每个段落并不能反映其真实的文章位置。 

Transformer-XL 虽然没有完全解决问题1，但是使处理文本长度是原始 Transformer 的 450%，对于问题2，Transformer-XL不再使用绝对位置，而是用相对位置。

$$
\bar_{h}_{\t}
$$  


![image](https://user-images.githubusercontent.com/80689631/113254529-48279e00-92f9-11eb-8bea-9632f50d478b.png)

![image](https://user-images.githubusercontent.com/80689631/113254552-4fe74280-92f9-11eb-9899-3fc8dea8aff0.png)


