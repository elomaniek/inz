from flask import *
import subprocess
import os
import socket
import signal
import hashlib
from flask_cors import CORS
from flask import Flask, request,jsonify
import requests
from contextlib import closing
import sys
from sys import exit
import time




response = requests.post("http://127.0.0.1:8080/connected", json={"stream": {"ip": "123.123.123.123"}})

