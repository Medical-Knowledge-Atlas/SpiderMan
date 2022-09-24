import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Procurement_258"
    base_link = ''
    hospital_name = '淮安市第二人民医院'

    def start_requests(self):
        # 初始页
        urls = []
        for i in range(17):
            if i == 0:
                list_url = 'https://www.rcstar.com/hospital/zbgs/index.html'
            else:
                list_url = 'https://www.rcstar.com/hospital/zbgs/index_{}.html'.format(i + 1)
            urls.append(list_url)
        print(urls)
        params = {
            # "hospital": "1010",
            # "category": "32",
            # "tag": "",
            # "size": "8",
            # "pageNum": "1",
            # "type": "0",
            # "status": "1",
            # "_": f'{int(time.time())}'
        }
        self.hospital_url = 'https://www.rcstar.com/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            print("第{}页".format(index + 1))
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//p[@class='tit']/a/@href")

        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//h1[@class='title']/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="view"]/span/text()').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@class="articleTxt"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if (len(annex_url) != 0) and (len(annex_title) != 0):
            annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
            item['annex_link'] = annex_link
            item['annex_title'] = annex_title.extract()[0]
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
