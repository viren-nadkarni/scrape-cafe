# -*- coding: utf-8 -*-
import scrapy
from scrapecafe.items import ScrapecafeItem


class GradcafeSpider(scrapy.Spider):
    name = "gradcafe"
    allowed_domains = ["thegradcafe.com"]
    status_key = {'A': 'American', 'U': 'International, with US degree', 'I': 'International, without US degree', 'O': 'Other', '?': 'Unknown'}

    def __init__(self, settings):
        super(GradcafeSpider, self).__init__()
        self.settings = settings
        self.start_urls = tuple( ['http://thegradcafe.com/survey/index.php?q={}'.format(keyword) for keyword in self.settings['KEYWORDS']] )

    def parse(self, response):
        trs = response.xpath('//*[@id="my-table"]/tr')
        for tr in trs:
            tds = tr.xpath('td')
            institution = tds[0].xpath('text()').extract()
            program = tds[1].xpath('text()').extract()
            decision = tds[2].xpath('span/text()').extract() + tds[2].xpath('text()').extract()
            scores = tds[2].xpath('a/span/text()').extract()
            status = tds[3].xpath('text()').extract() if len(tds) > 3 else list()
            notes = tr.xpath('td/ul/li[2]/text()').extract() if len(tr.xpath('td/ul/li[2]/text()')) > 0 else list()

            item = ScrapecafeItem()
            item['institution'] = ''.join(institution).strip()
            item['program'] = ''.join(program).strip()
            item['decision'] = ''.join(decision).strip()
            item['status'] = self.status_key.get(''.join(status), '').strip()
            item['notes'] = ''.join(notes).strip()
            item['gpa'] = scores[0][2:] if len(scores) else ''
            item['gre'] = scores[1][2:] if len(scores) else ''

            yield item

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)
