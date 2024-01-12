import pyautogui
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:

    currentMouseX1, currentMouseY = pyautogui.position()
    numY = int(arduino_map(currentMouseY, 0, 1439, 15, 0))
    numX = int(arduino_map(currentMouseX1, 0, 2559, 0, 39))
    array = [[0] * 16 for _ in range(39)]

    if numY % 2 == 1:
        numX = 39 - numX + 1
    num = numX + 39 * numY
    print(numY, " ", numX, " ", num)