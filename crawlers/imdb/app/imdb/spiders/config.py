import os
from pathlib import Path
from datetime import datetime

_current_date = datetime.today().strftime('%Y-%m-%d')

OUTPUT_DIR = Path(
    os.environ['OUTPUT_DIR']
).resolve()

NEXT_PAGE_POINTER = '//a[@class="lister-page-next next-page"]/@href'
START_URL = f'https://www.imdb.com/search/title/?title_type=feature&year=1900-01-01,{_current_date}&start=1'
