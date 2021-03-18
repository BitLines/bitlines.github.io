---
layout:     post
title:      C++11 并发编程之四 - thread
subtitle:   
date:       2018-03-04
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - CPP
---

# c++11 并发编程之四 - thread

c++ 11 的 thread 库提供了 一个 线程类 thread 和 一个命名空间 this_thread。

thread 提供了线程管理的一套方法， 其作用和linux 的pthread库很相似，用OOP（Object Oriented Programming）的方式提供，用起来更加便捷。 
先来看看 thread 提供的各种接口。
```c++
class
{
// 内部类型
public :
    // thread::id 类型，默认构造的 thread::id 表示 non-joinable thread 的 id。
    // 注意 thread::id 并不是整数类型，但是重载了一些操作符来进行访问。
    // thread::id 重载了各种比较操作符 和 流输出运算符（operator <<）
    class id;
    // thread 的底层实现句柄类型
    typedef some_implementation_defined native_handle_type;
// 构造函数
public :
    // 默认构造函数
    thread() noexcept;
    // 构造一个可 joinable 的thread，函数 fn 将会在新的线程中被立即调用。
    // 注意这里的 Fn 不是右值引用，而是一种引用折叠技术。
    // 并且使用std::decay方法转换成左值的函数指针。
    template <class Fn, class... Args> 
    explicit thread (Fn&& fn, Args&&... args);
    // 禁止拷贝构造
    thread (const thread&) = delete;
    // 允许移动构造
    thread (thread&& x) noexcept;
// 析构函数
public :
    // 析构函数，这个函数要注意的地方是，当 thread 时，要确保 thread 状态是
    // non-joinable 的，否则 terminate() 函数将被调用。关于什么是 joinable 见下文
    ~thread();
//成员函数
public :
    // 允许移动拷贝
    thread& operator= (thread&& rhs) noexcept;
    // 禁止复制拷贝
    thread& operator= (const thread&) = delete;
    // 阻塞等待直到 thread 管理的 function 被执行结束为止，如果 thread 是 non-joinable 的
    // 将会抛出异常。调用之后，thread 才会是 non-joinable，也就是才能够被安全的调用析构
    void join();
    // 把 thread 管理的 function 放到后台执行，与 join 不同的地方是，不会当前的调用线程，
    // 和 join 一样， 如果 thread 是 non-joinable 的将会抛出异常。
    // 调用之后，thread 才会是 non-joinable，也就是才能够被安全的调用析构
    void detach();
    // 返回thread是否joinable，joinable表达thread是否可以被执行，
    // 当以下三种情况时，thread不是joinable的：
    //  1. thread 被默认构造函数构造
    //  2. thread 被移动出去（移动赋值给其他thread或者移动构造给其他thread）
    //  3. 在调用join或者detach之后
    bool joinable() const noexcept;
    // 返回本机器的物理并发量，可以用来自适应调整线程数量
    static unsigned hardware_concurrency() noexcept;
    // 返回 thread 的底层实现句柄
    native_handle_type native_handle();
    // 返回本线程的thread::id
    id get_id() const noexcept;
    // 交换函数
    void swap (thread& x) noexcept;
}
```

this_thread 命名空间，提供在当前线程执行的4个函数，接口看下面。

```c++
namespace this_thread
{
    // 获得当前线程的 thread::id
    thread::id get_id() noexcept;
    // 为其他线程让步。在当前需要等待其他线程完成某种操作时，
    // 可以调用该函数让步给其他线程，来创造更有利的线程调度。
    void yield() noexcept;
    // 当前线程休眠一个给定的时间段
    template <class Rep, class Period>
    void sleep_for (const chrono::duration<Rep,Period>& rel_time);
    // 当前线程休眠到指定的时间点
    template <class Clock, class Duration>
    void sleep_until (const chrono::time_point<Clock,Duration>& abs_time);
} // namespace this_thread

```

