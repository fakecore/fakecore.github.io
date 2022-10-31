---
layout: post
title: cpp-virtual-table
date: 2022-10-17 17:32:00 +0800
last_modified_at: 2022-10-20 16:19:45 +0800
tags: []
author: fakecore
author_url: 

---



环境:Linux arm64 gcc

虚表是c++实现多态的一个重要内容.

让我们来看看不同的类生成的对象如何.

```c++

class BaseA{
};

class BaseB{
	void hi(){}
	int word;
};

class BaseC{
  virtual void ff(){}
  virtual void k(){}
};

class BaseD{
  virtual void ff(){}
};

class BaseE{
  virtual void ff(){}
  int word;
};

class DerivedC: public BaseC{
  void ff() override{}
};

class DerivedD: public BaseC,public BaseD{
  void ff() override{}
};

int main(){

    BaseA ba;
    BaseB bb;
    BaseC bc;
    BaseD bd;
    BaseE be;
    DerivedC dc;
    DerivedD dd;

    return 0;
}

```

先说结论.我们来看看每个类实例的内存布局.

![cpp_class_model](/Users/dylan/fakecore.github.io/assets/cpp_class_model.png)

今天我们用gdb来看看如何进行查看

1.设置打印友好

2.普通继承.

- 先根据基类虚函数生成一个虚表
- 根据子类虚函数,如果有重名的,参数相同.覆盖虚表上父类对应函数位置,如果同名,不同参数,则在后面添加. 如果是一个新函数,也一样在后面添加.

```c++
(gdb) set print pretty on
(gdb) p dc
$67 = {
  <BaseC> = {
    _vptr.BaseC = 0xaaaaaaab1cd8 <vtable for DerivedC+16>
  }, <No data fields>}
(gdb) p *((void**)0xaaaaaaab1cd8-1)
$68 = (void *) 0xaaaaaaab1d78 <typeinfo for DerivedC>
(gdb) p *((void**)0xaaaaaaab1cd8)
$69 = (void *) 0xaaaaaaaa1018 <DerivedC::ff()>
(gdb) p *((void**)0xaaaaaaab1cd8+1)
$70 = (void *) 0xaaaaaaaa0fdc <BaseC::k()>
(gdb) p *((void**)0xaaaaaaab1cd8+2)
$71 = (void *) 0xaaaaaaaa102c <DerivedC::nd()>
(gdb) p *((void**)0xaaaaaaab1cd8+Quit
(gdb) p *((void**)0xaaaaaaab1cd8+3)
$72 = (void *) 0x0
(gdb) p *((void**)0xaaaaaaab1cd8+3Quit
// 打印dd相关
(gdb) p dd
$73 = {
  <BaseC> = {
    _vptr.BaseC = 0xaaaaaaab1ca0 <vtable for DerivedD+16>
  }, 
  <BaseD> = {
    _vptr.BaseD = 0xaaaaaaab1cc0 <vtable for DerivedD+48>
  }, <No data fields>}
(gdb) p *((void**)0xaaaaaaab1ca0-1)
$74 = (void *) 0xaaaaaaab1d40 <typeinfo for DerivedD>
(gdb) p *((void**)0xaaaaaaab1ca0)
$75 = (void *) 0xaaaaaaaa1040 <DerivedD::ff()>
(gdb) p *((void**)0xaaaaaaab1ca0+1)
$76 = (void *) 0xaaaaaaaa0fdc <BaseC::k()>
(gdb) p *((void**)0xaaaaaaab1cc0-1)
$81 = (void *) 0xaaaaaaab1d40 <typeinfo for DerivedD>
(gdb) p *((void**)0xaaaaaaab1cc0)
$82 = (void *) 0xaaaaaaaa1054 <non-virtual thunk to DerivedD::ff()>
(gdb) p *((void**)0xaaaaaaab1cc0+1)
$83 = (void *) 0x0
```

虚函数表在哪里

**C++虚函数表保存在.rdata只读数据段**。编译时期由[编译器](https://so.csdn.net/so/search?q=编译器&spm=1001.2101.3001.7020)确定虚函数表。虚函数表属于类，类的所有对象共享这个类的虚函数表。

