#!make

install: install_docker install_docker_compose

setup:
	@mkdir -p $$(pwd)/data/

clean:
	sudo rm -rf $$(pwd)/data/*

prune:
	docker system prune -af
	sudo rm -rf $$(pwd)/data/*

build/airflow:
	docker build airflow -t airflow

build/parsers/all:
	$(foreach src,$(wildcard ./parsers/*),$(MAKE) build/parsers/$(notdir $(src)) && ) true

build/crawlers/all:
	docker build -t crawler crawlers

run/crawlers/%:
	@mkdir -p $$(pwd)/data/crawlers/$(notdir $@)
	docker run --rm \
	    --name $(notdir $@)-crawler \
		-e DATA_DIR=/data \
		-v $$(pwd)/data/crawlers/$(notdir $@):/data \
		-v $$(pwd)/crawlers:/code \
		$(notdir $@)

run/parsers/%:
	@mkdir -p $$(pwd)/data/parsers/$(notdir $@)
	docker run --rm --env-file .secrets --env-file .settings \
		-v $$(pwd)/parsers/$(notdir $@)/app:/app \
		-v $$(pwd)/data:/data \
		-v $$(pwd)/data/crawlers/$(notdir $@):/input \
		-v $$(pwd)/data/parserout/$(notdir $@):/output \
		$(notdir $@)

up:
	docker-compose -f $$(pwd)/airflow/docker-compose.yml up -d --scale worker=8

down: airflow/down
	echo "Done!"

