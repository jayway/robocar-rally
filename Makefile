.DEFAULT_GOAL := build

AWS_DIR := $(HOME)/.aws
TMP_DIR := $(shell mktemp -u)

.PHONY: build
build:
	docker build -t ansible .

.PHONY: deploy-test
deploy-test: build
		docker run --rm -e env=dev -v $(AWS_DIR):/root/.aws ansible