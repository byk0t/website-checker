import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
from storage import Storage

load_dotenv()

TOPIC_NAME = 'website-status'


def consumer_loop():
    consumer = KafkaConsumer(
        bootstrap_servers=os.getenv('SERVICE_URI'),
        auto_offset_reset='earliest',
        security_protocol="SSL",
        ssl_cafile=os.getenv('CA_PATH'),
        ssl_certfile=os.getenv('CERT_PATH'),
        ssl_keyfile=os.getenv('KEY_PATH'),
        consumer_timeout_ms=1000,
    )

    storage = Storage()
    try:
        consumer.subscribe([TOPIC_NAME])
        while True:
            msg = consumer.poll()
            if msg is None: continue
            if len(msg):
                process_message(msg, storage)
    finally:
        consumer.close()


def process_message(message, storage: Storage):

    for tp, messages in message.items():
        for message in messages:
            message_string = message.value.decode('utf-8')
            try:
                message_dict = json.loads(message_string)
            except:
                message_dict = {}
            storage.store_message(message_dict)

