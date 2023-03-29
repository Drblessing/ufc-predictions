import scrapy

class UFCStatsSpider(scrapy.Spider):
    name = 'ufcstats_spider'
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']
    just_fight_names = False

    def parse(self, response):
        for row in response.css('tbody tr'):
            fight_name = row.css('a::text').get()
            if fight_name:

                if self.just_fight_names:
                    yield {'fight_name': fight_name.strip()}
                    continue
                detail_link = row.css('a::attr(href)').get()
                yield scrapy.Request(detail_link, callback=self.parse_fight_data, meta={'fight_name': fight_name.strip()})


    def parse_fight_data(self, response):
        # Extract fight data from the fight detail page
        # For example, to extract the event date:
        event_date = response.css("i.b-flag__text::text").get()

        rows = response.css('tbody tr')
        fight_data = []
        for row in rows:
            fighters = row.xpath('td[2]//a')
            fighters_data = []
            for i,fighter in enumerate(fighters):
                fighter_name = fighter.xpath('text()').get().strip()
                fighters_data.append(fighter_name)

            
            fight_data.append({
                'fighter_1': fighters_data[0],
                'fighter_2': fighters_data[1],
            })

        fight_name = response.meta['fight_name']
        yield {'fight_name':fight_name,'event_date': event_date, 'fight_data': fight_data}