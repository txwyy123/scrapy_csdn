# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

import datetime
import time
import redis

from models import Article
from entity import Article as Art
from entity import ArticleStatistic as ArtSta

class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('csdn_data.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode('unicode_escape'))
        return item

class RedisPipeline(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        item['id'] = int(item['url'].split('/')[-1])
        article = Art(item)
        article_statistic = ArtSta(item)
        article_key = "csdn:article"
        statistic_key = "csdn:article:statistic"

        # pipe = self.r.pipeline()
        art = self.r.hget(article_key, item['id'])
        if art:
            art = json.loads(art)
            article.create_time = art['create_time']
        else:
            article.create_time = time.time()
        article.update_time = time.time()
        article = json.dumps(article.get_as_dict())

        art_sta = self.r.hget(statistic_key, item['id'])
        sta_list = []
        if art_sta:
            sta_list = json.loads(art_sta)
            sta_list.append(article_statistic.get_as_dict())
        else:
            sta_list.append(article_statistic.get_as_dict())
        sta = json.dumps(sta_list)

        self.r.hset(article_key, item['id'], article)
        self.r.hset(statistic_key, item['id'], sta)

    def close_spider(self, spider):
        return

class MySQLPipeline(object):

    def process_item(self, item, spider):
        try:
            rows = Article.select().where(Article.id == int(item['url'].split('/')[-1]))
            for row in rows:
                if row:
                    Article.update(title=item['title'], url=item['url'], read_count=item['read_count'],
                           comment_count=item['comment_count'], update_time=datetime.datetime.now())\
                        .where(Article.id == int(item['url'].split('/')[-1])).execute()
                else:
                    Article.create(id=int(item['url'].split('/')[-1]), title=item['title'], url=item['url'], read_count=item['read_count'],
                           comment_count=item['comment_count'], create_time=datetime.datetime.now(),
                           update_time=datetime.datetime.now())
        except Exception, e:
            print e