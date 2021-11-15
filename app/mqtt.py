"""This module contains the primary logic for sending messages to the MQTT broker."""

import os

import paho.mqtt.client as mqtt
from config import Config
from dotenv import load_dotenv

from app.status import (get_disk_use_percent, get_hostname, get_last_boot,
                        get_memory_use, get_processor_temperature,
                        get_processor_use)

load_dotenv()

USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")
BROKER = os.getenv("MQTT_BROKER")
ENV = os.getenv("ENV", "production")

if not USERNAME or not PASSWORD or not BROKER:
    raise ValueError(
        "MQTT_USERNAME, MQTT_PASSWORD, and MQTT_BROKER environment variables must be set."
    )

config = Config()

PORT = config.PORT
CLIENT_ID = "server_status" if ENV == "production" else "server_status-dev"
hostname = get_hostname()
topic_prefix = f"{CLIENT_ID}/{hostname}/"


def connect_mqtt():
    """Makes a connection to the MQTT broker."""

    # pylint: disable-next=invalid-name
    def cb_on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker.")
        else:
            print(f"Failed to connect to MQTT broker. Return code {rc}")

    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = cb_on_connect
    client.connect(BROKER, PORT)
    return client


def send_status(client):
    """Publishes messages to the MQTT broker."""

    while True:
        if config.PROCESSOR_USE:
            topic = topic_prefix + "processor_use"
            result = client.publish(topic, get_processor_use(15))
            check_error(result, topic)

        if config.PROCESSOR_TEMPERATURE:
            topic = topic_prefix + "processor_temperature"
            result = client.publish(
                topic,
                get_processor_temperature(),
            )
            check_error(result, topic)

        if config.DISK_USE_PERCENT:
            for i, path in enumerate(config.DISK_PATHS):
                topic = topic_prefix + f"disk_use_percent_disk{i}"
                result = client.publish(
                    topic,
                    get_disk_use_percent(path),
                )
                check_error(result, topic)

        if config.MEMORY_USE:
            topic = topic_prefix + "memory_use"
            result = client.publish(topic, get_memory_use())
            check_error(result, topic)

        if config.LAST_BOOT:
            topic = topic_prefix + "last_boot"
            result = client.publish(topic, get_last_boot())
            check_error(result, topic)

        print("Messages sent.")


def check_error(result, topic):
    """Checks the result code of a message publish to the broker."""
    if result.rc != 0:
        raise Exception(
            f"Message to topic '{topic}' could not be sent. Error status: {result}"
        )
