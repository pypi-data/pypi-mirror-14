from tinycm.executer import execute
from tinycm.parser import CMParser
from tinycm.graph import CMGraph
from socket import getfqdn
import urllib.parse
import os
import logging
import argparse

from tinycm.reporting import verify, get_verify_report


def main():
    parser = argparse.ArgumentParser(description="Tiny Configuration Manager")
    parser.add_argument('--apply', action='store_true', help="Apply configuration instead of verify")
    parser.add_argument('--hostname', help="Override hostname", default=getfqdn())
    parser.add_argument('--modulepath', help="Override the module path")
    parser.add_argument('--verbose', action='store_true', help="Show verbose messages")
    parser.add_argument('--debug', action='store_true', help="Show very verbose messages")
    parser.add_argument('configuration', help=".cm.yml file to verify or apply")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if not args.modulepath:
        if args.configuration.startswith('http://') or args.configuration.startswith('https://'):
            parts = urllib.parse.urlparse(args.configuration)
            path = os.path.dirname(parts.path)
            parts.path = path
            args.modulepath = urllib.parse.urlunparse(parts)
        else:
            args.modulepath = os.path.dirname(args.configuration)

    logging.info('Starting TinyCM run')
    logging.info('Configuration: {}'.format(args.configuration))
    logging.info('Module path  : {}'.format(args.modulepath))
    logging.info('Hostname     : {}'.format(args.hostname))

    logging.debug('Starting parse stage')
    configuration = CMParser(args.configuration, args.hostname, module_path=args.modulepath)
    logging.debug('Starting lint stage')
    for definition in configuration.definitions:
        configuration.definitions[definition].lint()
    logging.debug('Starting graph stage')
    graph = CMGraph(configuration)
    logging.debug('Starting sort stage')
    tasks = graph.get_sorted_jobs()

    if args.apply:
        result = execute(tasks)
    else:
        result = verify(tasks)
        print(get_verify_report(result))


if __name__ == '__main__':
    main()
