import scrapy
from spider_steam.items import SpiderSteamItem


class SpidersteamproductSpider(scrapy.Spider):
    name = 'SpiderSteamProduct'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?g=n&SearchText=sports_and_racing&page=1',
                  'https://store.steampowered.com/search/?g=n&SearchText=sports_and_racing&page=2',
                  'https://store.steampowered.com/search/?g=n&SearchText=strategy&page=1',
                  'https://store.steampowered.com/search/?g=n&SearchText=strategy&page=2',
                  'https://store.steampowered.com/search/?g=n&SearchText=adventure&page=1',
                  'https://store.steampowered.com/search/?g=n&SearchText=adventure&page=2']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, response):
        games = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for game in games:
            yield scrapy.Request(game, callback=self.parse_for_game)

    def parse_for_game(self, response):
        items = SpiderSteamItem()
        name_of_product = response.xpath('//span[@itemprop="name"]/text()').extract()
        date_of_release_of_product = response.xpath('//div[@class="date"]/text()').extract()
        if name_of_product == [] or int(''.join(date_of_release_of_product).strip()[-4::]) < 2000:
            return
        category_of_product = response.xpath('//span[@data-panel]/a/text()').extract()
        rating_of_product = response.xpath('//span[@class = "responsive_reviewdesc_short"]/text()').extract()  # тут [0]
        if rating_of_product:
            rating_of_product = rating_of_product[0]
        developers_of_product = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        tags_of_product = response.xpath('//a[@class="app_tag"]/text()').extract()
        price_of_product = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()  # тут [0]
        if price_of_product:
            price_of_product = price_of_product[0]
        platforms_of_product = response.xpath('//div[@class="sysreq_tabs"]/div/text()').extract()
        items['name_of_product'] = ''.join(name_of_product).strip()
        items['category_of_product'] = ', '.join(map(lambda x: x.strip(), category_of_product)).strip()
        items['rating_of_product'] = ''.join(rating_of_product).strip().replace('(', '').replace(')', '')
        items['date_of_release_of_product'] = ''.join(date_of_release_of_product).strip()  #
        items['developers_of_product'] = ', '.join(map(lambda x: x.strip(), developers_of_product)).strip()
        items['tags_of_product'] = ', '.join(map(lambda x: x.strip(), tags_of_product)).strip()
        items['price_of_product'] = ''.join(price_of_product).strip().replace('уб', '')
        if not platforms_of_product:
            platforms_of_product = response.xpath(
                '//div[@class="game_area_purchase_game" or @class="game_area_purchase_game "]/div/span/@class').extract()
            if platforms_of_product:
                platforms_of_product = platforms_of_product[0]
            items['platforms_of_product'] = ''.join(platforms_of_product).strip().replace('platform_img ', '')
        else:
            items['platforms_of_product'] = ', '.join(map(lambda x: x.strip(), platforms_of_product)).strip()
        yield items
