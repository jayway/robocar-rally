.DEFAULT_GOAL := all

.PHONY: all
all: iot

.PHONY: iot
iot:
	aws cloudformation deploy --template-file ./templates/iot.yaml --stack-name Donkey-Iot --capabilities CAPABILITY_IAM