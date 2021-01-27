# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#
# class MyscrapyPipeline:
#     def process_item(self, item, spider):
#         return item


class MyscrapyPipeline(object):
    def process_item(self, item, spider):
        print('开启数据库, 进行数据存储')
        item.save()
        print('关闭数据库')
        return item

