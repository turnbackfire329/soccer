# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
from pymongo import MongoClient
from scrapy.conf import settings
from urllib.parse import quote_plus
from scrapy.exceptions import DropItem
import logging

COLLECTIONS = ["teams", "team_season", "competitions", "competition_season", "players", "fixtures"]

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('tm.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class ValidateItemPipeline(object):
    def process_item(self, item, spider):
        if "collection" not in item:
            raise DropItem("Missing collection!")

        if item["collection"] not in COLLECTIONS:
            raise DropItem(f"Unknown collection {item['collection']}!")
        
        return item

class MongoDBPipeline(object):
    def __init__(self):
        uri = "mongodb://%s:%s@%s:%s" % (
            quote_plus(settings['MONGODB_USER']), quote_plus(settings['MONGODB_PASSWORD']), settings['MONGODB_SERVER'], settings['MONGODB_PORT'])

        client = MongoClient(uri, authSource=settings['MONGODB_AUTH_DB'])

        db = client[settings['MONGODB_DB']]
        self.collections = {
            "teams": db["teams"],
            "team_season": db["team_season"],
            "competitions": db["competitions"],
            "competition_season": db["competition_season"],
            "players": db["players"],
            "fixtures": db["fixtures"]
        }
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        find_dict = {}
        update_fields = []
        array_fields = []
        array_replace_fields = []
        dict_fields = []
        for field in item.fields:
            if item.fields[field]['existCheck']:
                find_dict[field] = item[field]
            if item.fields[field]['updateable']:
                update_fields.append(field)
            if item.fields[field]['isArray']:
                array_fields.append(field)
            if item.fields[field]['arrayReplace']:
                array_replace_fields.append(field)
            if item.fields[field]['isDict']:
                dict_fields.append(field)

        existingItem = self.collections[item['collection']].find_one(find_dict)

        if existingItem is None:
            self.collections[item['collection']].insert(dict(item))
            self.logger.info(f"Item added to MongoDB collection {item['collection']}")
        else:
            self.logger.info(f"Item already exists in MongoDB collection {item['collection']}")

            for field in item.fields:
                if field not in existingItem:
                    existingItem[field] = item[field]

            if update_fields:
                set_dict = {}
                for field in update_fields:
                    if field in array_fields:
                        if field in array_replace_fields:
                                existingItem[field] = item[field]
                        elif field in dict_fields:
                            for newEntry in item[field]:
                                bEntryFound = False
                                for index, existingEntry in enumerate(existingItem[field]):
                                    same_keys = [k for k in newEntry if k in existingEntry]
                                    same_value_keys = [k for k in same_keys if newEntry[k] == existingEntry[k]]
                                    if len(same_keys) == len(same_value_keys):
                                        self.logger.info(f"Updating existing dict-entry in field '{field}' of item {existingItem['_id']} in collection {item['collection']}")
                                        for key in newEntry:
                                            existingEntry[key] = newEntry[key]
                                        existingItem[field][index] = existingEntry
                                        bEntryFound = True
                                        break 
                                if not bEntryFound:
                                    self.logger.info(f"Adding new dict-entry to field {field} of item {existingItem['_id']} in collection {item['collection']}")
                                    existingItem[field].append(newEntry)
                        else:
                            for newEntry in item[field]:
                                if newEntry not in existingItem[field]:
                                    self.logger.info(f"Adding new entry '{newEntry}' to field {field} of item {existingItem['_id']} in collection {item['collection']}")
                                    existingItem[field].append(newEntry)
                        set_dict[field] = existingItem[field]
                    else:
                        if field in dict_fields:
                            self.logger.info(f"Updating dict-entry '{field}' of item {existingItem['_id']} in collection {item['collection']}.")
                            for key in item[field]:
                                existingItem[field][key] = item[field][key]
                            set_dict[field] = existingItem[field]
                        else:
                            self.logger.info(f"Updating field {field} of item {existingItem['_id']} in collection {item['collection']}. New value: '{item[field]}'")
                            set_dict[field] = item[field]
                        
                self.collections[item['collection']].update_one({'_id': existingItem['_id']}, {'$set': set_dict})
                self.logger.info(f"Updated item")
        return item