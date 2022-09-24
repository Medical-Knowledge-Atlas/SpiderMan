import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY16(BaseSpider):
    name = "YY16"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://www.zjyxcg.cn/showListZCFG.html?catalogId=3&type=&pageNow=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="newscontent"]/ul/li')
        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"https://www.zjyxcg.cn" + data.xpath('./div[1]/a/@href').extract()[0]
            save['title'] = data.xpath('./div[1]/a/text()').extract()[0]
            save['release_date'] = data.xpath('./div[2]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'https://www.zjyxcg.cn/showListZCFG.html?catalogId=3&type=&pageNow={next_page}',
                             callback=self.parse, meta={'page': next_page, 'save': {}})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@id="conextId"]/p/span')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = []
        response.meta['save']['annex_title'] = []
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
