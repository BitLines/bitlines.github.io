---
layout:     post
title:      TinyBERT 介绍
subtitle:   'Distilling BERT for Natural Language Understanding'
date:       2021-03-04
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - BERT
---

# TinyBERT 介绍
TinyBERT 论文名 Distilling BERT for Natural Language Understanding，介绍了一种对 BERT 量身定制的知识蒸馏方法。  
论文原文地址： https://arxiv.org/pdf/1909.10351.pdf

## TinyBERT 简介

TinyBERT 是 BERT 的蒸馏版本，蒸馏主要是减少了隐藏层单元的 size 和网络的层数，注意力的头数没有减少，因为论文中的蒸馏方法对每个注意力的头也进行了蒸馏。 文章针对 BERT 的结构提出了针对 BERT 的定制化的蒸馏方法。

## 预备知识

### BERT 网络结构

BERT 网络结构随处可见，不再这里讲了。

### 知识蒸馏

知识蒸馏最早是一种模型压缩的方案，后来逐渐也演变出一些提升模型效果的方法。知识蒸馏背后的动机是，一些带有大规模参数的复杂模型（比如 BERT） 的准确率很高，但是难以应用于实际的工业系统，原因是工业系统对计算效率要求严苛，大模型计算速度比简单模型确实慢很多。 知识蒸馏（名字也很恰当）的作用就是能否把对大模型萃取成小模型，在模型效果下降不多的前提下，是计算效率大幅度提升。  
一般来讲（并不是所有的）知识蒸馏中有两个角色， Teacher 和 Student。Teacher 就是那个大模型，而Student就是小模型。知识蒸馏的学习目标一般是下面的形式

$$
L_{KD}=\sum_{x \in X}L(f^S(x), f^T(x)),
$$

其中， $f^S(x)$ 和$f^T(x)$分别代表 Student 和 Teacher 模型的某些输出（例如隐藏层输出或者分类层输出）。


## 方法介绍

### Transformer 蒸馏
假设 Student 网络是 M 层的 Transformer，Teacher 是 N 层的 Transformer 网络，（一般 N 大于 M，因为 Teacher 比 Student 复杂嘛），首先从 Teacher 的 N 层中选取出 M 层，和 Student 做一个映射 $n=g(m)$。再加入额外的两层：0 代表词向量层， N+1 和 M+1代表输出层。那么蒸馏的学习目标是所有层蒸馏损失函数的累加：

$$
L_{model}=\sum_{x \in X}\sum_{m=0}^{M+1} \lambda_m L_{layer}(f_m^S(x), f_{g(m)}^T(x)),
$$

其中， $L_{layer}$ 是Transformer 某一层的损失函数，具体怎么算的稍后来讲，$f_m(x)$是Transformer第m层的输出（包括attention和隐藏单元），$\lambda_m$ 是超参。

#### Transformer 层的蒸馏

**注意力蒸馏**：从 Teacher 到 Student 对应层进行 Attention 的蒸馏，蒸馏的方法就是把每个注意力头全都对齐一下：

$$
L_{attn}=\frac{1}{h}\sum_{i=1}^hMSE(A_i^S,A_i^T)
$$

其中，MSE表示最小二乘法，h表示注意力头数。

**隐藏层蒸馏**：从 Teacher 到 Student 对应层的隐藏单元的蒸馏，蒸馏方法是是两个向量能够在两个空间中进行线性变换，不是直接学习的原因是 Teacher 和 Student 的隐藏层 size 并不一样：

$$
L_{hidn}=MSE(H^SW_h, H^T)
$$

其中 $W_h$是学习的参数，所有隐藏层共用一个。

#### Embedding 层的蒸馏
Embedding 层的蒸馏和隐藏层蒸馏方法一样：

$$
L_{hidn}=MSE(E^SW_e, E^T)
$$

其中 $W_e$是学习的参数。

#### Prediction 层的蒸馏

预测层的蒸馏是较常见的交叉熵：

$$
L_{pred}=CE(z^T/t,z^S/t)
$$

#### 层损失的总结
把上述讲的几种情况汇总：  
> **当 $m=0$ 时，** $L_{layer}=L_{embd}$  
> **当 $0\lt m \le M$ 时，** $L_{layer}=L_{hidn}+L_{attn}$  
> **当 $m=M+1$时，** $L_{layer}=L_{pred}$ 


### 蒸馏方法

**通用蒸馏**：通用蒸馏是对模型进行预训练阶段的蒸馏。因为参数少很多，预训练蒸馏效果很差。
**特定任务蒸馏**：因为前面一些论文总结出BERT参数过多，导致过拟合，在蒸馏之外提出了数据增强方案来降低Teacher过拟合。
**数据增强**：在finetune的时候，对样本中的一些词进行随机替换或者[MASK]，

## 实验

### 参数设置

网络层数 M=4，隐藏层d=312，映射层d=1200，注意力头数h=12（没变)。共计 14.5M。  
原始BERT选用12层BERT 网络层数 N=12，隐藏层d=768，映射层d=3072，注意力头数h=12（没变)。共计 109M。  
M和N的映射关系是 $g(m) = 3 \times m$

实验结果  
![image](https://user-images.githubusercontent.com/80689631/112147886-2c950700-8c18-11eb-83f3-84666ebf21f8.png)
