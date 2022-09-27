#!/usr/bin/python3

import time
import sys



if __name__ == "__main__":
    lt = time.localtime()
    created_time = time.strftime("%Y-%m-%d-", lt)
    title = sys.argv[1]
    title.replace(" ","-")
    filename ="./_posts/" + created_time + title + ".md"

    fn = filename
    try:
        file = open(fn, 'r')
        exit
    except IOError:
        file = open(fn, 'w')
        file.write("---\n")
        file.write("layout: post\n")
        file.write("title: " + title + "\n")
        file.write("date: "+ time.strftime("%Y-%m-%d %H:%M:%S +0800", lt) + "\n")
        file.write("last_modified_at: " + time.strftime("%Y-%m-%d %H:%M:%S +0800", lt) + "\n")
        file.write("tags: []\n")
        file.write("author: fakecore\n")
        file.write("author_url: \n")
        file.write("---\n")
        file.flush()
        file.close()





