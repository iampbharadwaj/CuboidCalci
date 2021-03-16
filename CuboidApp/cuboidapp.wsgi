#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/CuboidApp/")

from CuboidApp import app as application
application.secret_key = 'T3stI0n0s'
