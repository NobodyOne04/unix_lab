FROM aciobanu/scrapy
USER root

COPY entrypoint.sh .
COPY imdb_spider .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
