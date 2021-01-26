import os
import json
from kafka import KafkaProducer
from website_checker import WebsiteChecker
from dotenv import load_dotenv

load_dotenv()

TOPIC_NAME = 'website-status'


def producer_loop(url):
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('SERVICE_URI'),
        security_protocol="SSL",
        ssl_cafile=os.getenv('CA_PATH'),
        ssl_certfile=os.getenv('CERT_PATH'),
        ssl_keyfile=os.getenv('KEY_PATH'),
    )

    checker = WebsiteChecker(url, delay=5)
    for counter, message in enumerate(checker.start_checker()):
        print(f'[{counter}] got result {str(message)} for {url}')
        producer.send(TOPIC_NAME, json.dumps(message).encode('utf-8'))

    producer.flush()
