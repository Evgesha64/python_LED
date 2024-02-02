from PIL import Image
import paho.mqtt.client as mqtt
import struct
import time
import threading

mqtt_topic3 = "topicCallback"
rgb = 0
f = 1
msg_out = '--'
regim = 0

client = mqtt.Client()
# Подключаемся к брокеру MQTT
client.connect("192.168.1.3", 1883, 60)  # Замените "localhost" на адрес вашего MQTT брокера

client.subscribe(mqtt_topic3)

def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())


client.on_message = on_message

def imageNumPixelRGB(LEDnum, pixels, sdvig):
    if LEDnum > 600:
        LEDnum = 600
    if LEDnum > 312:
        LEDnum += 1
    LEDnum += 2

    y = LEDnum // 39
    x = LEDnum % 39
    if y % 2 == 1:
        x = 38 - x
    if y == 15:
        y = 14
    x1 = x + sdvig
    # print(y, " ", x)
    if x1 > 135:
        x1 -= 135
    # print(x1)
    y = 14 - y

    pixel = pixels[x1, y]
    r, g, b = pixel[:3]
    return r, g, b


def fun_start():
    global f
    global msg_out
    image = Image.open("imageTM2.png")
    (width, height) = image.size
    data = []
    # Получение данных о пикселях картинки
    pixels = image.load()
    sdvig = 0
    regim = 0

    while True:

        if msg_out != 'stop':
            for y in range(600):
                r, g, b = imageNumPixelRGB(y, pixels, sdvig)
                if r > 50:
                    r = 50
                if g > 50:
                    g = 50
                if b > 50:
                    b = 50
                data.append((g << 16) | (r << 8) | b)
            payload = struct.pack('I' * len(data), *data)

            data = []
            sdvig += 1
            if sdvig == 135:
                sdvig = 0
            # time.sleep(0.02)
            for i in range(60):
                if regim == i:
                    data.append((0 << 16) | (255 << 8) | 0)
                else:
                    data.append((0 << 16) | (0 << 8) | 0)
            regim += 1
            if regim == 61:
                regim = 0
            payload2 = struct.pack('I' * len(data), *data)

            client.publish("topic_num_RGB", payload)
            client.publish("topic_num_RGB2", payload2)
            data = []
            msg_out = 'stop'
            while msg_out == 'stop':
                client.loop()

        if f == 0:
            break


def fun_stop():
    global f
    global msg_out
    input("Нажми любую клавишу для завиршения цикла отправки.")
    f = 0
    msg_out = '--'


caseFlag = 0
stringN = "Запуск генератора тактов с обратной связью."
stringN2 = "Выключить обратную связь."
num = 0

############################################################################################################
while True:
    f = 1
    select = input(
        "Выберите действие \n 1 - Настройка генератора тактов.\n 2 - Выключить. \n 3 - " + stringN + "\n 4 - " + stringN2 + "\n")

    match select:
        case "1":
            print("Настройка генератора тактов")
            s = int(input("Введите количество циклов:"))

            print(s)

        case "2":
            print("Выключить")
            client.publish("topic_stop", "1")

        case "3":

            t1 = threading.Thread(target=fun_start)
            t2 = threading.Thread(target=fun_stop)

            t1.start()  # начать выполнение func1 в отдельном потоке
            t2.start()  # начать выполнение func2 в отдельном потоке

            t1.join()  # ожидать завершения func1
            t2.join()  # ожидать завершения func2

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
