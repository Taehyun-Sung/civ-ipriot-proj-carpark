import random
import json
from datetime import datetime
from smartpark import mqtt_device
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['CarParks'][0]['total-spaces']
        self.total_cars = config['CarParks'][0]['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')  # subscribes to "sensor" topic, in sensor class.
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(0, min(available, self.total_spaces))

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        temperature = random.randint(10, 35)
        print(
            (
                    f"TIME: {readable_time}, "
                    + f"SPACES: {self.available_spaces}, "
                    + f"TEMP: {temperature}℃"
            )
        )
        if self.total_cars > 0:
            message = (
                    f"TIME: {readable_time}, "
                    + f"SPACES: {self.available_spaces}, "
                    + f"TEMP: {temperature}℃"
            )
        else:
            message = "The car park is empty"
        if self.available_spaces == 0:
            message = "The car park is full"
        self.client.publish('display', message)  # sends the message to subscriber with topic "display"

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        if self.total_cars > 0:
            self.total_cars -= 1
            self._publish_event()
        else:
            self._publish_event()
        if self.available_spaces == 0:
            self.total_cars -= 1
            self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    with open('/Users/taehyeon/Downloads/civ-ipriot-proj-carpark/samples_and_snippets/config.json', 'r') as file:
        # Read the contents of the file
        json_data = file.read()

        # Parse the JSON data into a Python object
        config = json.loads(json_data)

    car_park = CarPark(config)
    print("Carpark initialized")
