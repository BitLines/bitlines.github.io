---
layout:     post
title:      C++11 并发编程之二 - mutex
subtitle:   
date:       2018-03-02
author:     BitLines
header-img: img/post-bg-blog.jpeg
catalog: true
tags:
    - CPP
---

# C++11 并发编程之二 - mutex

mutex，顾名思义就是互斥变量，用来提供线程间同步的方法。c++ 11 的 mutex 库提供了 4 种互斥变量 mutex，两个管理锁资源的lock，和三个函数。

四种mutex分别是：

- **mutex** *基础mutex*
- **recursive_mutex** *递归mutex*
- **timed_mutex** *计时mutex*
- **recursive_timed_mutex** *递归计时mutex*

两种管理锁资源的lock分别是：

- **lock_guard** *基础的RAII（Resource Acquisition Is Initialization）锁管理*
- **unique_lock** *包括lock_guard的所有功能，在此基础上提供了更灵活的锁管理功能，推荐使用*

三个函数分别是：
- **try_lock** *按顺序同时尝试对多个mutex加锁，失败返回第一个加锁失败的mutex的下标，成功返回-1*
- **lock** *按顺序同时对多个mutex加锁，阻塞等待直到获得所有mutex的锁*
- **call_once** *多次使用该方法调用函数，可以保证函数只被调用一次*

下面依次对上面提到的内容做详细的介绍，我保证，看完了你就知道怎么用啦。

## mutex

mutex 的声明类似下面这样
```c++
class mutex
{
public :
    // 底层实现句柄类型
    typedef some_handle_type native_handle_type;
public :
    // 默认构造
    mutex();
    // 禁止拷贝构造和移动构造
    mutex(const mutex&) = delete;
public :
    // 加锁，阻塞等待，直到获得锁
    void lock();
    // 尝试加锁，立即返回是否加锁成功
    bool try_lock();
    // 解锁。注意，互斥变量必须是被锁定状态，否则行为未定义
    void unlock();
    // 获取底层实现句柄
    native_handle_type native_handle();
};
```

看起来也比较简单，不详细介绍了。

## recursive_mutex

recursive_mutex 提供的方法与mutex完全一样。与 mutex 的差别在于其递归的特性。具体来说就是，同一线程内，可以对 recursive_mutex 重复加锁，锁的释放次数应该和获得次数一样。使用场景可以是占有锁的函数的递归调用。

## timed_mutex
timed_mutex 比 mutex 多添加了计时的特性，在获得锁的时候可以指定等待一段时间或者等待直到某个时间点。具体提供的方法来看下面

```c++
class timed_mutex
{
public :
    // 底层实现句柄类型
    typedef some_handle_type native_handle_type;
public :
    // 加锁，阻塞等待，直到获得锁
    void lock();
    // 尝试加锁，立即返回是否加锁成功
    bool try_lock();
    // 尝试加锁，阻塞等待直到超时，返回是否加锁成功
    template <class Rep, class Period>
    bool try_lock_for (const chrono::duration<Rep,Period>& rel_time);
    // 尝试加锁，阻塞等待直到超时，返回是否加锁成功
    template <class Clock, class Duration>
    bool try_lock_until (const chrono::time_point<Clock,Duration>& abs_time);
    // 解锁。注意，互斥变量必须是被锁定状态，否则行为未定义
    void unlock();
    // 获取底层实现句柄
    native_handle_type native_handle();
};
```

## recursive_timed_mutex
recursive_timed_mutex 从名字就可以看出来是 timed_mutex 和 recursive_mutex 的结合体，其实真的就是这样子！不详细讲啦。

## lock_guard
lock_guard 只有构造函数和析构函数，简单的RAII。其构造函数给互斥变量加锁，析构函数释放锁。并不负责互斥变量生命周期的管理。 lock_guard 接口如下：

