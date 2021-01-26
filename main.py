import argparse
import sys

from consumer import consumer_loop
from producer import producer_loop


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--consumer', action='store_true', default=False, help="Run Kafka consumer")
    parser.add_argument('--producer', action='store_true', default=False, help="Run Kafka producer")
    parser.add_argument('--url', default=False, help="Website url")
    args = parser.parse_args()

    validate_args(args)

    kwargs = {k: v for k, v in vars(args).items() if k not in ("producer", "consumer")}
    if args.producer:
        producer_loop(**kwargs)
    elif args.consumer:
        consumer_loop()


def validate_args(args):
    if args.producer and args.consumer:
        fail("--producer and --consumer are mutually exclusive")
    elif not args.producer and not args.consumer:
        fail("--producer or --consumer are required")
    if args.producer and not args.url:
        fail("url should be provided for producer")


def fail(message):
    print(message, file=sys.stderr)
    exit(1)


if __name__ == '__main__':
    main()
