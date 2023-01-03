---
layout: post
title: memcpy!为什么那么快!
date: 2022-10-27 10:56:37 +0800
last_modified_at: 2022-12-17 02:32:09 +0800
tags: []
author: fakecore
author_url:
---

相信学过c/c++的对这个函数都不会陌生.拷贝一段内存时,我们通常会使用memcpy或者循环拷贝.

只是大家想过没有,为什么memcpy那么快,它到底藏了什么魔法?

memcpy会使用SIMD指令,做多字拷贝.

正常我们写循环拷贝都是按照基础类型本身来进行,单次拷贝可能是在1-4byte之间.但是memcpy按照4byte进行拷贝.所以它的拷贝速度会比较快.



## SIMD

单指令流多数据流是一种采用一个控制器来控制多个处理器，同时对一组数据中的每一个分别执行相同的操作从而实现空间上的并行性的技术。 在微处理器中，单指令流多数据流技术则是一个控制器控制多个平行的处理微元，例如Intel的MMX或SSE，以及AMD的3D Now!指令集。

## 如何比memcpy还快

多线程拷贝

## Reference

1.https://en.wikipedia.org/wiki/Single_instruction,_multiple_data

