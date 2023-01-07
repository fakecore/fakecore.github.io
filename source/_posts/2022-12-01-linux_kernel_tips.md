---
layout: post
title: linux_kernel_tips[TODO]
date: 2022-12-01 13:10:02 +0800
last_modified_at: 2022-12-16 17:21:05 +0800
tags: [linux]
author: fakecore
author_url:

---



## 内核态的进程运行到sleep状态解析

schedule_timeout函数如何让当前进程陷入sleep,主动交出控制权

主要通过调用schedule主动进入调度函数

### Q:进程的数据栈会被回收吗?

A:是的,当进行进程切换时,在xx函数会进行进程清理,把相关现场保存

```c
schedule_timeout
//time/timer.c
signed long __sched schedule_timeout(signed long timeout)
//sched/core.c
asmlinkage __visible void __sched schedule(void){
	//call
  //进入调度器
  __schedule(SM_NONE);//https://zhuanlan.zhihu.com/p/363791563
}
```

## Linux 函数 get_current()

所以通过`esp`寄存器的值和内核栈大小，就可以方便的计算出内核栈的栈底地址，该地址其实就是进程对应的`struct thread_info`结构的地址

//http://linux.laoqinren.net/kernel/sched/current/

```c
static __always_inline struct task_struct *get_current(void)
{
	unsigned long sp_el0;

	asm ("mrs %0, sp_el0" : "=r" (sp_el0));

	return (struct task_struct *)sp_el0;
}
```

