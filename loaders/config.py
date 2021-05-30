#!/usr/bin/env python3
import os


DATA_PATH = os.environ['DATA_PATH']
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
INIT_BD = bool(os.environ['INIT_BD'])
