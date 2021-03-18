---
layout:     post
title:      C++11 并发编程之五 - future
subtitle:   
date:       2018-03-05
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - CPP
---

# c++11 并发编程之五 - future

有了前面几个小节介绍的东西，并发编程已经够用了。本节介绍的future，为异步编程创造了便利。

所有与future相关的东西，都是用来完成一次异步任务的协同。注意这里强调了一次异步任务，也就是future使用起来都像是一次性筷子，不能被第二次利用。

讲future之前，大家先看来看这样一个场景
>由于小明和小刚上课迟到了，老师对他们进行了一点惩罚。这个惩罚的内容也很简单，就是要求小明和小刚一起来打扫教室的卫生，但是要求小明负责拖地，小刚负责扫地。于是小明无奈只能等待小刚扫完地之后，才开始拖地。小明觉得一直在这里等很恼火，于是他想出来一个办法：**自己去睡觉，将来（future）小刚扫完地之后，小刚把自己叫醒，自己再拖地，这样自己就不用一直看着他傻等了（自旋等待）。岂不美哉**？

没错，这就是future的使用场景。聪明的小伙伴立马会想到，我用 condition_variable 完全可以实现这个功能啊！小明 wait, 小刚 notify_one。没错，你确实可以这样做，但是使用future 会使你的代码更精炼而优雅，为什么不花点时间来学习一下呢？

我先给大家列个清单，看看future到底提供了哪些东西：

- **future**：本身分为 future 和 shared_future。

- **future 提供者**：future库中，有三个future的提供者，其中promise
 和 packaged_task 是类, async 是函数。
 


future 需要和 future 提供者 配合来使用。上面故事里的场景中， 小明需要使用 future 来等待被唤醒， 而小刚需要 使用 future 提供者 来唤醒小明。

下面我们还是首先来看看各种接口，然后我再给大家介绍一下 3种 使用 future 和 future 提供者的方式


## future

### future

future 的作用是和 future 的提供者共享状态。 future 提供的接口如下
```c++
// future 的作用是和 future 的提供者共享状态。future 的提供者有
//  1. async
//  2. promise
//  3. packaged_task
// 除了移动构造之外，一个有效的 future 的获取方法有：
//  1. async
//  2. promise::get_future
//  3. packaged_task::get_future
template <class T>
class future
{
// 构造函数
public :
    // 默认构造，此时 future 是无效的。
    future();
    // 禁止拷贝构造
    future (const future&) = delete;
    // 允许移动构造
    future (future&& x) noexcept;
// 析构函数
public :
//成员函数
public :
    // 获得共享状态中存储的值，或者抛出共享状态中的异常。
    // 如果共享状态没有在就绪状态，阻塞当前线程直到就绪。
    // 调用前，如果 future 不是有效的，抛出 future_error 异常。
    // 调用后，future 变为无效的。
    T get();
    // 判断是否是有效的，判别是否有效的规则如下
    //  1. 默认构造时，是无效的
    //  2. 调用 async, promise::get_future 或者 packaged_task::get_future 获得的 future 是有效的
    //  3. 当调用 future::get 后，变为无效的
    bool valid() const noexcept;
    // 阻塞等待，直到共享变量变为就绪状态。当 future 是无效状态时，抛出 future_error 异常。
    void wait() const;
    // 阻塞等待一段时间，直到共享变量变为就绪状态或者超时。当 future 是无效状态时，抛出 future_error 异常。
    // 注意，当共享状态包含的是一个延期的函数 (async, 用launch::deffered，创建的)，
    // 立即返回 future_status::deferred，这一点和 wait 方法差距很大
    // 返回值的情况如下
    //  1. future_status::ready 共享变量就绪
    //  2. future_status::timeout 等待超时
    //  3. future_status::deferred 共享状态包含的是一个延期的函数
    template <class Rep, class Period>
    future_status wait_for (const chrono::duration<Rep,Period>& rel_time) const;
    // 阻塞等待一段时间，直到共享变量变为就绪状态或者超时。与 wait_for 一样。
    template <class Clock, class Duration>
    future_status wait_until (const chrono::time_point<Clock,Duration>& abs_time) const;
    // 允许移动赋值
    future& operator= (future&& rhs) noexcept;
    // 禁止拷贝赋值
    future& operator= (const future&) = delete;
    // 返回 shared_future， 调用后*this 指向的 future 变为无效的，把共享状态移交给shared_future
    shared_future<T> share();
};

template <class R&> future<R&>;     // 显式具体化 (explicit specialization) R& get();
template <>         future<void>;   // 显式具体化 (explicit specialization)) void get();
```
### shared_future

