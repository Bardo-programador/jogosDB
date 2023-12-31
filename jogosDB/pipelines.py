# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os

class JogosdbPipeline:
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    
class SteamWriterPipeline(JsonWriterPipeline):
    def open_spider(self, spider):
        if os.path.exists("dados"):
            self.file = open("dados/steam.jsonl", "w")
        else:
            os.makedirs('dados')
            self.file = open("dados/steam.jsonl", "w")

class NuuvemWriterPipeline(JsonWriterPipeline):
    def open_spider(self, spider):
        if os.path.exists("dados"):
            self.file = open("dados/nuuvem.jsonl", "w")
        else:
            os.makedirs('dados')
            self.file = open("dados/nuuvem.jsonl", "w")