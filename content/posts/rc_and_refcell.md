---
title: "Rc和refcell"
date: 2023-06-19T15:12:35+08:00
# weight: 1
# aliases: ["/first"]
tags: ["linux","rust"]
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

Today we will introduce (`Rc`, `RefCell`) and( `Arc`, `Mutex`) In advanced Rust programming.

### Rc\<T>

only for use in single-threaded scenarios.

Rc\<T> is a reference counter.

T is read-only

### RefCell\<T>

only for use in single-threaded scenarios.

*Interior mutability* is a design pattern in Rust that allows you to mutate data even when there are immutable references to that data;

### Rc<RefCell\<T>>

only for use in single-threaded scenarios.

```rust
#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

    *value.borrow_mut() += 10;

    println!("a after = {:?}", a);
    println!("b after = {:?}", b);
    println!("c after = {:?}", c);
}
```

### Arc\<T>

Fortunately, `Arc<T>` *is* a type like `Rc<T>` that is safe to use in concurrent situations.

Arc\<T>'s counter is atomic, So we can use it in concurrency.

### Mutex\<T>

lock the variable access permission. thread-safe.

### Arc<Mutex\<T>>

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

don't forget implement trait `Send` and `Sync` for T

```Rust
struct X{
}

unsafe impl Sync for X{

}
unsafe impl Send for X{

}
Arc::new(Mutex::new(X::new()));
```

