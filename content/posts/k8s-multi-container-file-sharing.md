---
title: "K8s多容器pod的数据共享"
date: 2023-09-13T17:01:12+08:00
# weight: 1
# aliases: ["/first"]
tags: ["k8s"]
author: "fakecore"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
description: ""
disableHLJS: true # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
UseHugoToc: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
editPost:
    URL: "https://github.com/fakecore/content"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---
最近刚好遇到多容器单Pod的数据共享需求.

随着需求做完,想着写点文章分享下.

本文只分享两个场景,共享空目录,共享非空目录

## 背景知识

Pod

> Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元
>
> 可以在单个Pod中创建多个Container,他们之间共享上下文
>
> Pod 的共享上下文包括一组 Linux 名字空间、控制组（cgroup）和可能一些其他的隔离方面， 即用来隔离容器的技术。 在 Pod 的上下文中，每个独立的应用可能会进一步实施隔离。
>
> Pod 类似于共享名字空间并共享文件系统卷的一组容器。

Volume

> Kubernetes 卷（Volume） 这一抽象概念用于解决Container文件存储和跨Container数据共享问题

## 共享空目录

这个场景比较常见,也比较好处理.

通常使用volumes中的emptyDir来处理

https://kubernetes.io/zh-cn/docs/concepts/storage/volumes/#emptydir
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  - image: registry.k8s.io/test-webserver
    name: test-container1
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```
test-conainer和test-conainer1的/cache目录就进行保持共享,当然你要记住,之前存在于/cache的内容将会无法看到

## 共享非空目录

k8s本身的设计,不允许直接挂载非空目录, 所以我们这里使用initContainer进行操作

```yaml
apiVersion: apps/v1
kind: Pod
spec:
initContainers:
- image:
    name:
    command: [
                "/bin/sh",
                "-c",
                "mkdir /tmp/dir;
                cp -r /target/folder /tmp/dir",
            ]
    volumeMounts:
    - name: sharing
    mountPath: /tmp/dir
containers:
- image:
    name:
    volumeMounts:
    - name: sharing
        mountPath: /usr/local/sharing
volumes:
- name: sharing
    emptyDir: {}
```

在PodInitialization的过程中,首先会启动initContainer. 加载它的fs,然后在这个过程中,我们会把想要的文件拷贝到/tmp/dir中,因为/tmp/dir提前被设置成了共享目录,所以这个操作会被保留下来.