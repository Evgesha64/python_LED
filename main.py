import time

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import asyncio

# Настройки подключения MQTT
mqtt_broker = "192.168.0.103"
mqtt_port = 1883
mqtt_topic1 = "topic_ckl"
mqtt_topic2 ="topic_num_RGB"
mqtt_topic3 = "topicCallback"

msg_out = '--'
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Нет подключения " + str(rc))


client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic3)


def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())
print("Сообщение получено ",msg_out)

client.on_message = on_message
client.on_connect = on_connect

s: int = int(input("Введите количество циклов:"))
t: int = int(input("Введите количество тактов:"))


print(s)
print(t)
start_time1 = time.time()
f1 = 0
for k in range(s):
    cklnumber = 0
    msg = str("dfjhd")

    f1 += 1


    #print("Цикл пройден:",cklnumber)
    while cklnumber < t:

        client.loop()

        if msg_out != '---':

            client.publish(mqtt_topic1, cklnumber)
            cklnumber += 1
            msg_out = '---'
            print(cklnumber)
        elif msg_out == '---':
            start_time = time.time()
            if time.time() - start_time > 5:
                print('timeout')
    string3 = ""
    for k1 in range(t):

        string = "#{}#".format(k1)
        string3 = string3 + string
        for k2 in range(59):
            if f1 == 0:
                string2 = "{},{},{},{},".format(k2, 255, 0, 0)
                string3 = string3 + string2
            elif f1 == 1:
                string2 = "{},{},{},{},".format(k2, 0, 255, 0)
                string3 = string3 + string2
            elif f1 == 2:
                string2 = "{},{},{},{},".format(k2, 0, 0, 255)
                string3 = string3 + string2
                f1 = 0
        if f1 == 2:
           f1 = 0
    client.publish(mqtt_topic2, string3)









print(time.time() - start_time1)
print("fps-", s * t / (time.time() - start_time1))