```c++
template <typename Mutex>
class lock_guard
{
// 内部类型
public :
    typedef Mutex mutex_type;
// 构造函数
public :
    // 加锁构造。lock_guard 管理 m。 构造时，调用 m 的 lock方法，
    // 阻塞当前线程直到获得 m 的锁。
    explicit lock_guard (mutex_type& m); 
    // 适应构造。构造前，m 必须是已经被锁定的状态, 不再调用 lock 方法。
    lock_guard (mutex_type& m, adopt_lock_t tag);
    // 禁止拷贝构造和移动构造
    lock_guard (const lock_guard&) = delete;
// 析构函数
public :
    // 析构时，调用 m 的unlock方法。
    ~lock_guard();

};
```

对于上面的适应构造，为了不留坑在这里，还是举个例子保险，不要打我，我确实啰嗦了一点，请看代码。

```
#include <iostream>
#include <mutex>

using namespace std;

mutex mtx;

void thread_1()
{
    while (true)
    {   
        // 1. 把 mtx 锁定
        // 2. 使用适应构造
        mtx.lock();
        lock_guard<mutex> lck(mtx, adopt_lock);
        // do someting
    }   
}

void thread_2()
{
    while (true)
    {   
        // 直接使用加锁构造
        lock_guard<mutex> lck(mtx);
        // do someting
    }   
}
```

lock_guard 使用起来很简单。来，再看个例子巩固一下。我们结合 lock_guard 和 recursive_mutex， 使例子不那么单调。 (\*\^▽^\*\)

```
#include <iostream>
#include <mutex>
#include <queue>

using namespace std;

class SyncQueue
{
public :
    explicit SyncQueue(size_t limit = 0) : mLimit(limit) {}
    ~SyncQueue() {}
public :
    bool Push(int x)
    {   // 获得锁
        lock_guard<recursive_mutex> lock(mMtx);
        if (mLimit && this->GetSize() >= mLimit) { return false; }
        mData.push(x);
        return true;
    }   
    bool Pop(int &x) 
    {   
        // 获得锁
        lock_guard<recursive_mutex> lock(mMtx);
        // 这里对 recursive_mutex 进行了二次加锁
        if (0 == this->GetSize()) { return false; }
        x = mData.front();
        mData.pop();
        return true;
    }   
    size_t GetSize()
    {   
        // 获得锁
        lock_guard<recursive_mutex> lock(mMtx);
        return mData.size();
    }   
private :
    queue<int> mData;
    recursive_mutex mMtx;
    size_t mLimit;
};
```

## unique_lock 
unique_lock 的作用和 lock_guard。 只不过提供了比 lock_guard 更灵活的 mutex 管理方法。lock_guard 只提供了最普通的RAII，也只有简单的构造函数和析构函数，unique_lock 除此之外，提供了 timed_mutex 的一些功能，可以指定等待一段时间或者等待直到某个时间点。看其名字，跟unique_ptr，类似，确实也有类似的功能，对一个mutex提供一个唯一管理的实例，并且可以进行移动拷贝和移动构造。但是 unique_lock 也不负责管理mutex的生命周期，要自己保证互斥变量的生命周期长于 unique_lock 。 废话不多说，看看接口就明白了

