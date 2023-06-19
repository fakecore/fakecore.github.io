---
title: "Tauri使用分享01-安装tauri"
date: 2023-06-19T15:12:43+08:00
# weight: 1
# aliases: ["/first"]
tags: ["first"]
author: "fakecore"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
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

## Installation

Until 2022-09-06, both failed after trying to use Bash and Cargo to create an app. I recommend using Yarn to create the app.

```bash
yarn create tauri-app
```

choose your package manager

choose yarn

choose your front-end stack.

After finishing filling out the options, you can start the app with the command

```bash
yarn tauri dev
```

