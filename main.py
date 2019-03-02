import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import sys

# Broker parameters
broker = "iot.eclipse.org"
brokerPort = 1883
keepAliveBroker = 60
topic = "whitestonedev/v1/smart-socket"

# Raspberry parameters
gpio_relay = 7
gpio.setmode(gpio.BOARD)
gpio.setup(gpio_relay, gpio.OUT)

# Callback - connection broker
def on_connect(client, userdata, flags, rc):
  print "[STATUS] Conected to broker. Status: " + str(rc)
  client.subscribe(topic)

# Callback - receive message
def on_message(client, userdata, msg):
  payload_message = str(msg.payload)
  print "[Message] Topic: " + msg.topic + " Message: " + payload_message
  if payload_message == "on":
    print "on"
    gpio.output(gpio_relay, gpio.HIGH)
  else:
    print "off"
    gpio.output(gpio_relay, gpio.LOW)

# Callback - publish message
def on_publish(mqttc, obj, mid):
  print("Publish (mid): " + str(mid))

# Clallback - subscribe topic
def on_subscribe(mqttc, obj, mid, granted_qos):
  print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Main
try:
  print("[STATUS] Initializing MQTT...")
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.on_publish = on_publish
  client.on_subscribe = on_subscribe

  client.connect(broker, brokerPort, keepAliveBroker)
  client.publish(topic, "I'm connected")
  client.loop_forever()
except KeyboardInterrupt:
  print "Ctrl+C pressed, over program..."
  gpio.cleanup()
  sys.exit(0)