## future 提供者（future providers）

### promise 

### packaged_task

### async

跟名字一样的作用，创建一个异步任务，返回异步任务的共享状态 future。来看看接口。

```
// 不指定发射策略的重载版本， 不建议使用这个版本。因为选择的策略依赖于底层实现而变得不确定。
template <class Fn, class... Args>
future<typename result_of<Fn(Args...)>::type> async (Fn&& fn, Args&&... args);

// 指定发射策略的重载版本
template <class Fn, class... Args>
future<typename result_of<Fn(Args...)>::type> async (launch policy, Fn&& fn, Args&&... args);
```

善于思考的读者可能会有个问题，为什么要重载，而不是使用默认参数呢？这样不就不需要重载了么？

> 因为这里面有两个 c++ 语言的限制。
> 1. 指定默认参数的形参必须处于函数头的最右侧。
> 2. 带有变长参数的模板函数的变长参数必须处于模板函数头的最右侧。
> 所以，这个只能通过重载函数来实现啦。

我着重要强调的地方就是 launch policy 这个参数。取值有三种情况

1. **launch::async** 立即创建一个新的线程来执行 Fn 函数，再次注意，创建的线程并不是被 detach 的，而是 自动被 future 在某个时刻 join 。这个 join 的时间点可能在 2 个地方。1 是在返回的 future 显示调用 wait 或者 get 方法时，2 是在返回的 future 析构的时候。
2. **launch::deferred**  Fn 函数将被延期执行，开始执行的时间点是在返回的 future 显示调用 wait 或者 get 方法时。再次注意，用 wait_for 和 wait_until 并不会开始执行 Fn 函数。这种方式来使用就好像同步调用函数等待其返回一样的。
3. **launch::async|launch::deferred** 自动 launch::async 和 launch::deferre 选择一个策略，到底选择哪一个这个依赖于底层的实现。不指定发射策略的重载版本就是使用这个策略。


## future 组合使用方法

我估计上面的接口你肯定没有耐心看完，不过没关系，我开始举一些例子，来看看上面的东西怎么用，如果你对下面的代码产生了疑问，再去上面翻翻接口也是可以的。

### promise - future 模式

```c++
#include <iostream>
#include <functional>
#include <thread>
#include <future>

using namespace std;

void PrintFuture(future<int>& fut)
{
    cout << "Value of future: " << fut.get() << '\n';
}

int main ()
{
    promise<int> prom;

    future<int> fut = prom.get_future();
    // prom 只能调用一次 get_future， 否则会抛出异常。
    // 如果打开下面的注释，会抛出 future_error 异常
    // fut = prom.get_future();

    thread t(PrintFuture, ref(fut));

    // 睡眠 1000 毫秒
    this_thread::sleep_for(chrono::milliseconds(1000));

    // 通知 future。
    prom.set_value (10);
    // prom 只能调用一次 set_value， 否则会抛出异常
    // 如果打开下面的注释，会抛出 future_error 异常
    // prom.set_value (10);

    t.join();
    return 0;
}
```

补充一下，promise 并不要求先调用 get_future 再调用 set_value。就好像  promise 类里面本身包含一个成员变量 future， 当调用get_future 后， 把自己包含的 future 移动到出来

我们把上面代码中get_future  和 set_value 的位置换一下，照样可以工作

```c++
#include <iostream>
#include <functional>
#include <thread>
#include <future>

using namespace std;

void PrintFuture(future<int>& fut)
{
    cout << "Value of future: " << fut.get() << '\n';
}

int main ()
{
    promise<int> prom;

    // 通知 future。
    prom.set_value (10);
    // prom 只能调用一次set_value， 否则会抛出异常
    // 如果打开下面的注释，会抛出 future_error 异常
    // prom.set_value (10);

    future<int> fut = prom.get_future();
    // prom 只能调用一次 get_future， 否则会抛出异常。
    // 如果打开下面的注释，会抛出 future_error 异常
    // fut = prom.get_future();

    // 睡眠 1000 毫秒
    this_thread::sleep_for(chrono::milliseconds(1000));

    thread t(PrintFuture, ref(fut));

    t.join();
    return 0;
}
```

### packaged_task - future 模式


