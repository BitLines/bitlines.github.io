---
layout:     post
title:      SMART 介绍
subtitle:   'Robust and Efficient Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized Optimization'
date:       2021-03-22
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 对抗学习
    - 迁移学习
---

# SMART 介绍

SMART 全称 Robust and Efficient Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized Optimization，是一种使用了对抗方法的迁移学习技术。  
论文原文地址： https://arxiv.org/pdf/1911.03437.pdf

## SMART 简介

SMART 的全称是 Robust and Efficient Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized Optimization （太长。。。都能绕地球一圈了），翻译成中文的意思是通过正则化优化方法实现的鲁棒高效的自然语言模型的微调方法。 主要解决的问题是目前自然语言模型通常是大规模语料进行预训练的，文中提出了一种通用的比原始方法更好的微调方法。既然是模型Fine-Tune就是迁移学习的一种，本文中的方法还引入了对抗的机制，也算是对抗学习的范畴。具体咋做微调的呢？ SMART 论文中的方法分为两个部分：诱导平滑对抗正则化（有可能翻译有问题，英文 Smoothness-Inducing Adversarial Regularization），布雷格曼最近点优化（英文 Bregman Proximal Point Optimization）。

诱导平滑对抗正则化实际上是在 Embedding 层加入了噪声，与简单的高斯白噪声不同的是，诱导平滑对抗正则化加的噪声引入了对抗的思想，在更新判别器之前，先用生成器生成一个能使分类为误差较大的噪声，然后优化模型使原始输入和加入噪声的输入同时分类正确。

布雷格曼最近点优化其实是一种置信区域方法（trust-region methods），其背后的想法是让模型在一个batch样本的更新过程中，更新前后概率分布的交叉熵不能过大（也就是步子走小一点，小心扯到蛋）。

下面来详细看看。

## 详细介绍

### 诱导平滑对抗正则化 Smoothness-Inducing Adversarial Regularization
给定一个模型$f(·;\theta)$ 和 $n$ 个样本的数据集 $\{(x_i, y_i)\}_{i=1}^{n}$，其中 $x_i$ 表示第 i 个样本的输入 embedding，$y_i$表示类标。诱导平滑对抗正则化的fine-tune目标是:
$$min_{\theta}F(\theta)=L(\theta)+\lambda_sR_s(\theta),$$
其中 $\lambda_s$是超参，$L(\theta)$ 是学习目标的损失函数  
$$L(\theta)=\frac{1}{n}\sum_{i=1}^{n}\ell(f(x_i;\theta), y_i)$$
其中 $\ell$是损失函数视具体任务而定。$R_s(\theta)$ 就是 Smoothness-Inducing Adversarial Regularization：
$$R_s(\theta)=\frac{1}{n}\sum_{i=1}^{n}\max_{||\tilde{x_i}-x_i||\le\epsilon}\ell_s(f(\tilde{x_i};\theta),f(x_i;\theta))$$
其中 $\epsilon$是超参，一般来说 $f(·;\theta)$ 是输出概率分布，$\ell_s$是KL散度
$$\ell_s(P,Q)=D_{KL}(P||Q)+D_{KL}(Q||P)$$

从 $R_s(\theta)$ 上来看，需要在$x_i$附近寻找一个 $\tilde{x_i}$，使得交叉熵最大。 $R_s(\theta)$其实就是一个生成器，来在原始输入 $x_i$ 附近找一个最能使分类器认不出的样本 $\tilde{x_i}$。因为新输入与原始输入距离很近，所以假设认为是两个样本的类标是一致的。

### 布雷格曼最近点优化 Bregman Proximal Point Optimization
为了更好的利用诱导平滑对抗正则化，在优化目标 $F_{\theta}$时，使用布雷格曼最近点优化方法。为了防止在上面的对抗方法中，模型侵略性的更新（理解侵略性的更新，应该是模型学着学着跑偏了），使用置信区间方法在模型每次迭代的时候加一个强约束。形式化描述为：
$$\theta_{t+1}=argmin_{\theta}F(\theta)+\mu D_{Breg}(\theta, \theta_t)$$
其中 $\mu$ 是超参，$D_{Breg}$ 是布雷格曼差异，定义为：
$$D_{Breg}(\theta, \theta_t)=\frac{1}{n}\sum_{i=1}^{n}\ell_s(f(x_i;\theta),f(x_i;\theta_t))$$
为了更好的炼丹，在训练过程中，还可以加入动量的想法，加入动量后的优化目标为：
$$\theta_{t+1}=argmin_{\theta}F(\theta)+\mu D_{Breg}(\theta, \tilde{\theta_t})$$
其中 $\tilde{\theta_t}=(1-\beta)\theta_t+\beta \tilde{\theta}_{t-1}$ 是指数动量平均值。$\beta \in (0, 1)$是超参。

模型训练过程的伪代码如下：  
![image](https://user-images.githubusercontent.com/80689631/112160220-ec885100-8c24-11eb-83ec-2b4e5dba7d46.png)

## 实验结果

实验参数设置
- $\epsilon = 10^{−5}$
- $\sigma=10^{-5}$
- $\mu=1$
- $\lambda_s \in {1, 3, 5}$
- $\eta=10^{-3}$
- $\beta=0.99$ for first 10% updates, $\beta=0.999$ the rest

实验结果如下图

![image](https://user-images.githubusercontent.com/80689631/112160311-ff9b2100-8c24-11eb-8409-f7bdcbb9e1f9.png)

## 其他参考 
1. VBPP (vanilla Bregman proximal point): https://arxiv.org/pdf/0905.1643.pdf
2. MBPP (momentum Bregman proximal point) 也叫 Mean Teacher: https://arxiv.org/pdf/1703.01780.pdf
