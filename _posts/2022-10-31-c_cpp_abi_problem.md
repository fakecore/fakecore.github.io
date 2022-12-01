---
layout: post
title: c/c++ ABI Problem
date: 2022-10-31 10:45:10 +0800
last_modified_at: 2022-11-09 16:48:25 +0800
tags: []
author: fakecore
author_url: 
---



事实上c/c++均没有稳定的abi.

gcc5.1之后会有abi问题.因为引入了c++11,为了保证向前兼容,额外添加了namespace去保存c++11的特性.

所以在这个前后编译的版本会存在abi问题.另外可以通过指令,使用老式abi进行编译.

```cmake
-D_GLIBCXX_USE_CXX11_ABI=0
```



## 为什么C没有ABI,在Linux上却依然可以兼容运行?

因为[LSB(linux Standard Base)](https://refspecs.linuxfoundation.org/),它定义了一套ABI兼容性布局,目标就是使程序能跨机器,跨版本,跨发行版本运行.

## 什么情况会破坏ABI兼容

	1.	修改导出函数参数
	1.	改变了虚函数的offset或者成员的顺序
	1.	添加新的虚函数
	1.	不导出或者移除一个导出类
	1.	改变类的继承
	1.	改变虚函数声明时的顺序（偏移量改变，导致调用失败）
	1.	添加新的非静态成员变量（类的内存布局改变，偏移量也发生变化）
	1.	改变非静态成员变量的声明顺序

## 不会破坏ABI兼容

1. 添加非虚函数（包括构造函数）
2. 添加新的类
3. 添加新的静态成员变量
4. 修改成员变量名称（偏移量未改变）

​	







## Reference:

1. https://www.infoq.cn/article/pqi0lyv7hhmsghkpzkji

2. https://en.wikipedia.org/wiki/Application_binary_interface

3. http://www.cppblog.com/Solstice/archive/2011/03/09/141401.aspx

4. https://www.cnblogs.com/my_life/articles/12154978.html

5. https://nextstart.online/2021/12/14/ABI/#4-%E6%80%8E%E4%B9%88%E5%81%9A%E5%88%B0abi%E5%85%BC%E5%AE%B9