```
#include <iostream>
#include <utility>
#include <future>
#include <thread>

using namespace std;

template <class RetureType, class ...Args>
future<RetureType> Launch(packaged_task<RetureType(Args...)>& task, Args... args)
{
    // 判断 packaged_task 是否有一个共享变量
    if (task.valid())
    {
        future<RetureType> ret = task.get_future();
        // 新建线程，把 task 放到后台执行。
        thread(move(task), args...).detach();
        return ret;
    }
    // 如果 packaged_task 不包含共享变量，返回无效的 future
    return future<RetureType>();
}

int main ()
{
    auto square = [] (int x) -> int { return x * x; };
    packaged_task<int(int)> task (square);

    future<int> fut = Launch(task, 5);

    cout << "The square of 5 is " << fut.get() << ".\n";
    return 0;
}

```

### async - future 模式

```
#include <iostream>
#include <utility>
#include <future>
#include <thread>

using namespace std;

int main ()
{
    // 求平方的 lambda 函数
    auto square = [] (int x) -> int { return x * x; };
    // 创建一个异步任务，新启一个线程立即开始执行 square(5)
    future<int> fut = async(launch::async, task, 5);
    // 获得异步任务的结果
    cout << "The square of 5 is " << fut.get() << ".\n";
    return 0;
}
```

注意： 我在使用 async - future 踩到一个坑，这里也当做经验分享给大家。

我们看下面这段代码
```c++
#include <future>
#include <iostream>
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>

using namespace std;

// 任务总数
const size_t TOTAL_TASK_NUMBER = 10;

// 已经完成的任务数
atomic<size_t> finished_task_number { 0 };

// 所有任务完成的 promise
promise<void> job_promise;

struct Task
{
    void operator()()
    {
        // 睡眠100毫秒
        this_thread::sleep_for(chrono::milliseconds(100));
        // 如果所有任务完成，对 job_promise 发出通知
        if (++finished_task_number == TOTAL_TASK_NUMBER)
        {
            job_promise.set_value();
        }
    }
};

int main()
{

    vector<Task> tasks { TOTAL_TASK_NUMBER };

    future<void> job_future = job_promise.get_future();

    // 计时开始
    chrono::system_clock::time_point beg = chrono::system_clock::now();
    for (size_t i = 0; i < TOTAL_TASK_NUMBER; ++i)
    {
        future<void> task_future = async(launch::async, tasks[i]);
    } // 执行到这里需要100毫秒, 因为task_future 析构时，阻塞等待任务执行完成

    job_future.wait();
    // 计时结束
    chrono::system_clock::time_point end = chrono::system_clock::now();
    // 这里 dur 将会是 10 * 100 = 1000 毫秒。
    auto dur = chrono::duration_cast<chrono::milliseconds>(end - beg);
    cout << "Total time cost: " << dur.count() <<" ms." << endl;
}
```

如何解决这个问题呢。嗯聪明人的小伙伴可能已经想到了，就是使用 ***packaged_task - future 模式***。 把 async 修改 package_task，然后创建 thread ,并调用thread 的 detach 方法放到后台执行。

把上面的代码修改成下面这样

```c++
#include <future>
#include <iostream>
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>

using namespace std;

// 任务总数
const size_t TOTAL_TASK_NUMBER = 10;

// 已经完成的任务数
atomic<size_t> finished_task_number { 0 };

// 所有任务完成的 promise
promise<void> job_promise;

struct Task
{
    void operator()()
    {
        // 睡眠100毫秒
        this_thread::sleep_for(chrono::milliseconds(100));
        // 如果所有任务完成，对 job_promise 发出通知
        if (++finished_task_number == TOTAL_TASK_NUMBER)
        {
            job_promise.set_value();
        }
    }
};

int main()
{

    vector<Task> tasks { TOTAL_TASK_NUMBER };

    future<void> job_future = job_promise.get_future();

    // 计时开始
    chrono::system_clock::time_point beg = chrono::system_clock::now();
    for (size_t i = 0; i < TOTAL_TASK_NUMBER; ++i)
    {
        packaged_task<void()> ptask { tasks[i] };
        future<void> task_future = ptask.get_future();
        thread task_thread = thread(move(ptask));
        task_thread.detach();
    } // 执行到这里需要 0 毫秒, 因为task_future 析构时，不需要阻塞等待

    job_future.wait();
    // 计时结束
    chrono::system_clock::time_point end = chrono::system_clock::now();
    // 这里 dur 将会是 100 毫秒。
    auto dur = chrono::duration_cast<chrono::milliseconds>(end - beg);
    cout << "Total time cost: " << dur.count() <<" ms." << endl;
}

```