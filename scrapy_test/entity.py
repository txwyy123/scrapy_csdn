# -*- coding: utf-8 -*-

import time

class ArticleStatistic():
    id = 0
    read_count = 0
    comment_count = 0
    create_time = time.time()

    def __init__(self, item):
        self.id = item['id']
        self.read_count = item['read_count']
        self.comment_count = item['comment_count']
        self.create_time = time.time()

    def get_as_dict(self):
        d = dict()
        d['id'] = self.id
        d['read_count'] = self.read_count
        d['comment_count'] = self.comment_count
        d['create_time'] = self.create_time
        return d

class Article():
    id = 0
    url = ''
    title = ''
    read_count = 0
    comment_count = 0
    create_time = time.time()
    update_time = 0

    def __init__(self, item):
        self.id = item['id']
        self.title = item['title']
        self.url = item['url']
        self.read_count = item['read_count']
        self.comment_count = item['comment_count']

    def get_as_dict(self):
        d = dict()
        d['id'] = self.id
        d['url'] = self.url
        d['title'] = self.title
        d['read_count'] = self.read_count
        d['comment_count'] = self.comment_count
        d['create_time'] = self.create_time
        d['update_time'] = self.update_time
        return d