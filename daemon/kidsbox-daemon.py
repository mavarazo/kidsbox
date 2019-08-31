#!/usr/bin/env python
# -*- coding: utf8 -*-


import RPi.GPIO as GPIO
import logging
import requests
import signal
import time

import MFRC522

# Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# API
BASE_URL = 'http://localhost:8001/tags/api/'


def tag_with_uid_registered(uid):
    url = BASE_URL + uid
    r = None
    while r is None:
       try:
          r = requests.get(url)
          break
       except:
          time.sleep(10)
          continue

    logging.info(r.text)
    if r.status_code == 200:
        return True
    return False


def create_tag(uid):
    url = BASE_URL
    payload = "{\"uid\": \"" + uid + "\"}"
    headers = {'content-type': 'application/json'}
    r = requests.request("POST", url, data=payload, headers=headers)
    logging.info(r.text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False


def play_by_uid(uid):
    url = BASE_URL + '/play/' + uid
    r = requests.get(url)
    logging.info(r.text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        logging.info("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        uid_str = values = ':'.join(str(v) for v in uid)

        # Print UID
        logging.info("Card read UID: " + uid_str)

        try:
            if tag_with_uid_registered(uid_str):
                play_by_uid(uid_str)
                time.sleep(10)
            else:
                create_tag(uid_str)
                time.sleep(10)
        except Exception as e:
            logging.error(e)