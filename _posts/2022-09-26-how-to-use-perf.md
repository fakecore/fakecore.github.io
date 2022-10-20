---
layout: post
title: 如何使用perf
date: 2022-09-26 16:54:13 +0800
last_modified_at: 2022-09-27 15:59:44 +0800
tags: []
author: fakecore
author_url:
---

如何使用perf进行性能监测.

perf是Linux系统下的一个性能分析工具.通常我们会使用perf+flamegraph进行性能分析.

## 示例:

unordered_map的倍增扩容机制导致抖动达毫秒级.

解决方案,重新造一个unordered_map,每次扩容指定大小,削峰.

