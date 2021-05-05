from datetime import datetime

from scrapy import (
    Spider,
    Request,
)

from .config import IMDB_DIR


class ImdbSpider(Spider):
    name = 'imdb'
    current_date = datetime.today().strftime('%Y-%m-%d')
    base_url = f'https://www.imdb.com/search/title/?title_type=feature&year=1900-01-01,{current_date}&start={1}'

    def start_requests(self):
        yield Request(
            url=self.base_url,
            callback=self.parse
        )

    @staticmethod
    def save_response(response, path_to_file):
        with open(path_to_file, 'w') as html_file:
            html_file.write(response.text)

    def parse(self, response):
        file_name = str(response.url).split('&')[-1]
        file_name = f"{file_name}.html"
        self.save_response(response, IMDB_DIR / file_name)
        next_page = response.xpath('//a[@class="lister-page-next next-page"]/@href')
        if next_page:
            yield response.follow(
                url=next_page.get(),
                callback=self.parse
            )