整个thread库比较简单，下面给出一段示例代码，来感受一下
```c++
#include <thread>
#include <thread>
#include <atomic>
#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

atomic_flag g_flag = { ATOMIC_FLAG_INIT };

void SayHelloWord(size_t seq)
{
    // 自旋等待
    while (g_flag.test_and_set()) {}
    // 当前线程休息100毫秒
    this_thread::sleep_for(chrono::milliseconds(100));
    // 向读者大老爷打招呼
    cout << "Hello World! "
         << "I'm the " << seq << "'th thread, "
         << "and my thread::id is " << this_thread::get_id()
         << endl;
    // 释放锁
    g_flag.clear();
}

int main()
{   
    vector<thread> threads;
    for (size_t i = 0; i < 50; ++i)
    {   
        // 创建线程，并立即执行
        threads.push_back(thread(SayHelloWord, i));
    }
    for (size_t i = 0; i < 50; ++i)
    {   
        // 阻塞等待，直到所有线程执行完毕，如果没有这一行，
        // main函数将立即退出，thread将会在 joinalble的状态下
        // 被析构，terminate()函数将被调用。
        threads[i].join();

        // 不使用join() 而是使用detach()的效果是，在这里主线程不会
        // 阻塞等待，main函数将立即退出，thread 可以被正常析构，
        // 程序也会正常退出，但是不保证所有线程的内容被执行完毕。
        // threads[i].detach();
    }
    return 0;
}
```

怎么样，是不是觉得比 pthread 看起来更优美，用起来更方面呢？不只是这样，如果你使用的是 thread 库的话，可以完美的支持***function***库提供的功能。

不只是这样！线程函数完全可以是类的***成员函数***，并且可以通过 ***std::bind*** 函数完成更加神奇的操作。

这么空谈也许你没有直观感受，还是看一段代码示例吧。

```
#include <thread>
#include <atomic>
#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

class Broadcaster
{
public :
    Broadcaster() : mFlag(ATOMIC_FLAG_INIT) {}
    ~Broadcaster() {}
public :
    void Broadcast(size_t seq, atomic<size_t> &counter)
    {
        counter.fetch_add(1UL, memory_order_relaxed);
        // 自旋等待
        while (mFlag.test_and_set()) {}
        // 当前线程休息100毫秒
        this_thread::sleep_for(chrono::milliseconds(100));
        // 向读者大老爷打招呼
        cout << "Hello World! "
             << "I'm the " << seq << "'th thread, "
             << "and my thread::id is " << this_thread::get_id()
             << endl;
        // 释放锁
        mFlag.clear();
    }
private :
    atomic_flag mFlag = { ATOMIC_FLAG_INIT };
};

int main()
{
    Broadcaster broadcaster;
    atomic<size_t> counter {0};
    vector<thread> threads;
    for (size_t i = 0; i < 50; ++i)
    {
        // 创建线程，并立即执行
        threads.push_back(thread(&Broadcaster::Broadcast, &broadcaster, i, ref(counter)));
    }
    for (size_t i = 0; i < 50; ++i)
    {
        // 阻塞等待，直到所有线程执行完毕，如果没有这一行，
        // main函数将立即退出，thread将会在 joinalble的状态下
        // 被析构，terminate()函数将被调用。
        threads[i].join();

        // 不使用join() 而是使用detach()的效果是，在这里主线程不会
        // 阻塞等待，main函数将立即退出，thread 可以被正常析构，
        // 程序也会正常退出，但是不保证所有线程的内容被执行完毕。
        // threads[i].detach();
    }
    cout << "Total broadcast time is " << counter.load(memory_order_relaxed) << endl;
    return 0;
}
```

总体而言，上面代码与原来没有特别的区别。重点要讲的谁下面这一行代码
```
thread(&Broadcaster::Broadcast, &broadcaster, i, ref(counter));
```
Broadcaster::Broadcast 是类 Broadcaster 的成员函数，因此除了```size_t seq, atomic<size_t> &counter ```这两个参数之外，还需要传递类实例对象的指针，因此这里面thread 的构造函数的参数是4个而不是3个。

Broadcaster::Broadcast 函数的 第二个参数 atomic<size_t> &counter 是个左值引用，必须要使用 std::ref 函数进行描述。