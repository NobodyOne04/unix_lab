import logging

from bs4 import BeautifulSoup
from bs4.element import Tag

from config import (
    INPUT_PATH,
    OUTPUT_DIR,
)
from src.functions import (
    read_html_file,
    write_json_file,
)


def parse_title(item: Tag) -> str:
    return item.find_all(
        'h3'
    )[0].find_all(
        'a'
    )[0].text


def parse_description(item: Tag) -> str:
    description_args: dict = {
        'class': 'text-muted'
    }
    return item.find_all(
        'p',
        description_args
    )[-1].text


def parse_rate(item: Tag) -> float:
    rate_args: dict = {
        'class': 'inline-block ratings-imdb-rating'
    }
    return item.find_all(
        'div',
        rate_args
    )[0].text


def parse_genre(item: Tag) -> list:
    genre_args: dict = {
        'class': 'genre'
    }
    return item.find_all(
        'span',
        genre_args
    )[0].text.split()


def parse_items(html: str) -> dict:
    result: dict = {}
    item_args: dict = {
        'class': 'lister-item mode-advanced'
    }
    soup = BeautifulSoup(html)
    for item in soup.find_all('div', item_args):
        result['title'] = parse_title(item)
        result['description'] = parse_description(item)
        result['genre'] = parse_genre(item)
        result['rate'] = parse_rate(item)
    return result


def process() -> None:
    logging.debug('Start')
    for file in INPUT_PATH.glob('*.html'):
        logging.debug(f'Process {file.name}')

        path_to_file = OUTPUT_DIR / f'{file.name}.json'

        html_data = read_html_file(file)
        parsed = parse_items(html_data)
        write_json_file(
            parsed,
            path_to_file
        )
    logging.debug('Finish')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    )
    process()
