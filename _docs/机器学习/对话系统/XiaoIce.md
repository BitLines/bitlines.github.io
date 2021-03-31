---
layout:     post
title:      微软小冰解读
subtitle:   'The Design and Implementation of XiaoIce, an Empathetic Social Chatbot'
date:       2020-04-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 对话系统
---

# 微软小冰解读
在论文中作者介绍说小冰兼顾智商和情商，把人机聊天问题转化为 MDP，注重优化用户的长期参与度。  
论文地址： https://direct.mit.edu/coli/article/46/1/53/93380/The-Design-and-Implementation-of-XiaoIce-an

## 小冰基础介绍
在论文中作者介绍说小冰兼顾智商和情商，把人机聊天问题转化为 MDP，注重优化用户的长期参与度。小冰的核心模块包括：
- 对话管理器 dialogue manager
- 核心聊天 core chat
- 技能 skills
- 移情计算模块 empathetic computing module

目前小冰已经在5个国家（China, Japan, US, India, and Indonesia） 中的40多个平台上线（QQ,WeChat等)。小冰到底怎么样，来看看作者举例的对话样例：

![image](https://user-images.githubusercontent.com/80689631/112414059-5e16eb00-8d5c-11eb-8b08-64d87f89bcbe.png)

### 设计原则：IQ+EQ+personality
小冰的设计原则是综合考虑智商（能回答的难度）、情商（回答的风趣性，换位思考同理心）和个性化（千人千面）。这三个模块的内建机制为：
- IQ 能力包括知识和记忆的建模、图像和文本理解、推理、生成和预测。这些是 skills 开发的基础。小冰包括 230 skills。
- EQ 包括两个关键部件：移情 （empathy） 和社交 （social） 技能（skill）。移情的作用是换位思考，站在另一方的视角去看用户的感受，包括识别用户情感，和情感需求。需要的技术包括 查询理解、用户profile，情绪检测，情感识别，动态追踪对话。
- Personality 被定义为行为、认知和情感模式的特征集合。

### 衡量标准
和任务型对话不同的是，chatbot 的性能评价很困难（任务型对胡成功率作为指标）。小冰采用 CPS (expected Conversation-turns Per Session) 作为指标。期望对话轮数。认为对话轮数越多越好。

### 社交聊天建模为层次决策
上层决策：层次决策的最上层是选择合适的 skill 进行回复。例如（闲聊、问答、订票等skill)。  
下层决策：下层决策是具体的skill 决定采取的动作。

把决策过程建模为 MDP，在对话的每轮，chatbot 识别当前的对话状态，依照层次对话策略选择一个 skill 或者 一个response 。chatbot 的目标是寻找一个最优的策略，最大化 CPS。

