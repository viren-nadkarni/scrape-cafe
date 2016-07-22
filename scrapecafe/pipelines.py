# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import time
import requests


class ScrapecafePipeline(object):
    def __init__(self, settings):
        self.settings = settings
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
        item_tuple = (item['decision'], item['institution'], item['notes'], item['program'], item['status'])

        if item_tuple not in self.all_items:
            # markdown foo
            text_md = u'*Institution:* {}\n*Program:* {}\n*Decision:* {}\n*Status:* {}\n'.format(item['institution'], item['program'], item['decision'], item['status'])
            if item['gre'] or item['gpa']:
                text_md += u'*GRE:* {} *GPA:* {}\n'.format(item['gre'], item['gpa'])
            if item['notes']:
                text_md += u'*Notes:* {}'.format(item['notes'])

            # send the telegram message
            requests.get('https://api.telegram.org/bot{}/sendMessage'.format(self.settings['TELEGRAM_BOT_API_KEY']), 
                    params={'chat_id': self.settings['TELEGRAM_CHANNEL_NAME'], 
                        'parse_mode': 'Markdown', 
                        'text': text_md})

            self.curs.execute('INSERT INTO gradcafe (time, decision, institution, notes, program, status) VALUES (?, ?, ?, ?, ?, ?)', 
                    (int(time.time()),) + item_tuple)
            self.conn.commit()

        return item

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)
