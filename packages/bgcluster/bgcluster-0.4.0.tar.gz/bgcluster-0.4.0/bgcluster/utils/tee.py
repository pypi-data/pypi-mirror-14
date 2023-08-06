import argparse
import logging
import requests
import sys


def cmdline():

    # Configure the logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)

    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Mandatory
    parser.add_argument('-u', '--url', dest='tee_url', default="http://localhost:8080/", help='Url where do you want to send the STDIN lines')
    parser.add_argument('-p', '--prefix', dest='prefix', default="", help='Add a prefix at all lines')
    args = parser.parse_args()
    logging.debug(args)

    for line in sys.stdin:
        requests.get("{}{}{}".format(args.tee_url, args.prefix, line))
        print(line, end="")

if __name__ == '__main__':
    cmdline()
