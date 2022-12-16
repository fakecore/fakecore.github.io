---
layout: post
title: 程序的一生,从启动到消亡[TODO]
date: 2022-10-12 10:15:00 +0800
last_modified_at: 2022-12-01 18:04:03 +0800
tags: []
author: fakecore
author_url: 

---

## 介绍

本文基于Linux和cpp可执行文件,来讲述从cpp软件执行到软件执行结束都发生了什么.

## elf格式





## 函数入栈分析

简单的一个可执行文件的栈变化.

代码

```c++
//test.cc
void test(long long i,int j){}
int main(){
	test(3,1);
	return 0;
}
```

反汇编

```
objdumo -d test
```

main指令

整个反汇编文件分为三列，分别对应：

​       指令地址:         指令机器码	     														指令机器码反汇编到的指令

![image-20221031151751295](/Users/dylan/fakecore.github.io/assets/image-20221031151751295.png)

test函数

![image-20221031151821182](/Users/dylan/fakecore.github.io/assets/image-20221031151821182.png)

简单术语说明

寄存器

| Name | discription                                               |
| ---- | --------------------------------------------------------- |
| rbp  | Frame pointer(栈帧指针，用于标识当前栈帧的起始位置)       |
| rsp  | Stack pointer(堆栈指针寄存器，通常会指向栈顶位置)         |
| esi  | source index                                              |
| edi  | destination index                                         |
| eax  | accumulator                                               |
| rax  | resutl register                                           |
| rdi  | first argument reigster(six register for argument saving) |

文章末尾有全的

指令

| name  | discription                                                  |
| ----- | ------------------------------------------------------------ |
| push  | 把字压入堆栈                                                 |
| pop   | 把字弹出堆栈                                                 |
| mov   | 传送字或字节                                                 |
| nop   | 空操作                                                       |
| req   | 用栈中的数据，修改IP的内容，                                 |
| callq | call指令分为两步：<br />(1) 将当前的IP或者CS和IP压入栈中。<br />(2) 转移。<br />实现近转移。相当于 pushq %rip；jmpq addr |
| nopl  |                                                              |
|       |                                                              |
|       |                                                              |

**CS**是代码段寄存器，**IP**是指令指针寄存器（相当于偏移地址）

函数执行步骤

main

1. push %rbp rbp压入栈
2. mov %rsp,%rbp 把rsp寄存器的值,存入rbp
3. mov    $0x1,%esi 把1存入esi (x64是这样的,可以生成x86,那样子会压栈)
4. mov    $0x3,%edi 把3存入edi (这里也可以看出,参数从右到左进入,主要为了不定参数的实现)
5. callq  5d5 <_Z4testxi> 调用0x5d5
   1. push %rbp 当前地址压入栈
    2. mov %rsp,%rbp 把rsp寄存器的值,存入rbp
    3. mov    %rdi,-0x8(%rbp) 
6. mov    $0x0,%eax
7. pop    %rbp 栈数据到rbp
8. retq
9. nopl   (%rax)











## reference

1. [ret指令与call指令的深入理解](https://rj45mp.github.io/ret%E6%8C%87%E4%BB%A4%E4%B8%8Ecall%E6%8C%87%E4%BB%A4%E7%9A%84%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3/)
2. https://stackoverflow.com/questions/14296088/what-is-this-assembly-function-prologue-epilogue-code-doing-with-rbp-rsp-l
3. https://stackoverflow.com/questions/46752964/what-is-callq-instruction
4. [程序执行汇编描述](https://segmentfault.com/a/1190000016661251)
5. [函数栈描述](https://z.itpub.net/article/detail/50503CAA1CDDA808A925D5758BD1B0A4)

## 附录![](https://pic2.zhimg.com/80/v2-bd5a0aa1625c4445ba33e506b91dba29_1440w.webp)





![img](https://pic1.zhimg.com/80/v2-8f2a02c38a3b53ce857b87ed01272b80_1440w.webp)



