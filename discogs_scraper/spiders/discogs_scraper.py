import scrapy
import os
import argparse
from scrapy.crawler import CrawlerProcess
class DiscogsScraper(scrapy.Spider):
    name =  'discogs_scraper'
    base_url = 'https://www.discogs.com'
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    def __init__(self,sort='want',rel_format='Vinyl',genre='Electronic',style='Electro',limit=10,*args, **kwargs):
        super(DiscogsScraper, self).__init__(*args, **kwargs)
        self.start_urls = [f'{self.base_url}/search/?sort={sort}%2Cdesc&genre_exact={genre}&style_exact={style}&format_exact={rel_format}&type=release']
        self.scraped_urls = set()
        self.page_limit = limit
        self.page_count = 0
        self.combination_seen = set()
    def start_requests(self):
        # Starts our requests with givin urls
        for urls in self.start_urls:
            yield scrapy.Request(url=urls,callback=self.parse_links)

    def parse_links(self,response):
        # We grab the response of that request and parse
        release_links = response.css('div.card-release-title  a::attr(href)').extract()

        for link in release_links:
            if link not in self.scraped_urls:
                self.scraped_urls.add(link)
                yield response.follow(link,callback=self.parse_release)

        if self.page_limit is not None and self.page_count >= self.page_limit:
            return

        next_page_link = response.css('a.pagination_next::attr(href)').extract_first()

        if next_page_link:
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page_link),callback=self.parse_links)

    def parse_release(self, response):
        artist = response.css('h1.title_1q3xW span.link_15cpV a::text').extract_first()
        title = response.xpath('//h1[@class="title_1q3xW"]/text()[last()]').get().strip()
        label = response.css('th:contains("Label") + td a::text').get()
        rel_format = response.css('th:contains("Format") + td a::text').get()
        release_date = response.css('th:contains("Released") + td time::attr(datetime)').extract_first()
        genre = response.css('th:contains("Genre") + td a::text').get()
        styles = response.css('th:contains("Style") + td a::text').getall()
        have = response.css('div.items_3gMeU a::text').extract()[0]
        want = response.css('div.items_3gMeU a::text').extract()[1]
        ratings = response.css('div.items_3gMeU a::text').extract()[2]
        prices = [(selector.extract()) for selector in response.css('span::text') if '€' in selector.extract()]
        avg_rating = response.css('span:contains("Avg Rating") + span::text').extract_first()
        date_list = response.css('a.link_1ctor time::attr(datetime)').getall()
        if date_list == []:
            last_sold = 'Never'
        elif len(date_list) > 1:
            last_sold = date_list[-1]
        else:
            last_sold = date_list[0]
        if len(prices) > 3:
            lowest_sold = prices[1]
            medium_sold = prices[2]
            highest_sold = prices[3]
        elif len(prices) > 2:
            lowest_sold = prices[0]
            medium_sold = prices[1]
            highest_sold = prices[2]
        else:
            lowest_sold = prices[0] if len(prices) > 0 else None
            medium_sold = prices[1] if len(prices) > 1 else None
            highest_sold = prices[2] if len(prices) > 2 else None

        combination = (artist, title)
        if combination not in self.combination_seen:
            self.combination_seen.add(combination)
            yield {
                'artist': artist,
                'title': title,
                'label': label,
                'format': rel_format,
                'release_date': release_date,
                'genre': genre,
                'styles': styles,
                'have': have,
                'want': want,
                'amount_of_ratings': ratings,
                f'average_rating':f"{avg_rating}/5",
                'last_sold_date': last_sold,
                'lowest_sold': lowest_sold,
                'median_sold': medium_sold,
                'highest_sold': highest_sold
            }



if __name__ == "__main__":
    # Create arg parse object
    parser = argparse.ArgumentParser(description='Scrape Discogs release data')
    # Add arguements to the parser
    parser.add_argument('-so', '--sort', type=str, default='want',help='Sort format:hot,most wanted,most collected,(default: most  wanted)')
    parser.add_argument('-f','--format',type=str,default='Vinyl',help='Release format (default: Vinyl)')
    parser.add_argument('-g','--genre',type=str,default='Electronic',help='Release genre (default: Electronic)')
    parser.add_argument('-s','--style',type=str,default='Electro',help='Release style (default: Electro)')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Limit the number of pages to scrape (default: 10)')
    parser.add_argument('-o', '--output', type=str, default='csv', choices=['csv', 'json'], help='Output format: csv or json (default: csv)')



    args = parser.parse_args()
    output_file = f"discogs_data.{args.output}"
    output_format = f"{args.output}"

    process = CrawlerProcess({
        'FEED_FORMAT': output_format,
        'FEED_URI': output_file,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_ENSURE_ASCII': False
    })


    process.crawl(DiscogsScraper,sort=args.sort, rel_format=args.format, genre=args.genre, style=args.style, limit=args.limit)
    process.start()
