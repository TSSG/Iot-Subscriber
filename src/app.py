import time
import mqtt_interface


if __name__ == '__main__':
    mqtt_interface.connect_mqtt_client()
    while True:
        time.sleep(1)