FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libsasl2-dev

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --no-cache-dir

COPY config.py /config.py
COPY entry_point.py /entry_point.py
COPY src /src

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 10000

ENTRYPOINT ["/entrypoint.sh"]