IMAGE_NAME = "fastui-starter-tester"

.Phony: build
build: Dockerfile
	docker build -t $(IMAGE_NAME) .

.Phony: run
run: build
	docker run $(IMAGE_NAME)
