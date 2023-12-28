import time
import pyautogui
import paho.mqtt.client as mqtt
import numpy as np
from paho.mqtt.client import Client
import asyncio

# Настройки подключения MQTT
mqtt_broker = "192.168.0.103"
mqtt_port = 1883
mqtt_topic1 = "topic_ckl"
mqtt_topic2 = "topic_num_RGB"
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
   # print("Сообщение получено ", msg_out)


client.on_message = on_message
client.on_connect = on_connect
screenWidth, screenHeight = pyautogui.size()  # Получаем размер экрана.
# Создаем список значений от 0 до 2500

f1 = 0
f2 = 0
caseFlag = 0
string3 = ""
stringN = "Запуск генератора тактов с обратной связью."
stringN2 = "Выключить обратную связь."
s = 1000
t = 1
l = 1
ks = 1
num = 0

cklnumber = 0
while True:
    select = input("Выберите действие \n 1 - Настройка генератора тактов.\n 2 - Настройка записи.\n 3 - " + stringN + "\n 4 - " + stringN2 + "\n")

    match select:
        case "1":
            print("Настройка генератора тактов")
            s = int(input("Введите количество циклов:"))

            print(s)
        case "2":
            print("Настройка записи цветов")

        case "3":
            start_time1 = time.time()

            for k in range(s):
                cklnumber = 0

                while cklnumber < 2:

                    client.loop()


                    currentMouseX, currentMouseY = pyautogui.position()  # Получаем XY координаты курсора.
                    num = currentMouseY * 59 / 1439


                    if msg_out != '---':

                        string3 = ""

                        if currentMouseX < 853:
                            string2 = "{},{},{},{},".format(num, 255, 0, 0)
                            string3 = string3 + string2

                        elif 853 < currentMouseX < 1706:
                            string2 = "{},{},{},{},".format(num, 0, 255, 0)
                            string3 = string3 + string2

                        elif 1706 < currentMouseX < 2559:
                            string2 = "{},{},{},{},".format(num, 0, 0, 255)
                            string3 = string3 + string2




                        client.publish(mqtt_topic2, string3)

                        client.publish(mqtt_topic1, cklnumber)

                        if num == 59:
                            num = 0
                        if caseFlag == 0:
                            msg_out = '---'

                        cklnumber += 1
                    elif msg_out == '---':

                        start_time = time.time()
                        if time.time() - start_time > 5:
                            print('timeout')
                            print('Нет ответа от ESP!!!')

            print(time.time() - start_time1)
            print("fps-", s * 2 / (time.time() - start_time1))
        case "4":
            if caseFlag == 0:
                stringN = "Запуск генератора тактов без обратной связью."
                stringN2 = "Включить обратную связь."
                print("Обратная связь выключена")
                caseFlag = 1
            else:
                stringN = "Запуск генератора тактов с обратной связью."
                stringN2 = "Выключить обратную связь."
                print("Обратная связь включена")
                caseFlag = 0
            print(caseFlag)


