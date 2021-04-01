---
layout:     post
title:      DropConnect 介绍
subtitle:   'Regularization of Neural Networks using DropConnect'
date:       2017-03-03
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 模型正则化
    - 机器学习
---

# DropConnect 介绍
DropConnect 是对 Dropout 的进一步延伸，可以视为 Dropout 的一般情况。  
论文地址：http://proceedings.mlr.press/v28/wan13.pdf

## DropConnect 简介

懂了 Dropout 之后， DropConnent 几句话就描述清楚了。 Dropout 核心思想让网络的一些隐藏层神经元不工作，输出置为0，那 DropConnent 其实就是让网络的一些权重不工作，让权重随机置为0。  
下面一张图就能清洗揭秘 DropConnent 的工作原理了。  
![image](https://user-images.githubusercontent.com/80689631/113237057-ba3bbb00-92d8-11eb-9a42-334db351deeb.png)

## 训练过程
DropConnent 训练过程中在网络前向传播的时候，要对权重进行随机mask，伪代码如下：  
![image](https://user-images.githubusercontent.com/80689631/113237109-d4759900-92d8-11eb-9ccb-48b8d3525228.png)

## 推理过程
DropConnent 推理过程就比 Dropout 繁琐多了，Dropout 推理阶段直接取消mask就行，而 DropConnent要多次采样。  
![image](https://user-images.githubusercontent.com/80689631/113237124-dc353d80-92d8-11eb-8076-3398a4b7ec8c.png)


## 读后小记
- Dropout 是 DropConnect 的一种特殊情况，如果把链接某个隐藏单元的权重全部置为 0，那 DropConnect 和 Dropout 效果是等价的。
- DropConnect 对比 Dropout 在模型实现的时候难度会大很多，要把 mask 嵌入到网络权重里面，而Dropout 在编码时候，可以用 ReLU 等激活函数一样的使用方式。
- DropConnect 的 Inference 过程需要采样，感觉有替代的方案。不然效率堪忧
- 个人觉得 DropConnect 没有火起来还是有原因的。