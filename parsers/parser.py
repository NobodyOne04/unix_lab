from lxml import html
from lxml import etree
from os import listdir

import os.path
import json

souce_path = "drive/MyDrive/souce/"
save_path = "result/"

prase_parameters = {
    "Name",
    "Rating",
    "Description",
    "Director",
    "Writer",
    "Star"
}

def read_file(filename):
  with open(filename, 'r' ,encoding='utf8') as file:
    text = file.read()
  return text

def make_json(data, filename):
  with open(filename, 'w', encoding='utf8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

def check_value(value):
  new_value = value[0] if len(value) == 1 else value
  new_value = delete_trash_from_string(new_value)

  if not new_value:
    return None

  return new_value

def check_name(name):
  new_name = name[0:-1] if name[-1] == 's' else name
  return delete_trash_from_string(new_name)

def init_dict():
  temp_dict = dict()
  for item in prase_parameters:
    temp_dict[item] = None

  return temp_dict

def delete_trash_from_string(string):
    if not type(string) is list:
      return  " ".join(string.split())
    else:
      return string
  

def parse_film_data(filename): 
  result = []
  temp_dict = init_dict()

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

def start_prase():
  files = listdir(souce_path);
  for item in files:
    result = parse_film_data(souce_path + item)
    make_json(result, save_path + item[0:-4])