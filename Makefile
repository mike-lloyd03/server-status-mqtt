SHELL := /bin/bash

.PHONY: venv
venv: requirements.txt
	python -m venv .venv
	source .venv/bin/activate; pip install -r requirements.txt

.PHONY: deploy
deploy: 
	sed "s|WORKING_DIRECTORY|$(pwd)|g" deployment/systemd/server-status-mqtt.service > /etc/systemd/system/server-status-mqtt.service
	systemctl daemon-reload
