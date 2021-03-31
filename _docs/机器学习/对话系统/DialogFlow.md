---
layout:     post
title:      DialogFlow 试用
subtitle:   '一个很好的对话机器人产品化的例子'
date:       2020-04-02
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 对话系统
---

# DialogFlow 简介

最近由于工作需要，去调研了一些业界对话机器人产品化的案例，DialogFlow 无疑是非常优秀的。 DialogFlow 是谷歌研发的产品，可以让没有任何技术功底的人快速搭建一个对话机器人。  
产品网址： https://dialogflow.cloud.google.com/

## DialogFLow 试用
由于时间原因，没有深入去了解代码层面的内容，先就产品进行了使用。使用 DialogFlow 大概分为两个步骤
1. 创建 DialogFLow 账户
2. 在账户下面创建机器人实例

### 创建 DialogFLow 账户


Dialogflow 需要 Google 帐户才能登录。如果您已有帐户，请跳至下一部分。如果您没有Google帐户，可以使用当前的电子邮件在此处获取一个帐户，也可以使用 Gmail 注册 Google 帐户和电子邮件。
创建好了 Google 账户，就可以登录了。 登录步骤如下图：  
![image](https://user-images.githubusercontent.com/80689631/112712476-db805e00-8f0a-11eb-9c31-5a6e0c817c13.png)


### 创建和试用对话机器人

使用 Google 账户登录 DialogFlow 后，单击左侧菜单中的“创建聊天机器人”。 输入聊天机器人的名称，默认语言和默认时区，然后单击“创建”按钮，如下图：  
![image](https://user-images.githubusercontent.com/80689631/112712575-901a7f80-8f0b-11eb-9d23-ba57098895a2.png)


创建过后，可以看到左侧的Dialogflow控制台和菜单面板。页面中间将显示代理的意图列表。默认情况下，Dialogflow 聊天机器人以两个意图开头。当您的聊天机器人不了解您的用户所说的内容时，您的聊天机器人会与默认后备意图相匹配。默认欢迎意图向您的用户致意。可以更改这些以定制体验。

![image](https://user-images.githubusercontent.com/80689631/112712681-ebe50880-8f0b-11eb-8bfb-68f656d2bdd9.png)


Dialogflow模拟器位于页面的右侧。模拟器允许您通过说出或键入消息来试用聊天机器人。

后续就可以对创建的聊天机器人进行各种个性化能力的配置了。

## 框架理解

DialogFLow 主要可以配置的概念有：
- Agents：智能体，可以配置多个意图，每个意图下面完成特定的一种任务。
- Intents：意图，包含唤起事件、话术；记忆上下文；交互实体和返回话术。
- Entities：实体
- Contexts：上下文
- Events：事件
- Fulfillment：设置回调API
- Integrations

各个模块之间的组织关系如下面这个图：  
 ![image](https://user-images.githubusercontent.com/80689631/112712411-73317c80-8f0a-11eb-8f8f-9d145c67dc4b.png)