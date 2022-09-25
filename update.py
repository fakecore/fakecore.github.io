#!/usr/bin/python3

import time
import sys
import os

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f

if __name__ == "__main__":
    base = './_posts/'
    for i in findAllFile(base):
        modTime = time.localtime(os.stat(base+i).st_mtime)
        modified_time = time.strftime("%Y-%m-%d %H:%M:%S +0800", modTime)
        file = base+i
        print(modified_time,file)
        fn = open(file,'r')
        lines = fn.readlines()
        for i in range(0,len(lines)):
            line = lines[i]
            if line.find("last_modified_at") != -1:
                print(line,i)
                lines[i] ="late_modified_at: " + modified_time + "\n"
                print(lines[i])
                fn.close()
                fn=open(file,"w+")
                fn.writelines(lines)
                fn.flush();
                fn.close()
                break
