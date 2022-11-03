# edgeflex-storage-manager

This is the repository for the edgeFLEX storage manager service. The purpose of this service is to route data captured by the subscriber and data manager to the appropriate database within `edgeflex-persistance`. 

## Preconditions
* git installed and access to the relevant code bases
* docker installed
* docker-compose installed
* An instance of edgeflex-persistance must be running, with the relavent databases created and configured.
  
## Deployment
To deploy the storage manager, navigate to the base directory in the terminal and 

`make run` to run the `edgeflex-storage-manager` service.

`make cleanup` to cleanup.

The following are also created and will be removed with the cleanup:
### Networks
edgeflex-network
### Images
edgeflex-storage-manager-image
python:3

## Endpoints

The following REST endpoint is available on the storage manager:

* Address: `/storage`

* Methods: POST
* Content: application/json
* Description: The purpose of this endpoint is to ingest data from the subscriber and data manager. This is not an externally facing endpoint, and it should only be made available to other services within the edgeFLEX platform. The data should be in a particular format, with a `topic` key and value which determines the Influx database where the data is to be stored, and a `payload` key and value which is detailed [here](https://gitlab-ee.waltoninstitute.ie/edgeflex/development/edgeflex-storage-manager/-/issues/1).