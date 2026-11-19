# unix_lab

A 2021 team project: IMDb → Hive → Spark Word2Vec film recommendations, stages as Docker images
run by Airflow.

## Commands
```sh
make build/airflow build/crawlers/all build/parsers/all build/loader   # images (make setup doesn't build them)
make up / make down          # Airflow + Hive
make run/crawlers/imdb       # one stage by hand; also run/parsers/imdb
```
No tests.

## Layout
- `crawlers/imdb/` (Scrapy), `parsers/imdb/` (BeautifulSoup), `loaders/` (PyHive + `docker-hive/`),
  `core/ml_engine/` (PySpark Word2Vec), `core/api/` (empty), `airflow/` (compose, Dockerfile, `dags/`).
- Image names the DAGs expect: `crawler-imdb`, `parser-imdb`, `hive_loader`, `word2vec`.
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- Each stage reads and writes through mounted `data/` folders (`INPUT_DIR` / `OUTPUT_DIR`).
- `airflow/docker-compose.yml` has a fixed Fernet key and default passwords: local only.
- Archived project: docs or small fixes only unless asked.
