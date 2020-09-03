# Flask parameters
DOCKER_IMAGE=trading-api
DOCKER_TAG=latest
HOST_PORT=8080

all: build docker
build: 
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
docker:
	docker run -p $(HOST_PORT):$(HOST_PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)
deploy: 
	gcloud builds submit --config cloudbuild.yaml .