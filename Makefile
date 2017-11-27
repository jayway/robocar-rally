.DEFAULT_GOAL := deploy

.PHONY: deploy
deploy: deploy-iot

.PHONY: deploy-iot
deploy-iot:
	aws cloudformation deploy --template-file ./templates/iot.yaml --stack-name Donkey-Iot --capabilities CAPABILITY_IAM