# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import string
import logging
import pymongo
from pymongo import MongoClient
from scrapy.conf import settings
from urllib.parse import quote_plus
from scrapy.exceptions import DropItem
from soccer.tm.items import TeamItem, TeamSeasonItem, PlayerItem, CompetitionItem, CompetitionSeasonItem, FixtureItem
from soccer.util import get_settings

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
        self.soccer_settings = get_settings()
        uri = "mongodb://%s:%s@%s:%s" % (
            quote_plus(self.soccer_settings['mongodb_user']), quote_plus(self.soccer_settings['mongodb_password']), self.soccer_settings['mongodb_server'], self.soccer_settings['mongodb_port'])

        client = MongoClient(uri, authSource=self.soccer_settings['mongodb_auth_db'])

        db = client[self.soccer_settings['mongodb_db']]
        self.collections = {
            "teams": db["teams"],
            "team_season": db["team_season"],
            "competitions": db["competitions"],
            "competition_season": db["competition_season"],
            "players": db["players"],
            "fixtures": db["fixtures"],
            "teams.search": db["teams.search"],
            "players.search": db["players.search"],
        }
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        find_dict = {}
        update_fields = []
        array_fields = []
        array_replace_fields = []
        dict_fields = []
        search_fields = {}
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
            if item.fields[field]['isSearchField']:
                search_fields[field] = item.fields[field]['searchWeight']

        existingItem = self.collections[item['collection']].find_one(find_dict)

        if existingItem is None:
            self.collections[item['collection']].insert(dict(item))
            self.logger.debug(f"Item added to MongoDB collection {item['collection']}")
            if search_fields:
                self.create_ngrams_for_search(item, search_fields, list(find_dict.keys()))
        else:
            self.logger.debug(f"Item already exists in MongoDB collection {item['collection']}")

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
                                        self.logger.debug(f"Updating existing dict-entry in field '{field}' of item {existingItem['_id']} in collection {item['collection']}")
                                        for key in newEntry:
                                            existingEntry[key] = newEntry[key]
                                        existingItem[field][index] = existingEntry
                                        bEntryFound = True
                                        break 
                                if not bEntryFound:
                                    self.logger.debug(f"Adding new dict-entry to field {field} of item {existingItem['_id']} in collection {item['collection']}")
                                    existingItem[field].append(newEntry)
                        else:
                            for newEntry in item[field]:
                                if newEntry not in existingItem[field]:
                                    self.logger.debug(f"Adding new entry '{newEntry}' to field {field} of item {existingItem['_id']} in collection {item['collection']}")
                                    existingItem[field].append(newEntry)
                        set_dict[field] = existingItem[field]
                    else:
                        if field in dict_fields:
                            self.logger.debug(f"Updating dict-entry '{field}' of item {existingItem['_id']} in collection {item['collection']}.")
                            for key in item[field]:
                                existingItem[field][key] = item[field][key]
                            set_dict[field] = existingItem[field]
                        else:
                            self.logger.debug(f"Updating field {field} of item {existingItem['_id']} in collection {item['collection']}. New value: '{item[field]}'")
                            set_dict[field] = item[field]
                        
                self.collections[item['collection']].update_one({'_id': existingItem['_id']}, {'$set': set_dict})
                self.logger.debug(f"Item updated successfully")
                if search_fields:
                    self.create_ngrams_for_search(item, search_fields, list(find_dict.keys()))
        return item

    def create_ngrams_for_search(self, item, search_fields, exist_check_fields):
        search_collection = item['collection'] + '.search'

        query = {}
        search_item = {}
        for field in exist_check_fields:
            search_item[field] = item[field]
            query[field] = item[field]
        
        for field in search_fields:
            word_processed = item[field].translate({ ord(c): None for c in string.whitespace }).lower()
            search_item[field] = item[field]
            search_item[field + '_ngrams'] = self.make_ngrams(word_processed, prefix_only=False)
            search_item[field + '_prefix_ngrams'] = self.make_ngrams(word_processed, prefix_only=True)

        self.collections[search_collection].update_one(query, {
            "$set": search_item, 
        }, upsert=True) 

    def make_ngrams(self, word, prefix_only=False):
        """
            string  word: word to split into ngrams
        """    
        min_size = 4
        length = len(word)
        size_range = range(min_size, max(length, min_size) + 1)
        if prefix_only:
            return [
                word[0:size]
                for size in size_range
            ]
        return list(set(
            word[i:i + size]
            for size in size_range
            for i in range(0, max(0, length - size) + 1)
        ))  

    def close_spider(self, spider):
        self.create_search_index("teams.search", "search_team_ngrams", TeamItem())
        self.create_search_index("players.search", "search_player_ngrams", PlayerItem())

    def create_search_index(self, collection, name, item):
        keys = []
        weights = {}
        for field in item.fields:
            if item.fields[field]['isSearchField']:
                keys.append((field + '_ngrams', pymongo.TEXT))
                keys.append((field + '_prefix_ngrams', pymongo.TEXT))
                weights[field + '_ngrams'] = item.fields[field]['searchWeight']
                weights[field + '_prefix_ngrams'] = item.fields[field]['searchWeight'] + 50

        try:
            self.collections[collection].drop_index(name)
        except:
            pass

        self.collections[collection].create_index(
            keys,
            name=name,
            weights=weights
        )
