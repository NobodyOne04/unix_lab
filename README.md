# unix_lab

A scalable **film recommendation system** (team university project, 2021): crawl IMDb, parse the
pages, load films into Hive, train a Spark Word2Vec model, and recommend similar films by vector
similarity. Each stage is a Docker image orchestrated by Airflow.

## Pipeline

```
extract_dag (hourly at :05):  crawler-imdb ──► parser-imdb ──► hive_loader ──► Hive
train_dag   (hourly at :05):  wait for Hive commit ──► word2vec (train) ──► deploy
```

| Stage | Folder | What |
|---|---|---|
| Crawl | `crawlers/imdb/` | Scrapy spider, writes raw pages to `data/crawlers/imdb` |
| Parse | `parsers/imdb/` | BeautifulSoup/lxml → JSON films in `data/parserout/imdb` |
| Load | `loaders/` | PyHive loader into Hive; `loaders/docker-hive/` runs a Hive cluster |
| Train | `core/ml_engine/` | PySpark `Word2Vec` on film descriptions, vectors saved to a Hive table; cosine similarity for "similar films" |
| Orchestrate | `airflow/` | Airflow (LocalExecutor) with `DockerOperator` DAGs `extract_dag` and `train_dag` |
| API | `core/api/` | planned, empty |

## Run

Built for Ubuntu with Docker and docker-compose:

```sh
make install            # Docker + docker-compose 1.23 (Ubuntu bionic, uses sudo)
make setup              # data folders, Airflow's .environment, then builds every image
make up                 # Airflow (4 workers) + Hive; Airflow UI on http://localhost:8080
make down               # stop both;  make prune  wipes Docker and data/
```

The Airflow compose file uses the default `airflow` / `airflow` Postgres login: local use only.

Decisions: [docs/adr](docs/adr/README.md).
