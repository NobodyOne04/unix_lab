from os import listdir

import os
import json

from lxml import html

import config

temp_dict = {
  "Name"        : None,
  "Rating"      : None,
  "Description" : None,
  "Director"    : None,
  "Writer"      : None,
  "Star"        : None
}

def read_file(filename):
    with open(filename, 'r' ,encoding='utf8') as file:
        text = file.read()
    return text

def save_json(data, filename):
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def check_value(value):
    if not value: 
        return None

    new_value = value[0] if len(value) == 1 else value
    new_value = formatting_value(new_value)

    return new_value

def check_name(name):
    name = " ".join(name.split())
    return name[0:-1] if name[-1] == 's' else name

def formatting_value(string):
    if not isinstance(string, list):
        return  " ".join(string.split())
    else:
        return string[0:-1] if string[-1] == 'See full cast & crew' else string

def parse_film_data(filename): 
    tree = html.fromstring(read_file(filename))

    film_name = tree.xpath('//div[@class="title_wrapper"]/h1/text()')[0]
    film_rating = tree.xpath('//span[@itemprop="ratingValue"]/text()')
    film_description = tree.xpath('//div[@class="summary_text"]/text()')[0]

    temp_dict['Name'] = check_value(film_name)
    temp_dict['Rating'] = check_value(film_rating)
    temp_dict['Description'] = check_value(film_description)

    film_data = tree.xpath('//div[@class="credit_summary_item"]')

    for item in film_data:
        name = item.xpath('./h4[@class="inline"]/text()')[0][0:-1]
        value = item.xpath('./a/text()')

        temp_dict[check_name(name)] = check_value(value)

    return temp_dict

def start_parse():
    if not os.path.exists(config.SAVE_PATH):
        os.mkdir(config.SAVE_PATH)
    files = listdir(config.SOURCE_PATH)
    for item in files:
        result = parse_film_data(config.SOURCE_PATH + item)
        save_json(result, config.SAVE_PATH + item[0:-4] + '.json')

if __name__ == '__main__':
    start_parse()

