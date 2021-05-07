#!make

install: install_docker install_docker_compose

setup:
	@mkdir -p $$(pwd)/data/
	@mkdir -p $$(pwd)/data/crawler
	@mkdir -p $$(pwd)/data/parser
	echo HOST_DATA_DIR=$$(pwd)/data > $$(pwd)/airflow/.environment 

clean:
	sudo rm -rf $$(pwd)/data/*

prune:
	docker system prune -af
	sudo rm -rf $$(pwd)/data/*

build/airflow:
	docker build airflow -t airflow

build/parsers/%:
	docker build --no-cache -t parser-$(notdir $@) parsers/$(notdir $@)

build/crawlers/%:
	docker build --no-cache -t crawler-$(notdir $@) crawlers/$(notdir $@)

build/parsers/all:
	$(foreach src,$(wildcard ./parsers/*),$(MAKE) build/parsers/$(notdir $(src)) && ) true

build/crawlers/all:
	$(foreach src,$(wildcard ./crawlers/*),$(MAKE) build/crawlers/$(notdir $(src)) && ) true

run/crawlers/%:
	@mkdir -p $$(pwd)/data/crawlers/$(notdir $@)
	docker run --rm \
	    --name $(notdir $@)-crawler \
	    -v $$(pwd)/parsers/$(notdir $@)/app:/app \
		-v $$(pwd)/data/crawlers/$(notdir $@):/data \
		-v $$(pwd)/crawlers:/code \
		-e OUTPUT_DIR=/data \
		$(notdir $@)

run/parsers/%:
	@mkdir -p $$(pwd)/data/parsers/$(notdir $@)
	docker run --rm \
		-v $$(pwd)/parsers/$(notdir $@)/app:/app \
		-v $$(pwd)/data/crawlers/$(notdir $@):/input \
		-v $$(pwd)/data/parserout/$(notdir $@):/output \
		-e INPUT_DIR=/input \
		-e OUTPUT_DIR=/output \
		$(notdir $@)

airflow/down:
	docker-compose -f $$(pwd)/airflow/docker-compose.yml down

airflow/up:
	docker-compose -f $$(pwd)/airflow/docker-compose.yml up -d --scale worker=4

up: airflow/up

down: airflow/down

