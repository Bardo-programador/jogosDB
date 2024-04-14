# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
import re 
import scrapy

class JogosdbPipeline:
    def process_item(self, item, spider):
        return item

    
   
class SteamWriterPipeline(JogosdbPipeline):
    def open_spider(self, spider):
        if os.path.exists("dados"):
            self.file = open("dados/steam.jsonl", "w")
        else:
            os.makedirs('dados')
            self.file = open("dados/steam.jsonl", "w")

    def process_item(self, item, spider)->scrapy.Item:
        self.precoFormatado(item)
        return item

def precoFormatado(self, item):
        price_pattern = r'(\d+,\d+)'
        item['price'] = (re.search(price_pattern, item['price'])).group(1)
        item['price'] = float(item['price'].replace(",","."))

class NuuvemWriterPipeline(JogosdbPipeline):
    def open_spider(self, spider):
        if os.path.exists("dados"):
            self.file = open("dados/nuuvem.jsonl", "w")
        else:
            os.makedirs('dados')
            self.file = open("dados/nuuvem.jsonl", "w")

    def process_item(self, item, spider):
        item['price'] = float(item['price'])
        return itemi