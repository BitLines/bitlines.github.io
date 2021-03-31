---
layout:     post
title:      ConvLab 代码解读
subtitle:   'DSTC8 对话评测代码框架'
date:       2020-04-04
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - 机器学习
    - 自然语言处理
    - 对话系统
---

# ConvLab 介绍
ConvLab 是支持 DSTC8 评测任务的任务型对话代码库。包括NLU/DST/DP/NLG等模块，以及一些强化学习算法。  
代码 github 地址： https://github.com/ConvLab/ConvLab

## ConvLab 简介

阅读代码之后，按照我个人的理解画出来一个系统框架图

![image](https://user-images.githubusercontent.com/80689631/112411561-14c49c80-8d58-11eb-95ee-11e21715a7c1.png)

代码组织的几个关键模块为：
- Agent：智能体，由算法、记忆组成。
    - Algorithm：提供各类强化学习算法，包括DQN/ActorCritic/PPO等
    - Memory：记忆模块，用于记录强化学习探索样本，包括Online和Offline种类
    - Agent：由 algorithm、memory和body组成。
    - Body：body 为智能体在环境中。主要是衔接数据（env）和算法模型。
- Env：环境主要处理数据集适配，管理数据读取和把模型输出文字化。实现了gym的env接口，约束动作空间和状态空间。
    - Simulator：包括UserSimulator和RuleSimulator
    - StateTracker：整理NLU或者DST的输出结果
    - KBHelper：与根据DST结果，连接数据库做数据查询。
    - State：[states],[rewards],[local_done]
    - Environment：环境由以上成员组成，包含act_set, slot_set,user,state_tracker和一些轮数等约束。
- Evaluator：结果评价方法
- Modules：提供基础模型，包括 datareader/Model和对应训练脚本
    - NLU：意图和槽
    - DST：用户动作user_action, belief_state置信状态, request_state需求状态, history对话历史。
    - DP：分类任务，输入state, 输出action
    - NLG：大多数都是模板规则生成话语。有个很大的配置文件。
    - E2E：端到端方案。
    - word_dst/word_policy：例如TRADE之类的方法，用生产方法做DST和DP的。


## 关键模块详解

### Agent

Agent 包含 algorithm、memory 和 body。 好处是几个模块职责划分清晰关系理得挺清楚的，不好的地方是  body 和 memory/agent 之间存在循环引用。不是很合理。
- algorithm：强化学习算法，DQN/A2C/PG等，包装了训练接口
- memory：记忆探索经验episode，用于存储和回放探索样本，配合模型训练
- body：描述一个智能体和在一个环境中。。

Demo代码如下：
```Python
# Agent 接口定义
class Agent(object):
    def __init__(self):
        self.body = None
        self.memory = None
        self.algorithm = None
        
        self.body.agent = self
        self.body.memory = self.memory

    def act(self, state):
        '''Standard act method from algorithm.'''
        with torch.no_grad():
            action = self.algorithm.act(state)
        return action

    def update(self, state, action, reward, next_state, done):
        pass
```

### Algorithm

Algorithm 的基类是 Reinforce，定义了强化学习算法的接口，一些 DQN 等算法继承此基类。

```Python
# Algorithm 接口定义
class Reinforce(object):
    '''算法基类，定义强化学习基础接口，包括动作选择、样本采样和训练'''
    def __init__(self):
        pass
    
    def act(self, state):
        '''根据状态 选择动作'''
        pass
    
    def sample(self, memory):
        '''从 momory 中抽样样本'''
        pass

    def train(self):
        '''执行训练过程'''
        pass
```

### Body
Body 描述一个智能体在环境中。 主要是衔接数据（env）和算法模型。Body 的作用 ：
1. 模型输入输出维数和空间推理
2. 连接智能体和环境

Body 伪代码如下
```Python
class Body:
    '''
    Body of an agent inside an environment, it:
    - enables the automatic dimension inference for constructing network input/output
    - acts as reference bridge between agent and environment (useful for multi-agent, multi-env)
    - acts as non-gradient variable storage for monitoring and analysis
    '''
    def __init__(self):
        self.memory = None
        self.agent = None
        self.env = env
```

### Env

Env主要是处理数据集，把数据集处理成词典，然后包装成为一个类似GYM的Env模块。可以理解为 DataReader + 规则限制。
- Simulator：包括UserSimulator和RuleSimulator
- StateTracker：整理NLU或者DST的输出结果
- KBHelper：与根据DST结果，连接数据库做数据查询。
- State：[states],[rewards],[local_done]
- Environment：环境由以上成员组成，包含act_set, slot_set,user,state_tracker和一些轮数等约束。

### Module

Module 主要定义一些对话系统的基本要素，包 End-to-End 的和 Pipeline 的两种方式
- Pipeline：NLU/DST/DP/NLG
- End-to-End：E2E等


#### NLU (Natural Language Understanding )
NLU类 包含 model 和 dataloader 两个部分。有独立的 train.py 和 test.py文件。

```Python
# NLU 接口定义
class NLU(object):
    def __init__(self):
        self.model = None # torch 模型
        self.dataloader = None # 数据加载器
    
    def parse(utterance, context):
        '''
        参数
        	utterance (str): 用户话术
        	context (dict): 上下文
        返回
        	result (dict): NLU结果，一般为
                {
                    "intent": "xx",
                    "slots": {
                        "k1":"v1"
                    }
                }
                为考虑可扩展性，可以改成下面这个结构
                {
                    "intent": {
                        "value": "xx",
                        "detail": [{"value": "xx", "score": 0.99}] 
                    },
                    "slots": {
                        "k1": {
                            "value": "xx",
                            "detail": [{"value": "xx", "score": 0.99}] 
                        }
                    }
                }
        ''' 
        pass
```

#### DST (Dialogue State Tracking )

DST 模块在对话系统中的作用是保持一个对话记忆，在当前轮以 用户的输入 和 NLU 解析结果为输入，决定是否要更新全局 Intent 和 Slot。

```Python

# State 定义
state = {
    'user_action': user_action,
    'belief_state': init_belief_state,
    'request_state': {},
    'history': []
}

# BeliefState 定义
{
        "police": {
            "book": {
                "booked": []
            },
            "semi": {}
        },
        "hotel": {
            "book": {
                "booked": [],
                "people": "",
                "day": "",
                "stay": ""
            },
            "semi": {
                "name": "",
                "area": "",
                "parking": "",
                "pricerange": "",
                "stars": "",
                "internet": "",
                "type": ""
            }
        },
        "attraction": {
            "book": {
                "booked": []
            },
            "semi": {
                "type": "",
                "name": "",
                "area": "",
                "entrance fee": ""
            }
        },
        "restaurant": {
            "book": {
                "booked": [],
                "people": "",
                "day": "",
                "time": ""
            },
            "semi": {
                "food": "",
                "pricerange": "",
                "name": "",
                "area": "",
            }
        },
        "hospital": {
            "book": {
                "booked": []
            },
            "semi": {
                "department": ""
            }
        },
        "taxi": {
            "book": {
                "booked": [],
                "departure": "",
                "destination": ""
            },
            "semi": {
                "leaveAt": "",
                "arriveBy": ""
            }
        },
        "train": {
            "book": {
                "booked": [],
                "people": "",
                "trainID": ""
            },
            "semi": {
                "leaveAt": "",
                "destination": "",
                "day": "",
                "arriveBy": "",
                "departure": ""
            }
        }
    }

# DialogStateTracker 接口定义
class DialogStateTracker(object):
    def __init__(self):
        self.datareader = None
        self.model = None
    
    def update(self, user_act):
        '''
        根据用户行为更新对话状态
        参数
            user_act (dict or str): 用户动作或者话语。
                当为dict型，可以包含NLU结果，当前话语，对话上下文等等信息。
        返回
            new_state (dict): 更新后的对话状态.
        '''
        pass
  
```

#### DP (Dialogue Policy)
DP 模块的作用是根据当前轮用户输入和DST，决定系统应该采取的动作。  
DP 伪代码如下
```Python
# DialoguePolicy 接口定义
class DialoguePolicy(object):
    def __init__(self):
        self.datareader = None
        self.model = None
    
    def predict(self, state):
        '''
        根据对话状态预测系统的 action
        参数
            state (dict):对话状态。内部结构见DST
                state = {
                    'user_action': user_action,
                    'belief_state': init_belief_state,
                    'request_state': {},
                    'history': []
                }
        返回
        	action (dict): 系统 act，将被用于NLG模块的输入。应为具体枚举值
        '''
        pass
```

#### NLG (Natural Language Generation)

NLG 的作用是根据当前轮用户输入、DST 结果和 DP 结果生成一段自然语言回复，返回给用户。

```Python
# NLG 接口定义
class NLG(object):
    def __init__(self):
        pass
    
    def generate(self, dialog_act):
        '''
        根据系统动作生成自然语言回复。
        参数:
            dialog_act (dict): 里面应当包含系统动作，以及当前对话状态.
        返回:
            response (str): 回复，str型
        '''
        pass
```