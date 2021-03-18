---
layout:     post
title:      C++11 并发编程之一 - atomic
subtitle:   
date:       2018-03-01
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - CPP
---

# c++11 并发编程之一 - atomic

atomic 的作用是什么呢？避免多线程访问数据竞争，解决多线程之间访问数据的线程安全问题。 atomic 库提供了原子变量类型，对其的访问使用原子原语，保证效率的同时来解决线程之间的数据竞争问题。

## memory_order

搞明白 memory_order 的作用是什么之前，首先要清楚它要解决什么样的问题。

先来看一段代码

```c++
int x = 0, y = 0;
int a, b;
void foo()
{
    x = 1;
    a = y;
}

void bar()
{
    y = 1;
    b = x;
}
```

上面这段代码，在单线程顺序调用 foo 和 bar 的情况下，a 和 b 的结果分别是 0 和 1。但是，在两个线程并行执行 foo 和 bar 的时候 a 和 b 的值有哪些种可能呢？
>答案是 (0, 0)、(0, 1)、(1, 0) 甚至是 (1, 1) 都有可能。

Oh, my god! 是不是编译器出了bug。不然怎么会这样，感觉(1, 1) 这种组合完全不合理啊。为什么(1, 1)这种组合会出现呢？

>因为 a = y 没有用到 x = 1 的写结果，不存在依赖关系，使用-o2 选项进行编译的时候，编译器会使用流水线并发执行他们，甚至可能重新排列指令，把 a = y 放到 x = 1 之前来执行。代码语句可以画出一个有向无环图，如果两个语句同时访问了相同的变量，那么他们之间将会有依赖关系，代码语句的实际执行顺序可以是这个有向无环图的任意拓扑排序结果。

下面来我给大家画个图一切答案将浮出水面。首先在单线程顺序调用 foo 和 bar 的情况如下图：

 ![foobar_1.png](https://gw.alipayobjects.com/zos/skylark/9339b560-8129-44dc-ae97-5a2fdd7801c6/2018/png/59d22983-e2df-4851-be67-3f4eac9f16e0.png) 
 


b = x; 依赖于 x = 1; 而 y = 1; 依赖于 a = y; 因此 a 和 b 结果只能是 (0, 1)

在多线程并行执行的时候，foo 和 bar 的情况如下图：

 ![foobar_2.png](https://gw.alipayobjects.com/zos/skylark/562fe048-746a-492d-95a0-3296d60cc711/2018/png/75d9ebe9-e4d6-4da7-8906-3df6e7a585cc.png) 
 
可以看到4条语句之间没有任何依赖关系，因此 4 条语句的执行顺序是任意的。没错就是任意的。

天哪。细思极恐！你是不是觉得自己以前写的代码经不起仔细推敲，仿佛在多线程并发执行的情况下，一切都没有了保证？

不要慌，我给你介绍完 happens-before （先发生于） 之后，相信你就不再迷茫了。

什么是 happens-before？
> 通俗的来讲，如果 A happens-before B, 那么在 B 执行之前， A 已经完成了对内存的修改。

因此只要你确定 A happens-before B， 那么你可以很容易判断出 B 的结果。不好意思，这个概念看起来简单，但是实际在多线程的情况下还是比较复杂的，更加很不幸的是，要搞清楚这个概念，需要引入额外的其他几个概念。让暴风雨来的猛烈一点，我要一口气吐出好多概念了。

### sequenced-before （先序于）

sequenced-before 可以粗略理解为在同一线程中代码的先后执行顺序。可以使用我上面给大家说的有向无环图的思路，判断 A 是否是 B 的前驱，来确定是否满足 A is sequenced-before B。深入理解 sequenced-before 起来还是比较复杂的，如果要深入研究请查阅相关资，这里不详细介绍了，[不过附上链接吧](http://en.cppreference.com/w/cpp/language/eval_order)。

### carries dependency （携带依赖）

A carries dependency into B （ B 依赖于 A ）的条件是，在同一线程中，若下列任一条件为真

1. A 的值被用作 B 的运算数，除非
    1. B 调用了 std::kill_dependency

    2. A 是 ```&&``` 、 ```||``` 、 ```?:``` 或 ```,``` 等运算符的左运算数。
2. A 向标量 M 做写入操作，B 从标量 M 做读取操作
3. A  A carries dependency into X 并且 X  A carries dependency into B（传递性）

carries dependency 是 sequenced-before 的充分条件。

### dependency-ordered before （依赖先序于）

A is dependency-ordered before B 的条件是， 要满足下面两个条件任意一个：
1. 在一个线程中，A 对 原子对象 M 做了 release store，在另一个线程中，B 对 原子对象 M 做了consume load，并且 B 中读取了 A 中任意部分写入的值。
2. A is dependency-ordered before X 并且 X carries a dependency into B.（这一条往往对最小粒度使用内存模型起到关键作用，注意这里是 carries dependency 而不是 sequenced-before）

### inter-thread happens-before （线程间先发生于）
inter-thread happens before 关系，是理解 happens-before 关系的关键所在。inter-thread happens before 描述了多线程之间的 happens-before 关系。在多线程之间，A inter-thread happens before B的条件是， 如果下面任意条件之一满足：
1) A synchronizes-with B
2) A is dependency-ordered before B
3) A synchronizes-with  X 并且 X is sequenced-before B
3) A is sequenced-before  X 并且 X inter-thread happens-before B
4) A inter-thread happens-before X 并且  X inter-thread happens-before B （传递性）

