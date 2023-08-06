import argparse
import logging
import requests


def cmdline():

    # Configure the logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)

    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Mandatory
    parser.add_argument('-u', '--url', dest='ping_url', default="http://localhost:8080/", help='Url where that do you want to ping')
    args = parser.parse_args()
    logging.debug(args)

    requests.get("{}".format(args.ping_url))

if __name__ == '__main__':
    cmdline()