```c++
template <typename Mutex>
class unique_lock
{
// 内部类型
public :
    typedef Mutex mutex_type;
// 构造函数
public :
    // 加锁构造。lock_guard 管理 m。 构造时，调用 m 的 lock方法，
    // 阻塞当前线程直到获得 m 的锁。
    explicit unique_lock (mutex_type& m); 
    // 适应构造。构造前，m 必须是已经被锁定的状态, 不再调用 lock 方法。
    unique_lock (mutex_type& m, adopt_lock_t tag);
    // 禁止拷贝构造和移动构造
    unique_lock (const lock_guard&) = delete;
// 析构函数
public :
    // 析构时，如果 m 是被锁定的状态，则调用 m 的unlock方法。
    ~unique_lock();
// 加锁解锁
public :
    // 加锁，阻塞等待，直到获得锁
    void lock();
    // 尝试加锁，立即返回是否加锁成功
    bool try_lock();
    // 尝试加锁，阻塞等待直到超时，返回是否加锁成功
    template <class Rep, class Period>
    bool try_lock_for (const chrono::duration<Rep,Period>& rel_time);
    // 尝试加锁，阻塞等待直到超时，返回是否加锁成功
    template <class Clock, class Duration>
    bool try_lock_until (const chrono::time_point<Clock,Duration>& abs_time);
    // 解锁。注意，互斥变量必须是被锁定状态，否则行为未定义
    void unlock();
// 修改方法
public :
    // 支持移动赋值
    unique_lock& operator= (unique_lock&& x) noexcept;
    // 禁止拷贝赋值
    unique_lock& operator= (const unique_lock&) = delete;
    // 和另一个 unique_lock 交换
    void swap (unique_lock& x) noexcept;
    // 返回管理的互斥变量的指针, 并且不再对其进行管理。
    mutex_type* release() noexcept;
// 观察方法
public :
    // 判断当前是否获得了锁。
    bool owns_lock() const nexept;
    // 同owns_lock。
    explicit operator bool() const noexcept;
    // 返回管理的互斥变量的指针
    mutex_type* mutex() const noexcept;
};
```

OK， 我知道你觉得一堆函数看起来很晕，不过耐心看完的话，是不是觉得功能很齐全。记不住没关系，用的时候去查查API就可以了。如果只是使用RAII的话，unique_lock 和 lock_guard 可以看做是等价的。所以上面给出的lock_guard的代码示例，对于 unique_lock 同样适用。这里就不再举例了。

## 外部函数

```c++

// 按顺序同时尝试对多个mutex加锁，失败返回第一个加锁失败的mutex的下标，成功返回-1。

template <class Mutex1, class Mutex2, class... Mutexes>
int try_lock (Mutex1& a, Mutex2& b, Mutexes&... cde);

// 按顺序同时对多个mutex加锁，阻塞等待直到获得所有mutex的锁
template <class Mutex1, class Mutex2, class... Mutexes>
void lock (Mutex1& a, Mutex2& b, Mutexes&... cde);

// 对同一个 once_flag 变量调用 call_once，保证 call_once 只被执行一次。调用 call_once 的效果是，
//  1. 如果没有其他线程已经对同一个 once_flag 正在调用或者调用完成 call_once，则执行 Fn 函数，并等待其执行完成
//  2. 如果已经有一个其他线程对同一个 once_flag调用完成 call_once，则不再执行 Fn 直接返回
//  3. 如果存在有一个其他线程对同一个 once_flag 正在执行 Fn 函数，则阻塞当前线程，直到其他线程执行Fn 完成。
// 眼前一亮，这简直就是自带单例功能嘛。
template <class Fn, class... Args>
void call_once (once_flag& flag, Fn&& fn, Args&&... args);
```

对 try_lock 和 lock 就不讲了，下面附上一段单例模式的示例代码，感受一下 call_once 函数有多么好用

```
#include <mutex>

using namespace std;

class Singleton
{
// 构造函数
private :
    // 禁止构造
    Singleton() {}
// 析构函数
public :
    ~Singleton() {}
// 静态方法
public :
    // 获取实例
    static Singleton * GetInstance();
// 私有方法
private :
    // 构造实例
    static void createInstance();
// 私有变量
private :
    static Singleton * sInstance;
    static once_flag sOnceFlag;
};

Singleton * Singleton::sInstance = nullptr;

once_flag Singleton::sOnceFlag;

void Singleton::createInstance()
{
    sInstance = new Singleton();
}

Singleton * Singleton::GetInstance()
{
    // 保证了该类的对象只被生成一次。
    call_once(sOnceFlag, createInstance);
    return sInstance;
}
``` 