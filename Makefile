.PHONY: build run clean test

APP_NAME = titan-warfare
VERSION = 17.0

build:
	@echo "[*] BUILDING CONTAINER IMAGE..."
	docker build -t $(APP_NAME):$(VERSION) .

run:
	@echo "[*] DEPLOYING TITAN C2..."
	# Maps local DB file to container so data persists
	docker run -it --rm -v $(PWD)/titan_operations.db:/app/titan_operations.db $(APP_NAME):$(VERSION)

test:
	@echo "[*] RUNNING PHYSICS INTEGRITY CHECKS..."
	python3 -m pytest tests/

clean:
	@echo "[*] SCRUBBING ARTIFACTS..."
	rm -rf build dist *.egg-info __pycache__
	rm -f *.log