### happens-before
好了难啃的骨头终须啃完了。如果你把上面的概念都理清楚了，那么再回到 happens-before 就变得很简单了。 happens-before 关系可以分两种情况讨论

- 在同一个线程内，满足 sequenced-before 
- 在多个线程之间，满足 inter-thread happens-before

感觉我在说废话，23333。

哦，差不多搞定了，你如果看完你就是神仙了！但是你如果反复看上面的东西，你一定会骂我的。`'$#&%*.^， 什么是 A synchronizes-with B？ 这个你怎么遗漏了？不说清楚这个你怎么就得到 happens-before 了概念了？网上大家感觉有好几种答案。不过我对这些答案做了仔细的对比，深入的思考，基本能肯定下面这两个情形就是 synchronizes-with：

1. 对同一个 mutex 的一对 lock 和 unlock
2. 对同一个 atomic 的一对 store 和 load

不要问我为什么，哥只是传说。

绕了一圈子，背景知识已经介绍的差不多了，回过头来讲讲 memory_order。 根据我的理解，memory_order 的作用就是来指定 原子内存访问和其上下文中其他内存访问的执行顺序。这相当于在上面介绍的有向无环图中，在原子内存访问和其上下文中的非原子内存访问之间加入依赖关系，为 sequenced-before 打了一个补丁，帮助确定 happens-before 关系。

```c++
typedef enum memory_order {
    // 原子内存访问和其上下文中其他内存访问没有同步或顺序制约，
    // 仅对此原子内存访问要求原子性，多用于计数器，例如 shared_ptr
    memory_order_relaxed, 
    // 有此内存顺序的原子 load 操作，此原子内存访问语句后面的其他依赖于
    //该原子操作的某个值内存访问（包括读和写），
    //在当前线程中不能被重新排列到此原子内存访问之前。
    memory_order_consume,
    // 有此内存顺序的原子 load 操作，对其上下文的其他内存访问有这样的约束：
    // 此原子内存访问语句后面的其他内存访问语句（包括读和写），
    // 在当前线程中不能被重新排列到此原子内存访问之前。
    memory_order_acquire,
    // 有此内存顺序的原子 store 操作，对其上下文的其他内存访问有这样的约束：
    // 此原子内存访问语句前面的其他内存访问语句（包括读和写），
    // 在当前线程中不能被重新排列到此原子内存访问之后。
    memory_order_release,
    // 同时具备 memory_order_release 和 memory_order_acquire
    memory_order_acq_rel,
    // load 时具备 memory_order_acquire，
    // store时具备 memory_order_release
    // raw( read and write 读取然后写入) 具备 memory_order_acq_rel
    // 所有由此内存顺序的原子访问，可以在全局上进行一个全序排列
    memory_order_seq_cst
} memory_order;

