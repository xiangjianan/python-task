import time
import random

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from fang58.items import Fang58Item
from scrapy_redis.spiders import RedisCrawlSpider


class FangSpider(RedisCrawlSpider):
    """
    爬虫类
    """
    name = 'fang'

    # 可以被共享的调度器队列名称
    redis_key = 'fang1'

    # 规则解析器，解析所有分页
    rules = (
        Rule(LinkExtractor(allow=r'/ershoufang/pn\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        获取当前页面所有房源的基本信息，存入item，并发送到共享的scrapy-redis管道
        :param self:
        :param response:
        :return:
        """
        tr_list = response.xpath('//ul[@class="house-list-wrap"]/li')
        for tr in tr_list:
            # 房源基本信息
            url = tr.xpath('./div[2]/h2/a/@href').extract_first()
            info = ' / '.join(tr.xpath('./div[2]/p[1]/span/text()').extract())
            location = ' '.join(tr.xpath('./div[2]/p[2]/span[1]/a//text()').extract())
            location_2 = ' '.join(tr.xpath('./div[2]/p[2]/span[2]/text()').extract())
            people = ' '.join(tr.xpath('./div[2]/div/span/text()').extract())
            people2 = ' '.join(tr.xpath('./div[2]/div/a/span/text()').extract())
            price = ''.join(tr.xpath('./div[3]/p[1]//text()').extract())
            per_price = tr.xpath('./div[3]/p[2]/text()').extract_first()

            # 存入item
            item = Fang58Item()
            item['url'] = url
            item['location'] = location + location_2
            item['people'] = people + people2
            item['info'] = info
            item['price'] = price
            item['per_price'] = per_price
            print('已获取：', info, price, per_price)

            # 发送到共享的scrapy - redis管道
            yield item
        time.sleep(random.randint(50, 100) / 100)

    def parse(self, response, **kwargs):
        pass
