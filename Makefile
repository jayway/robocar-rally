.DEFAULT_GOAL := all

.PHONY: all
all: iot server

.PHONY: iot
iot:
	aws cloudformation deploy --template-file ./templates/iot.yaml --stack-name Donkey-Iot --capabilities CAPABILITY_IAM

.PHONY: iot
server:
	aws cloudformation deploy --template-file ./templates/donkey-server.yaml --stack-name donkey-server --capabilities CAPABILITY_IAM
