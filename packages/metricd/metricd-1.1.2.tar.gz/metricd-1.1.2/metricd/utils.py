import argparse
import socket

from .collector import SystemCollector
from .metricd import MetricD
from .reporter import ConsoleReporter, HttpReporter


def factory(args):
    collector = SystemCollector(args.interval, args.hostname)
    reporter = None

    if args.reporter == 'console':
        reporter = ConsoleReporter()
    elif args.reporter == 'http':
        if args.headers:
            headers = dict(args.headers)
        else:
            headers = {}

        reporter = HttpReporter(args.hostname, args.url, headers)
    else:
        raise RuntimeError('You need to define a reporter')

    return MetricD(collector, reporter, args.interval)


def parse_arguments(args=None):
    try:
        socket_hostname = socket.gethostname()
    except socket.error:
        socket_hostname = None

    parser = argparse.ArgumentParser(
            description='Starts MetricD agent'
    )

    main_parser = argparse.ArgumentParser(add_help=False)
    main_parser.add_argument(
            '--hostname',
            help='Overrides hostname prefix for reporters',
            default=socket_hostname
    )

    main_parser.add_argument(
            '--interval',
            help='Interval for collecting metrics as second',
            default=10
    )

    subparsers = parser.add_subparsers(dest='reporter')

    console_parser = subparsers.add_parser('console', parents=[main_parser])

    http_parser = subparsers.add_parser('http', parents=[main_parser])
    http_parser.add_argument(
            '--url',
            help='Url for sending metrics as JSON',
            required=True
    )

    #  --headers x-access-token=bar --headers foo=bar
    http_parser.add_argument(
            '--headers',
            help='Extra headers',
            action='append',
            type=lambda kv: kv.split("=")
    )

    return parser.parse_args(args)
