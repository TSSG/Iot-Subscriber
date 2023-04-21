run:
	docker build -t iot-subscriber-image -f build/Dockerfile . 
	cd ./build && \
	docker-compose up --remove-orphans -d --force-recreate iot-subscriber

build_db:
	cd ./db && \
	docker-compose up -d

cleanup:
	cd ./build && docker-compose -f docker-compose.yml down --rmi local -v --remove-orphans;
	docker image rm -f iot-subscriber-image:latest;

