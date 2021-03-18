---
layout:     post
title:      C++11 并发编程之三 - condition_variable
subtitle:   
date:       2018-03-03
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - CPP
---

# c++11 并发编程之三 - condition_variable

条件变量是并发程序设计中的一种控制结构。多个线程访问一个共享资源(或称临界区)时，不但需要用互斥锁实现独享访问以避免并发错误(称为竞争危害)，在获得互斥锁进入临界区后还需要检验特定条件是否成立：

- (1)、如果不满足该条件，拥有互斥锁的线程应该释放该互斥锁，把自身阻塞(block)并挂到(suspend)条件变量的线程队列中

- (2)、如果满足该条件，拥有互斥锁的线程在临界区内访问共享资源，在退出临界区时通知(notify)在条件变量的线程队列中处于阻塞状态的线程，被通知的线程必须重新申请对该互斥锁加锁。

C++11的标准库中新增加的条件变量的实现，与pthread的实现语义完全一致。使用条件变量做并发控制时，某一时刻阻塞在一个条件变量上的各个线程应该在调用wait操作时指明同一个互斥锁，此时该条件变量与该互斥锁绑定；否则程序的行为未定义。条件变量必须与互斥锁配合使用，其理由是程序需要判定某个条件(condition或称predict)是否成立，该条件可以是任意复杂。

离开临界区的线程用notify操作解除阻塞(unblock)在条件变量上的各个线程时，按照公平性(fairness)这些线程应该有平等的获得互斥锁的机会，不应让某个线程始终难以获得互斥锁被饿死(starvation)，并且比后来到临界区的其它线程更为优先(即基本上FIFO)。一种办法是调用了notify_all的线程保持互斥锁，直到所有从条件变量上解除阻塞的线程都已经挂起(suspend)到互斥锁上，然后发起了notify_all的线程再释放互斥锁。互斥锁上一般都有比较完善的阻塞线程调度算法，一般会按照线程优先级调度，相同优先级按照FIFO调度。

发起notify的线程不需要拥有互斥锁。即将离开临界区的线程是先释放互斥锁还是先notify操作解除在条件变量上挂起线程的阻塞？表面看两种顺序都可以。但一般建议是先notify操作，后对互斥锁解锁。因为这既有利于上述的公平性，同时还避免了相反顺序时可能的优先级倒置。这种先notify后解锁的做法是悲观的(pessimization)，因为被通知(notified)线程将立即被阻塞，等待通知(notifying)线程释放互斥锁。很多实现(特别是pthreads的很多实现)为了避免这种”匆忙与等待”(hurry up and wait)情形，把在条件变量的线程队列上处于等待的被通知线程直接移到互斥锁的线程队列上，而不唤醒这些线程。

condition_variable 提供了两个类，一个等待状态描述枚举，和一个函数

两个类：
- **condition_variable** *条件变量类*
- **condition_variable_any** *同样是条件变量类，与condition_variable的差别在于，和condition_variable配合使用的锁类型只能是unique_lock，而condition_variable_any 可以使用任意的锁类型。嗯如果你没有特别的理由，建议使用 condition_variable 就足够了。使用 condition_variable_any 的场景可能是用户自己写了一套lock类型，这样可以配合 condition_variable_any 来使用* 

等待状态描述枚举 ：
- **cv_status** *condition_variable 的 wait_for 和 wait_until 的返回值类型，描述等待后的状态*

一个函数 ：

- **notify_all_at_thread_exit** *在当前线程退出时，通知其他所有正在等待的条件变量。*


好了说了这么多，我知道你已经有点看吐了。不如我们还是先看看接口，然后参照接口进一步介绍一下使用方式。

## condition_variable 

基础的 condition_variable 接口如下：

```
class 
{
// 构造函数
public :
    // 默认构造
    condition_variable();
    // 禁止拷贝构造和移动构造
    condition_variable (const condition_variable&) = delete;
// 析构函数
public :
    // 析构函数，在析构之前，要确保没有线程在wait中，析构之后不能再调用wait。
    ~condition_variable();
// 等待方法
public :
    // 阻塞当前线程，直到获得通知。调用前 lck 应该满足 owns_lock。
    // 当调用 wait 时，该函数先调用 lck 的unlock函数释放锁，
    // 然后阻塞线程直到获得通知。获得通知后，会调用lck的 lock方法，
    // 把lck 锁定，然后进入临界区。
    void wait (unique_lock<mutex>& lck);
    
    // 阻塞当前线程，直到获得通知。调用前 lck 应该满足 owns_lock。
    // 当调用 wait 时，该函数先调用 lck 的unlock函数释放锁，
    // 然后阻塞线程直到获得通知。获得通知后，会调用lck的 lock方法，
    // 把 lck 锁定，然后判断谓词 pred 是否为真，如果是则进入临界区，
    // 否则重新释放 lck 锁，继续等待通知。这个函数的行为类似于
    // while (!pred()) wait(lck);
    template <class Predicate>
    void wait (unique_lock<mutex>& lck, Predicate pred);
    
    // 阻塞当前线程一段时间，直到获得通知或者超时，返回等待的状态。
    // 其他与 wait 一样
    template <class Rep, class Period>
    cv_status wait_for (unique_lock<mutex>& lck,
        const chrono::duration<Rep,Period>& rel_time);
    template <class Rep, class Period, class Predicate>
    bool wait_for (unique_lock<mutex>& lck,
        const chrono::duration<Rep,Period>& rel_time, Predicate pred);
    
    // 阻塞当前线程到一个时间点，直到获得通知或者超时。返回等待的状态
    // 其他与 wait 一样
    template <class Clock, class Duration>
    cv_status wait_until (unique_lock<mutex>& lck,
        const chrono::time_point<Clock,Duration>& abs_time);
    template <class Clock, class Duration, class Predicate>
    bool wait_until (unique_lock<mutex>& lck,
        const chrono::time_point<Clock,Duration>& abs_time, Predicate pred);
// 通知方法
public :
    // 把其他在等待该条件变量的某一个线程唤醒，如果没有线程出于等待状态，则不做任何事
    void notify_one() noexcept;
    // 把其他在等待该条件变量的所有线程唤醒，如果没有线程出于等待状态，则不做任何事
    void notify_all() noexcept;

};
```


