import scrapy

class UFCStatsSpider(scrapy.Spider):
    name = 'ufcstats_spider'
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']

    def parse(self, response):
        for row in response.css('tbody tr'):
            fight_name = row.css('a::text').get()
            if fight_name:
                yield {'fight_name': fight_name.strip()}
