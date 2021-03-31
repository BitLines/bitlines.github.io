---
layout:     post
title:      FGSM 介绍
subtitle:   'EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES'
date:       2020-03-22
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 对抗学习
    - 模型正则化
---

# FGSM 介绍

FGSM 全称是 Fast Gradient Sign Method，出自论文 EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES，这是一篇引用量非常高的论文，虽然方法很简单，但是在模型的对抗和攻击的领域中具有里程碑的性质，影响深远。  
论文原文地址： https://arxiv.org/pdf/1412.6572.pdf

## FGSM 简介

想象一个场景，小王为了提高情感分类模型的准确率花了很大的努力，例如各处收集语料，实验各种模型，反正就是为了炼丹花了很多力气。经过一番努力，小王拿出了自己最得意的模型交给了业务方小张。正当小王洋洋得意的时候，小张竟然毫不客气，故意刁难挑出了几个 bad case 甩了过来，说“呵呵，你说得对” 这明明是个负面情感的话，模型给出正面情感的置信度竟然高达0.99。

上面情景之中 “呵呵，你说得对” 就叫做对抗样本（adversarial examples）：一些故意挑出的 bad case，模型误判且置信度很高。

这篇论文之前，大家普遍觉得造成对抗样本的原因是模型的非线性和过拟合问题。FGSM 就是探索这类问题的（并没有完全解决，只能说迈出尝试和探索的一步），指出在输入样本上加入一个非常小的线性扰动就可以改变模型的输出。

## 详细介绍

简单来讲，FGSM 的想法就是在一个模型的输入样本向量 $x$ 上，加上一个噪声扰动 $\eta$，使得加了这个扰动之后，模型输出正确类标的概率 $p(y|x+\eta) < p(y|x)$，如何得到 $\eta$ 呢？就是用模型输出的损失函数对 $x$ 求偏导。

形式化描述一下，对于一个以$\theta$为参数的模型，$(x,y)$为样本，其中$x$为输入向量，$y$为与$x$关联的类标，$J(\theta,x,y)$为模型的损失函数，那么 FGSM 方法求出的 $\eta$ 为
$$\eta=\epsilon \textup{sign}(\bigtriangledown_{x}J(\theta,x,y))$$

到底 FGSM 发生了一个什么效果，来看下面这个图。  
![image](https://user-images.githubusercontent.com/80689631/112847448-aaa25380-90d9-11eb-9eff-a1b2052d3fb4.png)

这个例子中，$x$ 是图片向量，$y$是“熊猫”类别，模型给出的置信分是 57.7%，那噪声扰动$\eta$就是使57.7%变小为目标对输入$x$的偏导。


特别的，对于一个线性模型，FGSM 其实就是加入了一阶范数正则化。想详细了解的可以去看看论文，论文有给公式去推到。个人觉得这里是作者让大家把对抗和模型正则化联系起来去讲解的。  

最终模型训练的损失函数为为原始样本 $x$ 和对抗样本 $x+\eta$ 损失函数的 trade-off：
$$\tilde{J}(\theta,x,y)=\alpha J(\theta,x,y) + (1-\alpha)J(\theta,x+\epsilon \textup{sign}(\bigtriangledown_{x}J(\theta,x,y)),y)$$

## 后续延伸
FGSM 在$x$ 的偏导数上取符号(sign)，对于多维偏导数每个维度只看方向不看大小，后续有很论文是 FGSM 的子孙，后面逐步来讲吧~
