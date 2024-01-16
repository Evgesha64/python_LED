import time
import pyautogui
import paho.mqtt.client as mqtt
import io
from PIL import Image
import colorsys
import random
# import keyboard
from pynput import mouse
import threading

# Настройки подключения MQTT
mqtt_broker = "192.168.0.103"
mqtt_port = 1883
mqtt_topic1 = "topic_ckl"
mqtt_topic2 = "topic_num_RGB"
mqtt_topic3 = "topicCallback"

msg_out = '--'
client = mqtt.Client()


def on_scroll(x, y, dx, dy):
    global scroll_value

    scroll_value += dy
    if scroll_value < 0:
        scroll_value = 40
    if scroll_value == 41:
        scroll_value = 0


# def on_connect(client, userdata, flags, rc):
#    print("Нет подключения " + str(rc))


client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic3)


def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())


# print("Сообщение получено ", msg_out)
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def imageNumPixelRGB(x,y,pixel):



    if y % 2 == 1:
        x = 39 - x + 1
    LEDnum = x + 39 * y
    LEDnum -= 3
    if LEDnum > 312:
        LEDnum -= 1
    if LEDnum > 600:
        LEDnum = 600

    r, g, b = pixel[:3]
    return LEDnum, r, g, b


client.on_message = on_message
# client.on_connect = on_connect
screenWidth, screenHeight = pyautogui.size()  # Получаем размер экрана.
# Создаем список значений от 0 до 2500


caseFlag = 0
string3 = ""
stringN = "Запуск генератора тактов с обратной связью."
stringN2 = "Выключить обратную связь."
s = 9999
num = 0
string2 = ""

while True:
    select = input(
        "Выберите действие \n 1 - Настройка генератора тактов.\n 2 - Настройка записи. + \n 3 - " + stringN + "\n 4 - " + stringN2 + "\n")

    match select:
        case "1":
            print("Настройка генератора тактов")
            s = int(input("Введите количество циклов:"))

            print(s)
        case "2":
            print("Настройка записи цветов")

        case "3":
            start_time1 = time.time()
            status_time = 0

            image = Image.open("imageTM2.png")
            (width, height) = image.size
            xpix = 38
            # Получение данных о пикселях картинки
            pixels = image.load()
            for k in range(s):

                client.loop()
                #  currentMouseX1, currentMouseY = pyautogui.position()  # Получаем XY координаты курсора.
                #  if currentMouseX1 < 0:
                #      currentMouseX1 = currentMouseX1 * (-1)
                #  #print(currentMouseX1)
                #  numY = int(arduino_map(currentMouseY, 0, 1439, 15, 0))
                #  numX = int(arduino_map(currentMouseX1, 0, 2559, 0, 39))

                if msg_out != '---':
                    for y in range(15):
                        for x in range(39):
                            ypix = 14 - y
                            pixel = pixels[x - xpix, ypix]
                            num, r, g, b = imageNumPixelRGB(x, y,pixel)
                            if r == 0 and g == 0 and b == 0:
                                continue
                            string2 = "{},{},{},{},".format(num, r, g, b)
                            string3 = string3 + string2

                    client.publish(mqtt_topic2, string3)
                    string3 = ""
                    xpix -= 1
                    if xpix == 0:
                        xpix = width-2
                    # client.publish(mqtt_topic1, "1")

                    if caseFlag == 0:  # Выключение обратной связи
                        msg_out = '---'
                    start_time = time.time()
                elif msg_out == '---':  # Если ждём ответа от ESP

                    if time.time() - start_time > 5:
                        print('Повторная отправка')
                        msg_out = '1'
                    elif time.time() - start_time > 2:
                        print('Нет ответа от ESP!!!')
                    status_time = status_time + (time.time() - start_time)

            print(time.time() - start_time1)
            print(status_time)
            print("fps-", s / (time.time() - start_time1 + status_time))
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
        # case "5":
        #     if caseFlag == 0:
        #         stringN = "Запуск генератора тактов без обратной связью."
        #         stringN2 = "Включить обратную связь."
        #         print("Обратная связь выключена")
        #         caseFlag = 1
        #     else:
        #         stringN = "Запуск генератора тактов с обратной связью."
        #         stringN2 = "Выключить обратную связь."
        #         print("Обратная связь включена")
        #         caseFlag = 0
        #     print(caseFlag)