```

## 使用限制

### load
- memory_order_relaxed
- memory_order_acquire
- memory_order_consume
- memory_order_seq_cst

### store
- memory_order_relaxed
- memory_order_release
- memory_order_seq_cst

### read modify write
- memory_order_relaxed
- memory_order_acquire
- memory_order_consume
- memory_order_release
- memory_order_acq_rel
- memory_order_seq_cst

## momery_order 的使用方式

### Relaxed ordering
```
// Thread 1:
r1 = y.load(memory_order_relaxed); // A
x.store(r1, memory_order_relaxed); // B
// Thread 2:
r2 = x.load(memory_order_relaxed); // C 
y.store(42, memory_order_relaxed); // D
```

修改一下

```
// Thread 1:
r1 = x.load(memory_order_relaxed);
if (r1 == 42) y.store(r1, memory_order_relaxed);
// Thread 2:
r2 = y.load(memory_order_relaxed);
if (r2 == 42) x.store(42, memory_order_relaxed);
```

计数器
```
#include <vector>
#include <iostream>
#include <thread>
#include <atomic>

using namespace std;

atomic<int> cnt = { 0 };
 
void foo()
{
    for (int n = 0; n < 1000; ++n)
    {
        // 这里使用fetch_add(1, memory_order_relaxed) 和使用 operator++ 是有差别的，
        // 差别在于 operator++ 使用 memory_order_seq_cst
        cnt.fetch_add(1, memory_order_relaxed);
    }
}
 
int main()
{
    vector<thread> threads;
    for (int n = 0; n < 10; ++n)
    {
        threads.emplace_back(foo);
    }
    for (auto& t : threads)
    {
        t.join();
    }
    cout << "Final counter value is " << cnt << '.\n';
}
```
### Release-Acquire ordering

```
#include <thread>
#include <atomic>
#include <cassert>
#include <string>

using namespace std;

atomic<string*> ptr;

int data;

void Produce()
{
    string* p1  = new string("Hello");
    data = 42;
    ptr.store(p1, memory_order_release);
}

void Consume()
{
    string* p2;
    while (!(p2 = ptr.load(memory_order_acquire))) { }
    // 永真断言
    assert(*p2 == "Hello");
    // 永真断言
    assert(data == 42);
}

int main()
{
    thread t1(Produce);
    thread t2(Consume);
    t1.join();
    t2.join();
}
```

### Release-Consume ordering
```
#include <thread>
#include <atomic>
#include <cassert>
#include <string>

using namespace std;

atomic<string*> ptr;

int data;

void Produce()
{
    string* p1  = new string("Hello");
    data = 42;
    ptr.store(p1, memory_order_release);
}

void Consume()
{
    string* p2;
    while (!(p2 = ptr.load(memory_order_consume))) { }
    // 永真断言
    assert(*p2 == "Hello");
    // 不确定断言，可能真也可能假
    assert(data == 42);
}

int main()
{
    thread t1(Produce);
    thread t2(Consume);
    t1.join();
    t2.join();
}
```

理解 load 的 memory_order_relaxed memory_order_consume 和 memory_order_acquire 之间的差异还是需要冷静一下的。

- memory_order_relaxed 和 memory_order_acquire 的差别还是很明显的
- memory_order_relaxed 和 memory_order_consume 我觉得主要差别在于 memory_order_consume 不能用于store
- memory_order_consume 和 memory_order_acquire：memory_order_consume 不限制其后续内存访问不能重排到其前面。

### Sequentially-consistent ordering

```
#include <atomic>

using namespace std;

// 自旋锁，使用 atomic_flag 可以实现一个很简单的版本
class SpinMutex
{
public :
    SpinMutex() : mFlag(ATOMIC_FLAG_INIT)
    {
    }
    ~SpinMutex()
    {
    }
public :
    void Lock()
    {
        while (mFlag.test_and_set(memory_order_seq_cst)) {}
    }
    void Unlock()
    {
        mFlag.clear(memory_order_seq_cst);
    }
private :
    atomic_flag mFlag;
};
```