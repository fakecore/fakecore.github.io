---
layout: post
title: brpc源码解析ep01——flatmap分析
date: 2022-11-29 15:34:41 +0800
last_modified_at: 2022-12-16 17:21:05 +0800
tags: []
author: fakecore
author_url: 
---



让我们来看看FlatMap的结构,看明白了FlatMap,那么FlatSet也是手到擒来.

```c++
class FlatMap{
  public:
    struct PositionHint {
        size_t nbucket;
        size_t offset;
        bool at_entry;
        key_type key;
    };
     struct Bucket {
        Bucket* next;
        char element_spaces[sizeof(Element)];
    };
  private:
  	size_t _size;
    size_t _nbucket;
    Bucket* _buckets;
    uint64_t* _thumbnail;
    u_int _load_factor;
    hasher _hashfn;
    key_equal _eql;
    SingleThreadedPool<sizeof(Bucket), 1024, 16> _pool;
}
```

FlatMap是一种开链法的hash table.



## hash函数

FlatMap支持多种hash函数

1.
