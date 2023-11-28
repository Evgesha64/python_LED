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
start_time1 = time.time()
f1 = 0
string3 = ""
s = 1
t = 1
l = 1
ks = 1

while True:
    select = input("Выберите действие \n 1 - Настройка генератора тактов.\n 2 - Настройка записи.\n 3 - Запуск генератора тактов.\n 4 - Запись настроек.\n")




    match select:
        case "1":
            print("Настройка генератора тактов")
            s = int(input("Введите количество циклов:"))
            t = int(input("Введите количество тактов:"))
            print(s, "\n", t)
        case "2":
            print("Настройка записи цветов")
            s1 = int(input("Введите количество линий:"))
            t = int(input("Введите количество светодиодов:"))
            print(s1, "\n", l)
        case "3":
            for k in range(s):
                cklnumber = 0
                msg = str("dfjhd")

                # print("Цикл пройден:",cklnumber)
                while cklnumber < t:

                    client.loop()

                    if msg_out != '---':

                        client.publish(mqtt_topic1, cklnumber)
                        cklnumber += 1
                        msg_out = '---'
                        #print(cklnumber)
                    elif msg_out == '---':
                        start_time = time.time()


                        if time.time() - start_time > 5:
                            print('timeout')
                            print('Нет ответа от ESP!!!')
                print(time.time() - start_time1)
                print("fps-", s * t / (time.time() - start_time1))
        case "4":
            for k1 in range(l):

                string = "#{}#".format(k1)
                string3 = string3 + string
                for k2 in range(ks):
                    if f1 == 0:
                        string2 = "{},{},{},{},".format(k2, 255, 0, 0)
                        string3 = string3 + string2
                    elif f1 == 1:
                        string2 = "{},{},{},{},".format(k2, 0, 255, 0)
                        string3 = string3 + string2
                    elif f1 == 2:
                        string2 = "{},{},{},{},".format(k2, 0, 0, 255)
                        string3 = string3 + string2
            client.publish(mqtt_topic2, string3)













