---
title: "Linux下shm和mmap的比较"
date: 2023-06-19T15:12:12+08:00
# weight: 1
# aliases: ["/first"]
tags: ["linux"]
author: "fakecore"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: true
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

shmget 和 shm_open+mmap是两种不同的共享内存用法,

shmget是老式system V 模型,

shm_open 是POSIX下的产物.

mmap和System V共享内存的主要区别在于：

- sysv shm是持久化的，除非被一个进程明确的删除，否则它始终存在于内存里，直到系统关机；
- mmap映射的内存在不是持久化的，如果进程关闭，映射随即失效，除非事先已经映射到了一个文件上。

内存映射机制mmap是POSIX标准的系统调用，有匿名映射和文件映射两种。

- 匿名映射使用进程的虚拟内存空间，它和malloc(3)类似，实际上有些malloc实现会使用mmap匿名映射分配内存，不过匿名映射不是POSIX标准中规定的。
- 文件映射有`MAP_PRIVATE`和`MAP_SHARED`两种。前者使用COW的方式，把文件映射到当前的进程空间，修改操作不会改动源文件。后者直接把文件映射到当前的进程空间，所有的修改会直接反应到文件的page cache，然后由内核自动同步到映射文件上。

shmget用法 shmget(IPC_PRIVATE,size,flag)

shm_open 创建一个共享内存(文件,/dev/shm下),返回一个fd.通过ftruncate指定文件大小

mmap通过fd attach上这个地址,进行操作

## shmget

compared to shm_open+mmap, shm_get used the old System V shared memory model.

```c
#include <sys/ipc.h>
#include <sys/shm.h>
int shmget(key_t key, size_t size, int shmflg);
```

key: It may be used either to obtain the identifier of a previously created shared memory segment (when shmflg is zero and key does not have the value IPC_PRIVATE), or to create a new set.

获取一个特定shm

size: A new shared memory segment, with size equal to the value of size rounded up to a  multi-
       ple  of  PAGE_SIZE, is created if key has the value IPC_PRIVATE or key isn't IPC_PRIVATE,
       no shared memory segment corresponding to key exists, and IPC_CREAT is specified in  shm-
       flg.

 If  shmflg  specifies both IPC_CREAT and IPC_EXCL and a shared memory segment already ex-
       ists for key, then shmget() fails with errno set to EEXIST.  (This is  analogous  to  the
       effect of the combination O_CREAT | O_EXCL for open(2).)

如果shmflag同时指定了`IPC_CREAT` 和`IPC_EXCL`,同时有一个已存在的KEY共享内存,shmget将会失败.

RETURN VALUE
       On success, a valid shared memory identifier is returned.  On error, -1 is returned,  and
       errno is set to indicate the error.

可以理解成返回一个fd,指向可用的shm segement



## shm_open+mmap

```c
#include <sys/mman.h>
#include <sys/stat.h>        /* For mode constants */
#include <fcntl.h>           /* For O_* constants */

int shm_open(const char *name, int oflag, mode_t mode);

int shm_unlink(const char *name);

Link with -lrt.
```

shm_open: 可以创建或者打开已存在的shm segement.

`open` is the same as `shm_open`.

shm_unlink: 关闭shm segement

 **oflag** is a bit mask created by ORing together exactly one of O_RDONLY or O_RDWR  and  any
       of the other flags listed here:

       O_RDONLY
              Open the object for read access.  A shared memory object opened in this way can be
              mmap(2)ed only for read (PROT_READ) access.

       O_RDWR Open the object for read-write access.

       O_CREAT
              Create the shared memory object if it does not exist.  The user and  group  owner-
              ship  of  the object are taken from the corresponding effective IDs of the calling
              process, and the object's permission bits are set according  to  the  low-order  9
              bits  of  mode,  except that those bits set in the process file mode creation mask
              (see umask(2)) are cleared for the new object.  A set of macro constants which can
              be  used to define mode is listed in open(2).  (Symbolic definitions of these con-
              stants can be obtained by including <sys/stat.h>.)

              A new shared memory object initially has zero length--the size of the  object  can
              be  set  using  ftruncate(2).  The newly allocated bytes of a shared memory object
              are automatically initialized to 0.

       O_EXCL If O_CREAT was also specified, and a shared memory object with the given name  al-
              ready exists, return an error.  The check for the existence of the object, and its
              creation if it does not exist, are performed atomically.

       O_TRUNC
              If the shared memory object already exists, truncate it to zero bytes.

**mmap**

```c
 #include <sys/mman.h>

void *mmap(void *addr, size_t length, int prot, int flags,
           int fd, off_t offset);
int munmap(void *addr, size_t length);

//See NOTES for information on feature test macro requirements.
```

