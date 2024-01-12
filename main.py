import time
import pyautogui
import paho.mqtt.client as mqtt
import colorsys
import random
from PIL import Image
#import keyboard
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


#def on_connect(client, userdata, flags, rc):
#    print("Нет подключения " + str(rc))


client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic3)


def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())
   # print("Сообщение получено ", msg_out)
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min




client.on_message = on_message
#client.on_connect = on_connect
screenWidth, screenHeight = pyautogui.size()  # Получаем размер экрана.
# Создаем список значений от 0 до 2500

f1 = 0
f2 = 0
caseFlag = 0
string3 = ""
stringN = "Запуск генератора тактов с обратной связью."
stringN2 = "Выключить обратную связь."
s = 9999
t = 1
l = 1
ks = 1
num = 0
color1 = 0
color2 = 0
color3 = 0
cklnumber = 0
string2 = ""
scroll_value = 0
# listener = mouse.Listener(on_scroll=on_scroll)
# thread = threading.Thread(target=listener.start)
# thread.start()
while True:
    select = input("Выберите действие \n 1 - Настройка генератора тактов.\n 2 - Настройка записи. + \n 3 - " + stringN + "\n 4 - " + stringN2 + "\n")

    match select:
        case "1":
            print("Настройка генератора тактов")
            s = int(input("Введите количество циклов:"))

            print(s)
        case "2":
            print("Настройка записи цветов")

        case "3":
            start_time1 = time.time()
            shet = 0
            shet1 = 0
            red = 0
            green = 0
            blue = 0
            kol_led = 1
            kol_led1 = 1
            status_time = 0
            invert = 0
            for k in range(s):

                client.loop()
               #  currentMouseX1, currentMouseY = pyautogui.position()  # Получаем XY координаты курсора.
               #  if currentMouseX1 < 0:
               #      currentMouseX1 = currentMouseX1 * (-1)
               #  #print(currentMouseX1)
               #  numY = int(arduino_map(currentMouseY, 0, 1439, 15, 0))
               #  numX = int(arduino_map(currentMouseX1, 0, 2559, 0, 39))
               #

               #  if numY % 2 == 1:
               #      numX = 39 - numX+1
               #  num = numX + 39 * numY
               # # print(numY, " ", numX, " ", num)
               #  num -= 3
               #  if num > 312:
               #      num -= 1
               #  if num > 600:
               #      num = 600
                if msg_out != '---':
###########################################
                    image = Image.open("imageTM.png")
                    # Изменение размера картинки до 39x15
                    image = image.resize((39, 15))
                    # Получение данных о пикселях картинки
                    pixels = image.load()
                    # Создание массива для хранения цветов пикселей
                    pixel_array = []

                    # Проход по каждому пикселю и сохранение его цвета в массиве
                    for y in range(15):
                        for x in range(39):
                            pixel = pixels[x, y]

                            # Извлечение отдельных компонентов цвета (R, G, B)
                            r, g, b = pixel[:3]
###############################################
                            if y % 2 == 1:
                                x = 39 - x+1
                            num = x + 39 * y

                            num -= 3
                            if num > 312:
                                num -= 1
                            if num > 600:
                                num = 600

                            string2 = "{},{},{},{},".format(num, r, g, b)
                            string3 = string3 + string2

                    client.publish(mqtt_topic2, string3)
                    string3 = ""
                    #client.publish(mqtt_topic1, "1")

                    if num == 600:
                        num = 0
                    if caseFlag == 0:
                        msg_out = '---'
                    start_time = time.time()
                elif msg_out == '---':



                    if time.time() - start_time > 5:
                        print('Повторная отправка')
                        msg_out = '1'
                    elif time.time() - start_time > 2:
                        print('Нет ответа от ESP!!!')
                    status_time = status_time + (time.time() - start_time)

            print(time.time() - start_time1)
            print(status_time)
            print("fps-", s / (time.time() - start_time1+status_time))
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

