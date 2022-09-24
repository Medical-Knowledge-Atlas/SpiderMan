
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider
from lxml import etree


class Resume267(ResumeBaseSpider):
    name = "Resume267"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.wxlx.gov.cn/intertidwebapp/department/departmentDetailJson',
        ]
        data = {
            "chanId": "45176"
        }
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata=data)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.json()['departmentVO']['leaders']
        # 解析列表页
        for data in datas:
            save = {}
            save['ori_url'] = 'http://www.jsxishan.gov.cn/qczj/zfxxgk/zfxxgkml_1/index.shtml'
            save['name'] = data['leaderName']
            save['tag'] = "江苏_无锡_锡山区_区财政局"
            save['status'] = data['leaderPost']
            save['division'] = data['leaderLabor']
            save['resume'] = data['leaderResume']
            print(save)
            yield save

