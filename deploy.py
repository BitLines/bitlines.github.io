# -*- coding:utf-8 -*-
# @File: deploy.py
# @Author: zhongpingliang
# @Date: 2021年03月17日

'''
部署博客文章，从目录 _docs 下递归遍历文件，读取每个 md 文件后缀的文件，
从 date 中获取年月日，**年月日的格式为 YYYY-MM-DD**，读取之后，把对应
的文件添加软连接到 *_posts* 目录下，文件格式是 YYYY-MM-DD-{file_name}。

_posts 文件的处理逻辑:
- 如果是软连接文件，删除重新连接
- 如果是普通文件，保留再最后做提醒
- 把 docs 下面的所有文件软链到 posts 下
- docs 下没有被软链的文件，报警处理

'''

import os
import re
import logging

logger = logging.getLogger()


def collect_files_in_directory(directory):
    '''
    从目录中递归搜集所有文件。

    Parameters:
        directory: 目录
    Returns:
        relative_paths: 文件从 directory 开始的相对路径
    '''

    directory = directory.rstrip('/') + '/'

    relative_paths = []

    for root, dirs, files in os.walk(directory):
        prefix = root[len(directory):]
        relative_paths.extend([os.path.join(prefix, x) for x in files])

    return relative_paths


def parse_date(d, f):
    try:
        date_pat = re.compile(r'\bdate:\s*(\d\d\d\d-\d\d-\d\d)\b')
        with open(os.path.join(d, f)) as ifile:
            content = ifile.read()
        mat = date_pat.search(content)
        date = mat.group(1)
        return date
    except Exception as e:
        logger.warning(f'parse date fail d:{d}, f:{f}, e: {e}')
    return None


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.join(this_dir, '_docs')
    post_dir = os.path.join(this_dir, '_posts')

    # remove symlinks
    posts = collect_files_in_directory(post_dir)
    remain_posts = []
    for post in posts:
        path = os.path.join(post_dir, post)
        if os.path.islink(path):
            os.remove(path)
        else:
            remain_posts.append(post)

    # create symlinks
    docs = collect_files_in_directory(doc_dir)
    remain_docs = []
    for doc in docs:
        # ignore readme.md
        filename = doc.rsplit('/')[-1]
        if filename.lower() == 'readme.md':
            continue
        date = parse_date(doc_dir, doc)
        if not date:
            remain_docs.append(doc)
        src = f'../_docs/{doc}'
        post_name = doc.replace('/', '-')
        dst = os.path.join(this_dir, post_dir, f'{date}-{post_name}')
        logger.info(f'make symlink {src} => {dst}')
        os.symlink(src, dst)

    if remain_docs:
        logger.warning(f'remain docs: \n\t' + '\n\t'.join(remain_docs))

    if remain_posts:
        logger.warning(f'remain posts: \n\t' + '\n\t'.join(remain_posts))


if __name__ == '__main__':
    main()
