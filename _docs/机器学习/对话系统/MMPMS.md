---
layout:     post
title:      MMPMS 论文解读
subtitle:   'Generating Multiple Diverse Responses with Multi-Mapping and Posterior Mapping Selection'
date:       2021-07-06
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 对话系统
---


# MMPMS 介绍

MMPMS 全称 Multi-Mapping and Posterior Mapping Selection，论文名 Generating Multiple Diverse Responses with Multi-Mapping and Posterior Mapping Selection，提出一种解决闲聊回复生成 one-to-many 的问题。  
论文地址： https://arxiv.org/pdf/1906.01781.pdf

## MMPMS 简介

闲聊对话中，一个对话上下文可以有多种多样的回复方式，被称为 one-to-many 问题。 目前业界解决 one-to-many 比较好的方法是建立 隐机制（latent mechanism），其方法大概是建立 n 个隐变量对应于生成 n 种不同的回复。这些方法虽然确实能应对 one-to-many 问题，但是其隐变量的选择没有考虑和最终生成的回复的相关性，导致其对隐机制选择的优化的学习不够。 MMPMS 延续了 隐机制（latent mechanism）称为 multi-mapping mechanism，同时为了更好的优化隐机制的选择，设计了后验映射选择（posterior mapping selection）。


## 模型介绍

编码器采用 GRU 编码

$$

h_t=[h_t;h_t]

$$