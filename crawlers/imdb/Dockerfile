FROM aciobanu/scrapy
USER root

COPY entrypoint.sh .
COPY app .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
