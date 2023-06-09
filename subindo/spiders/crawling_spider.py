import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy


class CrawlingSpider(CrawlSpider):
    name = 'mycrawler'
    allowed_domains = ['espn.com.br']
    start_urls = [
        'https://www.espn.com.br/nba/time/_/nome/mil/milwaukee-bucks']

    rules = (
        Rule(LinkExtractor(
            allow=""), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        name1 = response.css('span.db.pr3.nowrap::text').get()
        name2 = response.css('span.db.fw-bold::text').get()
        Win = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div/div/div/ul/li[1]/text()').get()
        yield {
            'name': name1,
            'surname': name2,
            'vd': Win,
        }
        
    def print_info(self, result):
        with open("output.txt", "a") as f:
            for item in result:
                name = item.get('name')
                surname = item.get('surname')
                wins = item.get('wins')

                f.write(f"Name: {name} {surname}\n")
                f.write(f"Wins: {wins}\n")
                f.write("\n")
        f.close()

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    deferred = process.crawl(CrawlingSpider)
    deferred.addCallback(CrawlingSpider().print_info)
    process.start()

