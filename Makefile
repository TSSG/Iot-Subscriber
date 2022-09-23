run:
	docker build -t edgeflex-base-image -f build/Dockerfile . 
	cd ./build && \
	docker-compose up --remove-orphans -d --force-recreate edgeflex-storage-manager
cleanup:
	cd ./build && docker-compose -f docker-compose.yml down --rmi local -v --remove-orphans;
	docker image rm -f edgeflex-base-image:latest;

