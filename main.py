import time

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import asyncio

# Настройки подключения MQTT
mqtt_broker = "192.168.0.103"
mqtt_port = 1883
mqtt_topic = "topik"
mqtt_topic2 = "topicCallback"

msg_out = '--'
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Нет подключения " + str(rc))


client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic2)


def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())


client.on_message = on_message
client.on_connect = on_connect

s: int = int(input("Введите количество циклов:"))
t: int = int(input("Введите количество тактов:"))
t -= 1
print(s)
print(t)
start_time1 = time.time()
for k in range(s):
    cklnumber = 0
    #print("Цикл пройден:",cklnumber)
    while cklnumber < t:

        client.loop()

        if msg_out != '---':

            client.publish(mqtt_topic, cklnumber)
            cklnumber += 1
            msg_out = '---'
           # print(cklnumber)
        elif msg_out == '---':
            start_time = time.time()
            if time.time() - start_time > 5:
                print('timeout')


print(time.time() - start_time1)
print("fps-", s * t / (time.time() - start_time1))