### 系统架构
原文中给的架构图  
![image](https://user-images.githubusercontent.com/80689631/112414508-22305580-8d5d-11eb-9b4f-4d4ad6d0ecc2.png)

知乎大神架构图  
![image](https://user-images.githubusercontent.com/80689631/112414561-34aa8f00-8d5d-11eb-8be4-d0ee9eb173de.png)

整个系统架构从右到左分为3层：
- 数据层：基础数据，包括用户profile，小冰profile，Paired dataset， unpaired dataset等
- 对话引擎层：包括 core chat/skill，empathetic computing， global dst， dialogue policy等 
- 用户交互层：对话能力适配到不同的聊天系统中。full duplex(双工)， message-based conversations

## 对话引擎实现

### 对话管理
传统的对话管理主要是 DST + DP，因为小冰是一个开放领域的对话系统，为了让上下文连贯加入了话题管理模块，这样对话管理就包含3个组件：
- 对话状态跟踪 Global State Tracker
- 对话策略 Dialogue Policy
- 话题管理 Topic Manager

#### Global State Tracker
对话状态跟踪说直白点就是一个记忆单元，在最初时为空，在每轮对话中，保存用户utterance，小冰 response，实体以及 empathy labels （empathetic 模块计算结果）

#### Dialogue Policy
小冰的对话策略模块分为两个层级（hierarchical policy）：
- 高层策略（top-level policy） 管理全局对话，基于对话状态选择 core chat or skill 来进行回复，其实就是一个多引擎的融合
- 低层策略（low-level policies）处于各个子对话模块中，各模块实现不尽相同，但是目的都是使子模块顺畅进行，低层策略在 Core chat 和 各种 Skill 中。

高层策略基本是基于规则的，或者简单的决策树模型，高层策略设计的时候要考虑对话的连贯性，所以如果某个多轮的 skill 在上一轮被选中，那么知道这个skill结束之前，需要被持续选中。具体实现原文这样讲：  
 ![image](https://user-images.githubusercontent.com/80689631/112415768-64f32d00-8d5f-11eb-95d4-da41e07d834a.png)

低层策略比较复杂，每个模块都不一样后面描述（在CoreChat部分）

#### Topic Manager
话题管理器是一个分类器，决定在每轮是否切换话题，有个推荐器推荐一个新话题。切换换题的条件：
1. 在当前话题下没有充足的知识
2. 用户开始厌倦当前话题

话题管理器是一个树模型，采用的特征如下：  
 ![image](https://user-images.githubusercontent.com/80689631/112415883-9a981600-8d5f-11eb-9cf2-d7559335517d.png)

话题推荐分别话题挖掘和话题排序。话题挖掘是从豆瓣等开源网站爬取。话题排序同样使用树模型，特征如下：  
 ![image](https://user-images.githubusercontent.com/80689631/112415896-9ec43380-8d5f-11eb-9ede-2ccb643f44a3.png)


### 移情计算 Empathetic Computing
移情计算好比是一个大的 query process 模块，包括几个部分：
- Contextual Query Understanding（CQU）：把用户的query Q 改写为 ，命名实体识别，指代消解，句子补全等。
- User Understanding：topic 检测，Intent 检测，情感分析，观点分析，用户特征补齐
- Interpersonal Response Generation：管理response 生成的 persona。比如生成语句的年龄，情感，话题等。一些属性继承自User Understanding （话题等）, 一些可能是规则（用户情感对应回复情感），还有一些可能是profile配置（如年龄）

### Core chat
Core chat 包含 通用聊天（General Chat）和一些领域聊天（Domain Chats）。 General Chat 注重 Open Domain 的广度泛聊，Domain Chat 注重 close domain 的深入聊天。就好比生活中，有些人知识面很广，能跟你聊各种话题，有些人对某个领域非常热爱（例如漫宅）能滔滔不绝聊非常非常久。 Core chat 技术有4种：
- Retrieval-Based Generator using Paired Data
- Neural Response Generator
- Retrieval-Based Generator using Unpaired Data
- Response Candidate Ranker


#### Retrieval-Based Generator using Paired Data
FAQ 的一种回答方式。需要（Q,A）形式的数据。一部分是从网络获取，另一部分是用户和小冰对话获得。

#### Neural Response Generator
文本生成模型，给定 query 生成 response。Decoder部分除了query 也要把 Empathetic Computing 的结果融入进去。如下图  
 ![image](https://user-images.githubusercontent.com/80689631/112415204-6bcd7000-8d5e-11eb-9cd9-9db1217d8076.png)


#### Retrieval-Based Generator using Unpaired Data
这部分使用知识图谱进行query 扩展。KG由 三元组组成（h,r,t），如果  h t 和经常在一个会话中被一起讨论，那么KG就包含这个三元组。

 ![image](https://user-images.githubusercontent.com/80689631/112415254-80116d00-8d5e-11eb-955b-f72e87952094.png)

#### Response Candidate Ranker
给定 对话状态  dialogue state $s = (Q_c, C, e_Q, e_R)$ response candidate R′ 使用几个特征进行排序

 ![image](https://user-images.githubusercontent.com/80689631/112415278-8d2e5c00-8d5e-11eb-94ea-6028076b2092.png)


### Image Commenting
图片创作是一种新颖的对话模式，例如互回表情，推荐景色、海报等等，都会吸引用户的兴趣。

### Dialogue Skills
Skills 分别三种，内容创作，深入介入和任务完成：
- Content Creation 内容创作：例如写诗
- Deep Engagement：感觉可能像提供成语接龙，看图猜成语等小游戏
- 任务完成：私人助理，如查天气、订票等功能。