里面 notify_one 和 notify_all 的差别是，notify_one只唤醒一个等待的条件变量，而 notify_all 将唤醒所有等待的条件变量。来看一个例子能更直观一些
```c++
#include <iostream>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>
#include <thread>

using namespace std;

condition_variable g_cond_var;

mutex g_mtx;

int resource = 0;

bool IsResourceReady()
{
    return resource > 0;
}

void Consume()
{
    unique_lock<mutex> lock(g_mtx);
    // 等待获得资源的通知
    g_cond_var.wait(lock, IsResourceReady);
    // 消费一个资源
    resource -= 1;
    cout << "get" << endl;
}

int main()
{
    vector<thread> consumers {2};
    consumers[0] = thread(Consume);
    consumers[1] = thread(Consume);

    // 先让两个消费者阻塞等待通知
    this_thread::sleep_for(chrono::milliseconds(1000));

    // 生产2个资源
    resource = 2;

    // 调用 notify_all， 2个消费者都可以被唤醒，并且获取到资源
    g_cond_var.notify_all();

    // 如果调用 notify_one， 2个消费者只有其中某1个可以被唤醒
    // 并且获取到资源，另一个将无限等待。
    //g_cond_var.notify_one();

    consumers[0].join();
    consumers[1].join();
}
```

condition_variable简直就是 生产者-消费者 模式的一个利器。来来来，我们把前面一节的同步队列的例子，拿出来使用 condition_variable 来翻新一下。

```c++
#include <iostream>
#include <mutex>
#include <condition_variable>
#include <queue>

using namespace std;

class SyncQueue
{
public :
    explicit SyncQueue(size_t limit = 0) : mLimit(limit) {}
    ~SyncQueue() {}
public :
    void Push(int x)
    {
        unique_lock<mutex> lock(mMtx);
        // 等待 isNotFull 发生
        mFullConditionVariable.wait(lock, bind(&SyncQueue::isNotFull, this));
        mData.push(x);
        // 唤醒 Pop 方法中的 mEmptyConditionVariable.wait 函数，
        // 让其重新检查 isNotEmpty 是否发生。
        mEmptyConditionVariable.notify_one();
    }
    void Pop(int &x)
    {
        unique_lock<mutex> lock(mMtx);
        // 等待 isNotEmpty 发生
        mEmptyConditionVariable.wait(lock, bind(&SyncQueue::isNotEmpty, this));
        x = mData.front();
        mData.pop();
        // 唤醒 Push 方法中的 mFullConditionVariable.wait 函数，
        // 让其重新检查 isNotFull 是否发生。
        mFullConditionVariable.notify_one();
    }
    size_t GetSize()
    {
        lock_guard<mutex> lock(mMtx);
        return mData.size();
    }
private :
    inline bool isNotFull() const
    {
        return 0 == mLimit || mData.size() < mLimit;
    }
    inline bool isNotEmpty() const
    {
        return !mData.empty();
    }
private :
    queue<int> mData;
    mutex mMtx;
    size_t mLimit;
    condition_variable mFullConditionVariable;
    condition_variable mEmptyConditionVariable;
};
```

怎么样，理解了没有？

## condition_variable_any
condition_variable_any 的功能与 condition_variable 完全一致。差别在于和condition_variable配合使用的锁类型只能是unique_lock，而condition_variable_any 可以配合任意的锁类型来使用。嗯如果你没有特别的理由，建议使用 condition_variable 就足够了。

使用 condition_variable_any 的场景可能是用户自己写了一套lock类型（例如自旋锁），这样可以配合 condition_variable_any 来使用。

例子就不再介绍啦。

## cv_status
cv_status是一个枚举类型，用来描述 condition_variable 和 condition_variable_any 的 wait_for 和 wait_until 方法的等待状态，亦是它们的返回值类型。
```
enum class cv_status
{
    // 没有超时，等待成功
    no_timeout,
    // 超时，等待失败
    timeout
};
```

## 外部函数
```
// 作用有些类似 RAII，控制范围是当前的线程内。
// 在当前线程结束后，通知所有其他等待条件变量 cond 的线程，
// 并且释放 lck 锁。其行为是
//   lck.unlock();      // 1
//   cond.notify_all(); // 2
void notify_all_at_thread_exit (condition_variable& cond, unique_lock<mutex> lck);
```
