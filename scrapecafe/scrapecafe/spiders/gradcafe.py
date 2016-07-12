# -*- coding: utf-8 -*-
import scrapy
from scrapecafe.items import ScrapecafeItem


class GradcafeSpider(scrapy.Spider):
    name = "gradcafe"
    allowed_domains = ["thegradcafe.com"]
    start_urls = (
        'http://thegradcafe.com/survey/index.php?q=computer',
    )
    status_key = {'A': 'American', 'U': 'International, with US degree', 'I': 'International, without US degree', 'O': 'Other', '?': 'Unknown'}

    def parse(self, response):
        trs = response.xpath('//*[@id="my-table"]/tr')
        for tr in trs:
            tds = tr.xpath('td')
            institution = tds[0].xpath('text()').extract()
            program = tds[1].xpath('text()').extract()
            decision = tds[2].xpath('span/text()').extract() + tds[2].xpath('text()').extract()
            status = tds[3].xpath('text()').extract() if len(tds) > 3 else list()
            notes = tr.xpath('td/ul/li[2]/text()').extract() if len(tr.xpath('td/ul/li[2]/text()')) > 0 else list()

            item = ScrapecafeItem()
            item['institution'] = ''.join(institution).strip()
            item['program'] = ''.join(program).strip()
            item['decision'] = ''.join(decision).strip()
            item['status'] = self.status_key.get(''.join(status), '').strip()
            item['notes'] = ''.join(notes).strip()

            yield item
