IMAGE_NAME=beaker-run

.PHONY : run-checks
run-checks :
	isort --check .
	black --check .
	flake8 .
	mypy .

.PHONY : docker-image
docker-image :
	docker build -t $(IMAGE_NAME) .

.PHONY : test-run
test-run : docker-image
	docker run --rm $(IMAGE_NAME) '$(shell cat test_fixtures/hello_world.json)' \
		--token $$BEAKER_TOKEN \
		--workspace ai2/petew-testing \
		--timeout=-1 \
		--clusters ai2/general-cirrascale,ai2/allennlp-cirrascale
