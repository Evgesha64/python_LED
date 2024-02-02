import paho.mqtt.client as mqtt
import struct
import time
import random
# Создаем клиента MQTT
client = mqtt.Client()

# Подключаемся к брокеру MQTT
client.connect("192.168.1.3", 1883, 60)  # Замените "localhost" на адрес вашего MQTT брокера

# Создаем массив данных uint32_t
data = []
r = 0
g = 0
b = 0
rgb = 0
f = 0
s = 1
regim = 0
while 1:
    select = input()
    if select == "r":
        r = 255
    if select == "g":
        g = 255
    if select == "b":
        b = 255
    if select == "c":
        b = 0
        g = 0
        r = 0
    if select == "e":
        break

    if select == "":
        while 1:
            for k in range(600):
                # if k == rgb:
                if regim == 0:
                    data.append((255 << 16) | (0 << 8) | 0)
                elif regim == 1:
                    data.append((0 << 16) | (255 << 8) | 0)
                elif regim == 2:
                    data.append((0 << 16) | (0 << 8) | 255)

                else:
                    data.append((0 << 16) | (0 << 8) | 0)
            time.sleep(s)
            if f == 0:
                rgb += 1
            elif f == 1:
                rgb -= 1

            if rgb == 600:
                rgb = 600
                f = 1
                s = 1
                regim += 1
            elif rgb == 0:
                rgb = 0
                f = 0
                s = 1
                regim += 1

            if s < 0.01:
                s = 0
            s /= 1.04
            if regim == 3:
                regim = 0
            # Преобразуем данные в байты
            payload = struct.pack('I' * len(data), *data)
            print(s)

            client.publish("topic_num_RGB", payload)
            data = []
            select = "kgfkgfkgf"

# Отключаемся от брокера
client.disconnect()
