from smartpark import mqtt_device
import time
import json

class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""

    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')  # subscribed to "display" topic in carpark class.
        self.client.loop_forever()  # listen forever.

    def display(self, *args):
        print('*' * 20)
        for val in args:
            print(val) # then print them in this method.
            time.sleep(1)

        print('*' * 20)

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()  # takes the message
        self.display(*data.split(','))  # splits the message into 3 sections,
        # TODO: Parse the message and extract free spaces,\
        #  temperature, time


if __name__ == '__main__':
    if __name__ == '__main__':
        with open('/Users/taehyeon/Downloads/civ-ipriot-proj-carpark/samples_and_snippets/config.json', 'r') as file:
            # Read the contents of the file
            json_data = file.read()

            # Parse the JSON data into a Python object
            config = json.loads(json_data)
    # TODO: Read config from file
    display = Display(config)  # create an object of Display class, so its methods will run.
