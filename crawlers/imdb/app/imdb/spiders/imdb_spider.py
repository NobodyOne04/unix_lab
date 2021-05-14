from scrapy import (
    Spider,
    Request,
)

from .config import (
    START_URL,
    OUTPUT_DIR,
    NEXT_PAGE_POINTER,
)


class ImdbSpider(Spider):
    name = 'imdb'

    def start_requests(self):
        yield Request(
            url=START_URL,
            callback=self.parse
        )

    @staticmethod
    def save_response(response, path_to_file):
        with open(path_to_file, 'w') as html_file:
            html_file.write(response.text)

    def parse(self, response, **kwargs):
        page_number = str(response.url).split('&')[-1]

        self.save_response(
            response,
            OUTPUT_DIR / f"{page_number}.html"
        )

        next_page = response.xpath(NEXT_PAGE_POINTER)

        if next_page:
            yield response.follow(
                url=next_page.get(),
                callback=self.parse
            )
