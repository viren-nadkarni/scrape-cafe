# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import time
import requests
from tokens import *


class ScrapecafePipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect('./gradcafe.db')
        self.curs = self.conn.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS gradcafe (
                id INTEGER PRIMARY KEY,
                time INTEGER,
                decision TEXT,
                institution TEXT,
                notes TEXT,
                program TEXT,
                status TEXT);''')
        self.conn.commit()

        self.all_items = self.curs.execute('SELECT decision, institution, notes, program, status from gradcafe').fetchall()

    def process_item(self, item, spider):
        item_tuple = (item['decision'].decode("ascii","ignore"), item['institution'].decode("ascii","ignore"), 
                item['notes'].decode("ascii","ignore"), item['program'].decode("ascii","ignore"), item['status'].decode("ascii","ignore"))

        if item_tuple not in self.all_items:
            # markdown foo
            text_md = '*Institution:* {}\n*Program:* {}\n*Decision:* {}\n*Status:* {}\n*Notes:* {}'.format(item['institution'], item['program'], item['decision'], item['status'], item['notes'])

            # send telegram message
            requests.get('https://api.telegram.org/bot{}/sendMessage'.format(BOT_API_TOKEN),
                    params={'chat_id': '@scrapecafe', 'parse_mode': 'Markdown', 'text': text_md})

            self.curs.execute('INSERT INTO gradcafe (time, decision, institution, notes, program, status) VALUES (?, ?, ?, ?, ?, ?)', (int(time.time()),) + item_tuple)
            self.conn.commit()

        return item
