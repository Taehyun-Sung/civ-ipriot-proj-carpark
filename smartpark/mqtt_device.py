import paho.mqtt.client as paho
import json


class MqttDevice:
    if __name__ == '__main__':
        with open('/Users/taehyeon/Downloads/civ-ipriot-proj-carpark/samples_and_snippets/config.json', 'r') as file:
            # Read the contents of the file
            json_data = file.read()

            # Parse the JSON data into a Python object
            config = json.loads(json_data)

    def __init__(self, config):
        self.name = config['CarParks'][0]['name']  # Access the name key from the nested structure
        self.location = config['CarParks'][0]['location']

        # Define topic components:
        self.topic_root = config['CarParks'][0]['topic-root']
        self.topic_qualifier = config['CarParks'][0]['topic-qualifier']
        self.topic = self._create_topic_string()

        # Configure broker
        self.broker = config['CarParks'][0]['broker']
        self.port = config['CarParks'][0]['port']

        # Initialise a paho client and connect to the broker
        self.client = paho.Client()
        self.client.connect(self.broker, self.port)

    def _create_topic_string(self):
        return (f"{self.topic_root}/{self.location}/" +
                f"{self.name}/{self.topic_qualifier}")


