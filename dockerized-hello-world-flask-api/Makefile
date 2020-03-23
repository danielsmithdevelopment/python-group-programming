# Flask parameters
DOCKER_IMAGE=hello-flask
DOCKER_TAG=latest
HOST_PORT=5000

all: build docker
build: 
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
docker:
	docker run -p $(HOST_PORT):$(HOST_PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)
