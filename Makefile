.DEFAULT_GOAL := all

DIR:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: all
all: metrics

.PHONY: train
train: server

.PHONY: metrics
metrics: iot dashboard

.PHONY: iot
iot:
	$(DIR)/metrics/deploy-iot.sh -s Donkey-Metrics-Iot

.PHONY: dashboard
dashboard:
	$(DIR)/metrics/deploy-website.sh -s Donkey-Metrics-Dashboard

.PHONY: server
server: 
	$(DIR)/train/deploy-server.sh -s Donkey-Train-Server
	
