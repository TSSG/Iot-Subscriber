build:
	cd ./src/ \
	&& docker build -t edgeflex-base-image -f Dockerfile .

run: 
	cd ./src && \
	docker-compose up --remove-orphans --force-recreate edgeflex-storage-manager
cleanup:
	cd ./src && docker-compose -f docker-compose.yml down --rmi local -v --remove-orphans;
	docker image rm -f edgeflex-base-image:latest;

