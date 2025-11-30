#!/usr/bin/env python
import argparse
import json
import logging
import random
from paho.mqtt import client as mqtt_client
import socket
import time

__author__ = "Roger Huang"
__copyright__ = "Copyright 2025, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "1.0.0"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Testing"

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

def connect_mqtt(broker: str, port: int, client_id: str):
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id,
                                callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def register_dump(client: mqtt_client.Client, topic: str, obj: dict) -> None:
    word = obj.get('WORD')
    if word:
        print(word)
        st = client.publish(topic, json.dumps(word))
        if st[0]:
            logging.error(f'Failed({st}) to send message to topic {topic}')

    bit = obj.get('BIT')
    if bit:
        print(bit)
        st = client.publish(topic, json.dumps(bit))
        if st[0]:
            logging.error(f'Failedi({st}) to send message to topic {topic}')


def tag_dump(client: mqtt_client.Client, topic: str, obj: dict) -> None:
    name = obj.get('name')
    tmp_val = obj.get('value')
    try:
        val = int(tmp_val)
    except ValueError:
        val = tmp_val
    tag = {name:val}
    print(tag)
    st = client.publish(topic, json.dumps(tag))
    if st[0]:
        logging.error(f'Failed({st[0]}) to send message to topic {topic}')


def main():
    opts = argparse.ArgumentParser(description='Flat JSON format data to MQTT')
    opts.add_argument('-u', '--url', 
                      type=str,
                      required=True,
                      help='The device url - [hostname:]port, e.g. 127.0.0.1:51820')
    opts.add_argument('-b', '--broker', help='MQTT broker IP', type=str, required=True)
    opts.add_argument('-p', '--port', help='MQTT broker port, default is 1883', type=int, default=1883)
    opts.add_argument('-t', '--topic', type=str, required=True, help="MQTT publish topic")
    opts.add_argument('--username', help='MQTT connect user name', type=str)
    opts.add_argument('--password', help='The passowrd for MQTT server', type=str)
    args = opts.parse_args()

    url = args.url.split(':')
    host = '127.0.0.1' if len(url) == 1 else url[0]
    port = int(url[-1])

    client = connect_mqtt(args.broker, args.port,
                          f'python-mqtt-{random.randint(0, 1000)}')
    client.disconnect = on_disconnect
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        classes = {
            'DIFFER': register_dump,
            'TAG': tag_dump,
        }

        sock.connect((host, port))
        while True:
            tmp = sock.recv(16384).decode().splitlines()
            if len(tmp) == 0:
                print('EOF of the device server')
                break
            for ln in tmp:
                try:
                    payload = json.loads(ln)
                except json.decoder.JSONDecodeError as e:
                    print(f'{ln}, {e}')

                cls = payload.get('class')
                if cls is None:
                    print(f'No class on {payload}')
                    continue
                cls_hdl = classes.get(cls)
                if cls_hdl:
                    cls_hdl(client, args.topic, payload)
                else:
                    print(f'No handler for {payload}')
    client.loop_stop()


if __name__ == "__main__":
    main()
