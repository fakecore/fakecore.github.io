---
title: "Cgroup"
date: 2023-11-13T16:45:34+08:00
# weight: 1
# aliases: ["/first"]
tags: ["first"]
author: "fakecore"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: true
hidemeta: false
comments: false
description: "Desc Text."
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

最近工作重心是k8s,docker. 借机了解了下cgroup相关的知识内容.

今天会用短短的篇幅介绍下Linux cgroup v1和v2. 主要涉及hierarchy和资源控制.

## 什么是cgroup?

