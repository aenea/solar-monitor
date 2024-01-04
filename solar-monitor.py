#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import os
import renogymodbus
import socket
import ssl
import time
from renogymodbus import RenogyChargeController

BATTERY_VOLTAGE_UID = 'hive_solar_battery_voltage'
LOAD_POWER_UID = 'hive_solar_load_power'
SOLAR_POWER_UID = 'hive_solar_solar_power'
TOPIC_PREFIX = 'homeassistant/sensor/'


# create a connection callback function
def on_connect(client, userdata, flags, result, properties=None):
    if (result == 0):
        # create a config entry for the hive solar battery voltage
        config = {}
        config['unique_id'] = BATTERY_VOLTAGE_UID
        config['device_class'] = 'voltage'
        config['icon'] = 'mdi:lightning-bolt-circle'
        config['name'] = BATTERY_VOLTAGE_UID
        config['state_class'] = 'measurement'
        config['state_topic'] = TOPIC_PREFIX + BATTERY_VOLTAGE_UID + '/state'
        config['suggested_display_precision'] = 1
        config['unit_of_measurement'] = 'Vh'

        client.publish(TOPIC_PREFIX + BATTERY_VOLTAGE_UID + '/config', json.dumps(config), retain=True, properties=None)

        # create a config entry for hive solar load
        config['unique_id'] = LOAD_POWER_UID
        config['device_class'] = 'power'
        config['icon'] = 'mdi:meter-electric-outline'
        config['name'] = LOAD_POWER_UID
        config['state_topic'] = TOPIC_PREFIX + LOAD_POWER_UID + '/state'
        config['suggested_display_precision'] = 0
        config['unit_of_measurement'] = 'Wh'

        client.publish(TOPIC_PREFIX + LOAD_POWER_UID + '/config', json.dumps(config), retain=True, properties=None)

        # create a config entry for solar production
        config['unique_id'] = SOLAR_POWER_UID
        config['device_class'] = 'power'
        config['icon'] = 'mdi:solar-power'
        config['name'] = SOLAR_POWER_UID
        config['state_topic'] = TOPIC_PREFIX + SOLAR_POWER_UID + '/state'
        config['suggested_display_precision'] = 0
        config['unit_of_measurement'] = 'Wh'

        client.publish(TOPIC_PREFIX + SOLAR_POWER_UID + '/config', json.dumps(config), retain=True, properties=None)


# script variabled
loop_timer = os.getenv("LOOP_TIMER", default=30)
mqtt_broker = os.getenv("MQTT_BROKER", default='mqtt')
mqtt_port = os.getenv("MQTT_PORT", default=1883)
mqtt_ssl = os.getenv("MQTT_SSL", default='no')

# create a mqtt client
client = mqtt.Client(client_id=socket.getfqdn(), transport='tcp', protocol=mqtt.MQTTv5)
client.on_connect = on_connect

if mqtt_ssl.lower() == 'yes':
    client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)

client.connect(mqtt_broker, int(mqtt_port), properties=None)
client.loop_start()

controller = RenogyChargeController("/dev/ttyUSB0", 1)

while True:
    try:
        # read the current controller state
        battery_voltage = controller.get_battery_voltage()
        load_power = controller.get_load_power()
        solar_power = controller.get_solar_power()

        # publish the data to the mqtt server
        client.publish(TOPIC_PREFIX + BATTERY_VOLTAGE_UID + '/state', battery_voltage)
        client.publish(TOPIC_PREFIX + LOAD_POWER_UID + '/state', load_power)
        client.publish(TOPIC_PREFIX + SOLAR_POWER_UID+ '/state', solar_power)

        time.sleep(int(loop_timer))
    except:
        client.loop_stop()
        client.disconnect()
        break
