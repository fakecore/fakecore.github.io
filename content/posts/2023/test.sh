#!/bin/bash

# 遍历当前目录下的所有文件
for file in *.md
do
    # 获取文件名(不包括扩展名)
    filename="${file%.*}"

    # 创建以文件名命名的文件夹
    mkdir "$filename"

    # 移动文件到新建的文件夹中,并重命名为index.md5
    mv "$file" "$filename/index.md"
done
