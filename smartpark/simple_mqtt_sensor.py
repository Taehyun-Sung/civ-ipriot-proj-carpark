""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import json
import random
import paho.mqtt.client as paho

from smartpark import mqtt_device
from smartpark.mqtt_device import MqttDevice


class Sensor(mqtt_device.MqttDevice):
    def __init__(self, config):  # Sensor class' attributes are referred to config file, where all the infos are kept.
        super().__init__(config)
        self.name = config['CarParks'][0][
            "name"]  # so that people who don't code, can also access the config file(json) and change the value.
        self.location = config['CarParks'][0]["location"]
        self.broker = config['CarParks'][0]["broker"]
        self.port = config['CarParks'][0]["port"]
        self.client = paho.Client()
        self.client.connect(self.broker, self.port)
        self.topic = MqttDevice._create_topic_string(self)  # connected to the topic.

    @property
    def temperature(self):
        """Returns the current temperature"""
        return random.randint(10, 35)

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('sensor', message)  # publish the message argument to "sensor" topic

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            print("Press E when 🚗 entered!")
            print("Press X when 🚖 exited!")
            detection = input("E or X> ").upper()
            if detection == 'E':
                self.on_detection(f"entered, {self.temperature}")
            else:
                self.on_detection(f"exited, {self.temperature}")


if __name__ == '__main__':
    # when the program is run directly by the Python interpreter.
    # The code inside the if statement is not executed when the file's code is imported as a module.
    with open('/Users/taehyeon/Downloads/civ-ipriot-proj-carpark/samples_and_snippets/config.json', 'r') as file:
        # Read the contents of the file
        json_data = file.read()

        # Parse the JSON data into a Python object
        config = json.loads(json_data)
    sensor1 = Sensor(config)
    print("Sensor initialized")
    sensor1.start_sensing()