```
mmap() creates a new mapping in the virtual address space of the
       calling process.  The starting address for the new mapping is
       specified in addr.  The length argument specifies the length of
       the mapping (which must be greater than 0).

RETURN VALUE
On success, mmap() returns a pointer to the mapped area.  On
       error, the value MAP_FAILED (that is, (void *) -1) is returned,
       and errno is set to indicate the error.

On success, munmap() returns 0.  On failure, it returns -1, and
errno is set to indicate the error (probably to EINVAL).
```

**ftruncate**

把文件size变到指定大小

```c
#include <unistd.h>
#include <sys/types.h>
int truncate(const char *path, off_t length);
int ftruncate(int fd, off_t length);
```

    The truncate()  and ftruncate() functions cause the regular file named by path or refer-
           enced by fd to be truncated to a size of precisely length bytes.

    If the file previously was larger than this size, the extra data is lost.   If  the  file
       previously was shorter, it is extended, and the extended part reads as null bytes ('\0').

       The file offset is not changed.

       If  the  size  changed, then the st_ctime and st_mtime fields (respectively, time of last
       status change and time of last modification; see inode(7)) for the file are updated,  and
       the set-user-ID and set-group-ID mode bits may be cleared.

       With  ftruncate(),  the  file must be open for writing; with truncate(), the file must be
       writable.

simply code

```c
//get.c
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define STORAGE_ID "/SHM_TEST"
#define STORAGE_SIZE 32

int main(int argc, char *argv[])
{
	int res;
	int fd;
	char data[STORAGE_SIZE];
	pid_t pid;
	void *addr;

	pid = getpid();

	// get shared memory file descriptor (NOT a file,but act as a regular file)
	fd = shm_open(STORAGE_ID, O_RDONLY, S_IRUSR | S_IWUSR);
	if (fd == -1)
	{
		perror("open");
		return 10;
	}

	// map shared memory to process address space
	addr = mmap(NULL, STORAGE_SIZE, PROT_READ, MAP_SHARED, fd, 0);
	if (addr == MAP_FAILED)
	{
		perror("mmap");
		return 30;
	}

	// place data into memory
	memcpy(data, addr, STORAGE_SIZE);

	printf("PID %d: Read from shared memory: \"%s\"\n", pid, data);

	return 0;
}
```

```c
//set.c
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define STORAGE_ID "/SHM_TEST"
#define STORAGE_SIZE 32
#define DATA "Hello, World! From PID %d"

int main(int argc, char *argv[])
{
	int res;
	int fd;
	int len;
	pid_t pid;
	void *addr;
	char data[STORAGE_SIZE];

	pid = getpid();
	sprintf(data, DATA, pid);

	// get shared memory file descriptor (NOT a file)
	fd = shm_open(STORAGE_ID, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
	if (fd == -1)
	{
		perror("open");
		return 10;
	}

	// extend shared memory object as by default it's initialized with size 0
	res = ftruncate(fd, STORAGE_SIZE);
	if (res == -1)
	{
		perror("ftruncate");
		return 20;
	}

	// map shared memory to process address space
	addr = mmap(NULL, STORAGE_SIZE, PROT_WRITE, MAP_SHARED, fd, 0);
	if (addr == MAP_FAILED)
	{
		perror("mmap");
		return 30;
	}

	// place data into memory
	len = strlen(data) + 1;
	memcpy(addr, data, len);

	// wait for someone to read it
	sleep(2);

	// mmap cleanup
	res = munmap(addr, STORAGE_SIZE);
	if (res == -1)
	{
		perror("munmap");
		return 40;
	}

	// shm_open cleanup
	fd = shm_unlink(STORAGE_ID);
	if (fd == -1)
	{
		perror("unlink");
		return 100;
	}

	return 0;
}
```

## 题外话 Q&A:

### Q:mmap下的资源需要锁吗?

A:

需要锁:

**Semaphores**

**共享内存的**mutex

​	pthread_mutexattr_setrobust() ，将 pthread 互斥锁初始化为“robust”，如果持有互斥锁的进程死了，下一个获取它的线程将收到 EOWNERDEAD（但仍然成功获取互斥锁），以便它知道执行任何清理。然后它需要使用 pthread_mutex_consistent() 通知获取的互斥锁再次一致

如何使用?

通过mmap获取一块共享内存,共享内存内存在pthread_mutex相关信息

https://blog.csdn.net/qq_35396127/article/details/78942245



**文件锁**

在linux 系统中，flock函数是为解决多进程对同一文件的读写冲突的，而flock函数只能锁定整个文件，无法锁定文件的某一区域。且flock可以保证robust



### Q:shm_open获取的资源能自动销毁吗?不调用shm_unlink

A:

The operation of **shm_unlink**() is analogous to ***[unlink](https://linux.die.net/man/2/unlink)**(2)*: it removes a shared memory object name, and, once all processes have unmapped the object, de-allocates and destroys the contents of the associated memory region. After a successful **shm_unlink**(), attempts to **shm_open**() an object with the same *name* will fail (unless **O_CREAT** was specified, in which case a new, distinct object is created).

文件存在于/dev/shm下,如果不调用该函数,文件会一直存在
