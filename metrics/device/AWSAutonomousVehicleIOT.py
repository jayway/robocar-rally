#!/usr/bin/python

import time
from time import sleep
import json
import random
import uuid
import datetime
import paho.mqtt.client as paho
import ssl
import rightfrontwheel
import leftfrontwheel

# Fill out this area with AWS account specific details
AWS_REST_ENDPOINT = ""
AWS_PORT = 8883
THING = ""
TOPIC = '/topics/DonkeyCars/{}'.format(THING)

# Location of Certificates
CA_PATH = ""
CERT_PATH = ""
KEY_PATH = ""

connflag = False


def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(TOPIC+" "+str(msg.payload))


def getTime():
    currenttime = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", currenttime)


def drivetelemetry():
    vehicleid = THING
    actualtime = getTime()
    unixtime = str(datetime.datetime.now())
    event = uuid.uuid4()
    eventid = event.hex
    dynamodb_ttl = int(time.time()) + 2592000
    wheel_travel = 9.5
    feet = 12
    wheel_rotations_per_mile = 63360
    speed_reset = random.randint(1, 9)
    battery_capacity = 5320

    right_front_wheel_rpm = int(rightfrontwheel.get_wheelrpm())
    right_front_wheel_odometer = round((rightfrontwheel.get_wheeldistance())/feet, 2)
    right_front_wheel_distance = right_front_wheel_rpm * wheel_travel
    right_front_wheel_mpm = right_front_wheel_distance / wheel_rotations_per_mile
    right_front_wheel_mph = right_front_wheel_mpm * 60
    right_front_wheel_speed = round(right_front_wheel_mph)
    right_front_wheel_data = {"right_front_speed": right_front_wheel_speed, "right_front_rpm": right_front_wheel_rpm, "right_front_wheel_odometer": right_front_wheel_odometer}

    left_front_wheel_rpm = int(leftfrontwheel.get_wheelrpm())
    left_front_wheel_odometer = round((leftfrontwheel.get_wheeldistance())/feet, 2)
    left_front_wheel_distance = left_front_wheel_rpm * wheel_travel
    left_front_wheel_mpm = left_front_wheel_distance / wheel_rotations_per_mile
    left_front_wheel_mph = left_front_wheel_mpm * 60
    left_front_wheel_speed = round(left_front_wheel_mph)
    left_front_wheel_data = {"left_front_speed": left_front_wheel_speed, "left_front_rpm": left_front_wheel_rpm, "left_front_wheel_odometer": left_front_wheel_odometer}

    vehicle_speed = int((right_front_wheel_speed + left_front_wheel_speed)/2)
    average_wheel_rpm = int((right_front_wheel_rpm + left_front_wheel_rpm)/2)
    vehicle_odometer = ((right_front_wheel_odometer + left_front_wheel_odometer)/2)
    remaining_power = int(battery_capacity - vehicle_odometer)
    engine_rpm = int(average_wheel_rpm * 11)

    # JSON Key/Value pairs of telemetry
    vehiclepayload = json.dumps(
        {
            "vehicleid": vehicleid,
            "eventid": eventid,
            "time": actualtime,
            "timestamp": unixtime,
            "average_wheel_rpm": average_wheel_rpm,
            "engine_rpm": engine_rpm,
            "vehicle_speed": vehicle_speed,
            "vehicle_odometer": vehicle_odometer,
            "remaining_power": remaining_power,
            "right_front_wheel_rpm": right_front_wheel_rpm,
            "left_front_wheel_rpm": left_front_wheel_rpm,
            "right_front_wheel_speed": right_front_wheel_speed,
            "left_front_wheel_speed": left_front_wheel_speed,
            "right_front_wheel_odometer": right_front_wheel_odometer,
            "left_front_wheel_odometer": left_front_wheel_odometer,
            "dynamodb_ttl": dynamodb_ttl
        }
    )

    print(vehiclepayload)
    return vehiclepayload

# Logging can be enabled by uncommenting below
def on_log(client, userdata, level, buf):
    print("{}".format(buf))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_log = on_log

mqttc.tls_set(CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(AWS_REST_ENDPOINT, AWS_PORT, keepalive=60)

# Begin reading sensor telemetry
mqttc.loop_start()

# drivetelemetry()
for r in range(10000000):
    # Sending telemetry to AWS IoT Service
    vehicle_topic = TOPIC
    telemetry_payload = drivetelemetry()
    print(telemetry_payload)
    mqttc.publish(vehicle_topic, telemetry_payload, 1)
    sleep(1)
