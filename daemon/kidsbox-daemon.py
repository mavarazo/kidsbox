#!/usr/bin/env python
# -*- coding: utf8 -*-


import logging
import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


# Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# API
BASE_URL = 'http://localhost/tags/api/'


def tag_with_uid_registered(uid):
    url = BASE_URL + uid
    r = r = requests.get(url)
    logging.info(r.url + " - " + r.text)
    if r.status_code == 200:
        return True
    return False


def create_tag(uid):
    url = BASE_URL
    payload = "{\"uid\": \"" + uid + "\"}"
    headers = {'content-type': 'application/json'}
    r = requests.request("POST", url, data=payload, headers=headers)
    logging.info(r.url + " - " + r.text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False


def play_by_uid(uid):
    url = BASE_URL + 'play/' + uid
    r = requests.get(url)
    logging.info(r.url + " - " + r.text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False


reader = SimpleMFRC522()

try:
    logging.info(f"kidsbox-daemon startup")
    while True:
        id, text = reader.read()
        logging.info(f"Card read {id}, {text}")

        try:
            if tag_with_uid_registered(id):
                play_by_uid(id)
                time.sleep(10)
            else:
                create_tag(id)
                time.sleep(10)
        except Exception as e:
            logging.error(e)
finally:
    logging.info(f"kidsbox-daemon shutdown")
    GPIO.cleanup()
