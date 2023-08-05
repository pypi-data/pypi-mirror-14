#!/usr/bin/env python3
from eagle.application import app
import sys

import argparse

def main():
    parser = argparse.ArgumentParser();
    parser.add_argument('--port', '-p', default=8000, type=int, help="port (default: 8000)")
    parser.add_argument('--public', default=False, action='store_true', help="listen for external connections")
    parser.add_argument('--nodebug', dest='debug', default=True, action='store_false', help="disable debug messages")
    parser.add_argument('--config', '-c', required=True, help="config file to use.")
    args = parser.parse_args()

    if args.public:
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'

    app.secret_key = 'T0Jw9sidVJi0vybbuCNN'
    app.run(config=args.config, host=host, port=args.port, debug=args.debug, use_reloader=True)

if __name__ == "__main__":
    main()
