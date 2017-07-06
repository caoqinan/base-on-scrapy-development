# -*- coding: utf-8 -*-
from scrapy import signals
import json
import codecs
from scrapy import log
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d
    def _do_upinsert(self, conn, item, spider):
        conn.execute("""
            insert into liebiao(name, tel, addr, belongtowhere) 
            values(%s, %s, %s, %s)
        """, (item['name'], item['tel'], item['addr'], item['belongtowhere']))
        #print """

    def _handle_error(self, failue, item, spider):
        log.err(failure)


    # def process_item(self, item, spider):
    #     d = self.dbpool.runInteraction(self._do_upinsert, item)
    #     d.addErrback(self._handle_error, item)
    #     d.addBoth(lambda _: item)
    #     return d
    # def _do_upinsert(self, conn, item, spider):
    #     conn.execute("""
    #         insert into liebiao(name, tel, addr ,belongtowhere) 
    #         values(%s, %s, %s, %s)
    #     """, (item['name'], item['tel'], item['addr'], item['belongtowhere']))

    # def _handle_error(self, failue, item):
    #     log.err(failure)


    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self._conditional_insert, item)
    #     query.addErrback(self.handle_error)
    #     return item

    # def _conditional_insert(self, tb, item):

    #     tb.execute("insert into liebiao(name, tel, addr, belongtowhere) values (%s, %s, %s, %s)",(item["name"], item["tel"], item["addr"], item["belongtowhere"]))
    #     log.msg("Item data in db: %s" % item, level=log.DEBUG)

    # def handle_error(self, e):
    #     log.err(e)


