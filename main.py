import time
import pyautogui
import paho.mqtt.client as mqtt
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


def on_connect(client, userdata, flags, rc):
    print("Нет подключения " + str(rc))


client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic3)


def on_message(client, userdata, msg):
    global msg_out
    msg_out = str(msg.payload.decode())
   # print("Сообщение получено ", msg_out)
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min




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
listener = mouse.Listener(on_scroll=on_scroll)
thread = threading.Thread(target=listener.start)
thread.start()
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

                client.loop()
                currentMouseX1, currentMouseY = pyautogui.position()  # Получаем XY координаты курсора.
                if currentMouseX1 < 0:
                    currentMouseX1 = currentMouseX1 * (-1)
                #print(currentMouseX1)
                num = int(arduino_map(currentMouseX1, 0, 2560, 59, 0))


                if msg_out != '---':
                    currentMouseX = int(arduino_map(scroll_value, 0, 40, 0, 2559))

                    if currentMouseX < 853:
                        color1 = int(arduino_map(currentMouseX, 0, 853, 255, 0))

                    if currentMouseX > 1703:
                        color2 = int(arduino_map(currentMouseX, 1703, 2559, 255, 0))

                    # if 753 < currentMouseX < 1279:
                    #     color3 = int(arduino_map(currentMouseX, 653, 1279, 0, 255))

                    if 753 < currentMouseX < 1803:
                        color3 = int(arduino_map( currentMouseX, 753, 1903, 255, 0))

                    for i in range(3):
                        string2 = "{},{},{},{},".format(num + i, color1, color3, color2)
                        string3 = string3 + string2

                    # if currentMouseX < 853:
                    #     string2 = "{},{},{},{},".format(num, 255, 0, 0)
                    #     string3 = string3 + string2
                    #
                    # elif 853 < currentMouseX < 1706:
                    #     string2 = "{},{},{},{},".format(num, 0, 255, 0)
                    #     string3 = string3 + string2
                    #
                    # elif 1706 < currentMouseX < 2559:
                    #     string2 = "{},{},{},{},".format(num, 0, 0, 255)
                    #     string3 = string3 + string2




                    client.publish(mqtt_topic2, string3)
                    string3 = ""
                    client.publish(mqtt_topic1, "1")

                    if num == 59:
                        num = 0
                    if caseFlag == 0:
                        msg_out = '---'

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


