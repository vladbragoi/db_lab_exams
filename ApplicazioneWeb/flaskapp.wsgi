#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/python/Insegnamenti")

from Insegnamenti import app as application
application.secret_key = 'poseSecret'
