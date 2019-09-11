# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class XiaohuaPipeline(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "root", "xiaohua", charset='utf8' )
    def process_item(self, item, spider):
        cursor = self.db.cursor()
        data=dict(item)
        sql="INSERT INTO `joke` (`id`, `title`, `contents`, `fenlei`, `laiyuan`) VALUES ('', %s, %s, %s,%s)"
        # 执行sql语句
        try:
            cursor.execute(sql,[data['title'],data['contents'],data['fenlei'],data["laiyuan"]])
            self.db.commit()
            #print("1")
        except:
            # Rollback in case there is any error
            self.db.rollback()
        cursor.close()
        return item
    def close_spider(self,spider):
        self.db.close()
