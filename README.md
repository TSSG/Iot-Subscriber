# IoT Subscriber

This is a utility that captures data from an MQTT broker and routes it to an InfluxDB 2.X database. The routing information provided by the topic under which the data is published in the following format: `bucket/measurement/tag1/tag2/tag3...`. The Subscriber can insert data that is already structured to be written to InfluxDB, or unstructured data where any fields with a name matching one of the tags passed in through the topic are written to the database as tags.

### Sample structured data:
```json
{
	"time": 1682060040000,
	"fields": {
		"value": 50
	},
	"tags": {
		"location": "waterford"
	}
}
```

### Sample unstructured data:
```json
{
	"time": 1682050040000,
	"value": 100,
	"val_list": [60, 70, 80],
	"location": "waterford"
}
```

## Preconditions
* GNU Make
* docker & docker-compose
* Existing InfluxDB containers should be added to the `subscriber-network` docker network. This has been done in the optional deployment below.
* The conf.env file in the base directory should be populated with credentials for connecting to the MQTT broker and to the InfluxDB container.

## Database deployment (optional)
In the case where there is no pre-existing InfluxDB container, a method to deploy one has been provided. 

To preconfigure the InfluxDB instance with username, password, retention policy, default bucket, etc, uncomment the first line in `db/conf.env` and fill out the relevant fields. 

The URL for the container should be added to the conf.env at the base directory, eg, `DB_URL=http://iot-subscriber-persistance:8086`. 

The data will persist in `db/storage/` and the configuration in `db/config/` if the InfluxDB container should exit.

To deploy the InfluxDB container, `make build_db` from the base directory.

## Deployment
To deploy the Subscriber, navigate to the base directory in the terminal and 

`make run` to run the `IoT Subscriber` service.

`make cleanup` to cleanup.

## License

Maintained by [Jack Jackman](mailto:jack.jackman@waltoninstitute.ie) at the Walton Institute under the South East Technological University.

This work was funded under the European Union Horizon 2020 research and innovation programme under grant agreement No 883710, project edgeFLEX (Providing flexibility to the grid by enabling VPPs to offer both fast and slow dynamics control services).

This utility is released under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).