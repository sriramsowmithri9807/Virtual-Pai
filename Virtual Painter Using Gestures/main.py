import cv2
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter.colorchooser import askcolor

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

brushThickness = 15
eraserThickness = 50
drawColor = (255, 0, 255)

eraser_img = cv2.imread(r'C:\Users\sowmi\OneDrive\Desktop\Virtual Painter Using Gestures\Eraser.png')
clear_img = cv2.imread(r'C:\Users\sowmi\OneDrive\Desktop\Virtual Painter Using Gestures\Clear all.png')
if eraser_img is None or clear_img is None:
    raise FileNotFoundError("Eraser or Clear All image not found. Check the file paths.")

eraser_img = cv2.resize(eraser_img, (100, 80))
clear_img = cv2.resize(clear_img, (100, 80))

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

xp, yp = 0, 0
undoStack = []
redoStack = []

def pushCanvasState():
    global undoStack, imgCanvas
    undoStack.append(imgCanvas.copy())
    if len(undoStack) > 10:
        undoStack.pop(0)

def undo():
    global undoStack, redoStack, imgCanvas
    if undoStack:
        redoStack.append(imgCanvas.copy())
        imgCanvas = undoStack.pop()

def redo():
    global undoStack, redoStack, imgCanvas
    if redoStack:
        undoStack.append(imgCanvas.copy())
        imgCanvas = redoStack.pop()

def openColorPicker():
    global drawColor
    color_code = askcolor(title="Choose Drawing Color")[0]
    if color_code:
        drawColor = tuple(int(c) for c in color_code)

def drawColorPalette(img, x1=None, y1=None):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    labels = ["Blue", "Green", "Red"]
    for i, color in enumerate(colors):
        x_start = 100 + i * 150
        x_end = x_start + 100
        label = labels[i]
        cv2.rectangle(img, (x_start, 10), (x_end, 90), color, cv2.FILLED)
        cv2.putText(img, label, (x_start + 10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        if x1 is not None and y1 is not None:
            if x_start < x1 < x_end and y1 < 90:
                global drawColor
                drawColor = color

    img[10:90, 550:650] = eraser_img
    img[10:90, 700:800] = clear_img
    cv2.putText(img, "Eraser", (550, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.putText(img, "Clear", (700, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    cv2.rectangle(img, (850, 10), (950, 90), (200, 200, 200), cv2.FILLED)
    cv2.putText(img, "Pick Color", (860, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    if x1 is not None and y1 is not None:
        if 550 < x1 < 650 and y1 < 90:
            drawColor = (0, 0, 0)
        elif 700 < x1 < 800 and y1 < 90:
            imgCanvas[:] = 0
        elif 850 < x1 < 950 and y1 < 90:
            openColorPicker()

def findHandLandmarks(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    return lmList

fps = 0
prev_time = 0

def displayUI(img):
    global fps, prev_time
    current_time = cv2.getTickCount()
    fps = int(cv2.getTickFrequency() / (current_time - prev_time))
    prev_time = current_time

    cv2.putText(img, f"FPS: {fps}", (10, 690), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    tool_text = f"Tool: {'Eraser' if drawColor == (0, 0, 0) else 'Brush'}"
    cv2.putText(img, tool_text, (10, 740), cv2.FONT_HERSHEY_SIMPLEX, 1, drawColor, 2)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    lmList = findHandLandmarks(img)

    x1, y1 = None, None
    if lmList:
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        if lmList[8][2] < lmList[7][2] and lmList[12][2] < lmList[11][2]:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            if y1 < 90:
                drawColorPalette(img, x1=x1, y1=y1)

        elif lmList[8][2] < lmList[7][2] and lmList[12][2] > lmList[11][2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    drawColorPalette(img)
    displayUI(img)

    cv2.imshow("Virtual Painter", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('z'):
        undo()
    elif key == ord('y'):
        redo()
    elif key == ord('s'):
        pushCanvasState()

cap.release()
cv2.destroyAllWindows()
