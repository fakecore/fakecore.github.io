---
layout: post
title: cpp生产问题汇总
date: 2022-10-20 10:07:03 +0800
last_modified_at: 2022-12-16 17:21:05 +0800
tags: []
author: fakecore
author_url: 
---



## std::bad_alloc

程序报std::bad_alloc,通过gdb简单排查,判断异常函数出在通过std::bind注册的定时程序.

结果:函数定义返回json,最后忘记添加返回语句,(gcc和msvc相关文档说道,对于这种情况,作为未定义动作).并且在CmakeLists.txt并没有添加检查返回类型的编译选项

处理结果:把函数返回类型改成void,并且给编译选项加上-Wreturn-type(发现项目已经加上,只是没有对于这些编译过程中出现的warning进行处理)

补充知识:对于有定义返回类型的函数,如果没有显示写出return,编译器可能会从eax(EAX 是"累加器"(accumulator), 它是很多加法乘法指令的缺省寄存器)或者al寄存器拿值,返回.

