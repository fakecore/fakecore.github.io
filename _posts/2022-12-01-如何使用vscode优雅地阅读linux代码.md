---
layout: post
title: 如何使用vscode优雅地阅读linux代码
date: 2022-12-01 17:53:41 +0800
last_modified_at: 2022-12-01 18:03:36 +0800
tags: [tech]
author: fakecore
author_url: 
---



笔者将介绍如何使用vscode阅读Linux内核代码.

1.下载Linux内核

2.进行内核编译

```bash
tar xvf linux-x.x.x.tar.gz && cd linux-x.x.x
 cp /boot/config-$(uname -r) .config
 //install bear
 bear -- make -j
```

经过这步骤之后,会生成一个//linux-x.x.x/compile_commands.json

用vscode打开linxu-x.x.x

配置//linxu-x.x.x/.vscode/c_cpp_properties.json

```json
"compileCommands": "${workspaceFolder}/compile_commands.json"
```

3.关闭选项:c/c++ disable error squiggles

4.最后vscode:reload window

5.享受你的阅读
