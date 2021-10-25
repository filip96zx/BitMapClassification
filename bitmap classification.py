import tkinter as tk

import numpy
from PIL import Image, ImageDraw, ImageTk
from math import sqrt
import cv2
import time

classes = []
test = []
size = 1
rubber = False
step = 1

while True:
    try:
        bitmap = cv2.bitwise_not(cv2.imread('class' + str(len(classes) + 1) + '.bmp', 0))
        if bitmap is None:
            break
    except FileNotFoundError:
        break
    classes.append(numpy.ceil(bitmap / 255.0))

try:
    img = Image.open('test1.bmp')
except FileNotFoundError:
    img = Image.new('1', [len(classes[0][0]), len(classes[0])], color='white')


def loadTest():
    test.clear()
    test.append(numpy.ceil(cv2.bitwise_not(cv2.imread('test' + str(len(test) + 1) + '.bmp', 0)) / 255.0))


def niepodobienstwo(BA, BB, Xsarray, rstep):
    miara = 0
    for pay, j in enumerate(BA):
        for pax, k in enumerate(j):
            if k == 1:
                odl_min = float('inf')
                flag = True
                r = 0
                while flag:
                    points = circle(pay, pax, r, Xsarray)
                    for point in points:
                        try:
                            if BB[point[0]][point[1]] == 1:
                                odl_akt = sqrt(((pax - point[1]) ** 2) + ((pay - point[0]) ** 2))
                                odl_min = min(odl_akt, odl_min)
                                flag = False
                        except IndexError:
                            if point[0] < 0:
                                point[0] = 0
                            if point[0] > len(BB) - 1:
                                point[0] = len(BB) - 1
                            if point[1] < 0:
                                point[1] = 0
                            if point[1] > len(BB[0]) - 1:
                                point[1] = len(BB[0]) - 1
                            if BB[point[0]][point[1]] == 1:
                                odl_akt = sqrt(((pax - point[1]) ** 2) + ((pay - point[0]) ** 2))
                                odl_min = min(odl_akt, odl_min)
                                flag = False
                    if r > len(BB)+len(BB[0]):
                        flag = False
                    r += rstep
                miara += odl_min
    try:                                            # jeżeli flag niezdefiowane tzn. nie bylo czarnego punktu
        flag                                        # obslugujemy wyjątek zwracamy nieskonczonosc
    except UnboundLocalError:
        return float('inf')
    return miara


def circle(sy, sx, r, arr):
    y = range(0, int((r * 0.715) + 1))
    points = []
    newpoints = []
    if r >= len(arr):
        for index, y in enumerate(y):
            c = y ** 2 - r ** 2
            delta = sqrt(-4 * c)
            x1 = round(delta / 2)
            points.extend([[sy + index, sx + x1], [sy + index, sx - x1], [sy - index, sx + x1], [sy - index, sx - x1],
                           [sy + x1, sx - index], [sy - x1, sx - index], [sy + x1, sx + index], [sy - x1, sx + index]])
            newpoints.append(x1)
            if x1 == index:
                break
        if r > len(arr):
            arr.extend([[0]] * (r - len(arr)))
        arr.append(newpoints)
    else:
        for index, x1 in enumerate(arr[r]):
            points.extend([[sy + index, sx + x1], [sy + index, sx - x1], [sy - index, sx + x1], [sy - index, sx - x1],
                           [sy + x1, sx - index], [sy - x1, sx - index], [sy + x1, sx + index], [sy - x1, sx + index]])
    return points


x = []
lastr = [0]
def miara_podobienstwa(BA, BB, rstep):
    if lastr[0] != rstep:                                        # resetuje tablice x'ów jeżeli zmieniono rstep
        x.clear()
        lastr[0] = rstep
    return -(niepodobienstwo(BA, BB, x, rstep) + niepodobienstwo(BB, BA, x, rstep))

def niepodobienstwo1(BA, BB):
    miara = 0
    for pay, j in enumerate(BA):
        for pax, k in enumerate(j):
            if k == 1:
                odl_min = float('inf')
                for pby, l in enumerate(BB):
                    for pbx, m in enumerate(l):
                        if m == 1:
                            odl_akt = sqrt(((pax - pbx) ** 2) + ((pay - pby) ** 2))
                            odl_min = min(odl_akt, odl_min)
                miara += odl_min
    return miara


def miara_podobienstwa1(BA, BB):
    return -(niepodobienstwo1(BA, BB) + niepodobienstwo1(BB, BA))

def draw(event):
    if size > 2 and not rubber:
        x1, y1 = (event.x - size / 2), (event.y - size / 2)
        x2, y2 = (event.x + size / 2), (event.y + size / 2)
        canvas.create_oval(x1, y1, x2, y2, fill='black')
        ImageDraw.Draw(img).ellipse([x1, y1, x2, y2], fill='black')
    elif size > 2 and rubber:
        x1, y1 = (event.x - size / 2), (event.y - size / 2)
        x2, y2 = (event.x + size / 2), (event.y + size / 2)
        canvas.create_oval(x1, y1, x2, y2, fill='white', outline='white')
        ImageDraw.Draw(img).ellipse([x1, y1, x2, y2], fill='white')
    elif size <= 2 and not rubber:
        x, y = event.x, event.y
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            canvas.create_line(x, y, x1, y1, width=size)
            ImageDraw.Draw(img).line([x, y, x1, y1], width=size)
        canvas.old_coords = x, y
    elif size <= 2 and rubber:
        x, y = event.x, event.y
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            canvas.create_line(x, y, x1, y1, width=size, fill='white')
            ImageDraw.Draw(img).line([x, y, x1, y1], width=size, fill='white')
        canvas.old_coords = x, y


def reset_coords(event):
    canvas.old_coords = None


def incWidth():
    global size
    size += 1


def decWidth():
    global size
    if size > 1:
        size += -1

def incStep():
    global step
    step += 1
    stepinfo.configure(text='r step: ' + str(step))

def decStep():
    global step
    if step > 1:
        step += -1
        stepinfo.configure(text='r step: '+str(step))


def rubberbtn():
    global rubber
    if rubber:
        rubberBTN.configure(relief='raised')
        rubber = not rubber
    else:
        rubberBTN.configure(relief='sunken')
        rubber = not rubber


def clearbtn():
    canvas.delete("all")
    global img
    img = Image.new('1', [len(classes[0][0]), len(classes[0])], color='white')


def startTest(rstep):
    img.save("test1.bmp")
    loadTest()
    start_time = time.time()
    result = []
    if menuSelect.get():
        for i in classes:
            result.append(round(miara_podobienstwa(test[0], i, rstep), 2))
    else:
        for i in classes:
            result.append(round(miara_podobienstwa1(test[0], i), 2))
    result.append(str(round(time.time() - start_time, 2)) + ' s.')
    openNewWindow(result)



def openNewWindow(result):
    newWindow = tk.Toplevel(root)
    newWindow.title("Results")
    newWindow.image = []
    exectime = result.pop()
    for i in range(0, len(result)):
        nw = tk.Frame(newWindow, relief='raised', bd=3)
        nw.grid(column=int(i % 6), row=int((i/6)+1))
        newWindow.image.append(ImageTk.PhotoImage(Image.open('class' + str(i + 1) + '.bmp')))
        if max(result) == result[i]:
            lab = tk.Label(nw, image=newWindow.image[i], bg='green', text=str(i), bd=4)
        else:
            lab = tk.Label(nw, image=newWindow.image[i], bd=4)
        lab.pack()
        tk.Label(nw, text='Class ' + str(int(i + 1)) + ', result: ' + str(result[i])).pack()

    tk.Label(newWindow, text='Time: ' + exectime).grid(column=0, sticky='w')


root = tk.Tk()
root.title('Bitmap classification')
menuSelect = tk.BooleanVar()
menuSelect.set(True)

# Drawing window
drawWindow = tk.Frame(root, relief='raised', bd=3)
canvas = tk.Canvas(drawWindow, width=len(classes[0][0]), height=len(classes[0]), bg='white')
canvas.pack()
drawWindow.grid(column=1, row=2, pady=5, padx=5)

try:
    testimg = ImageTk.PhotoImage(Image.open('test1.bmp'))
except FileNotFoundError:
    testimg = ImageTk.PhotoImage(img)

canvas.create_image(0, 0, anchor='nw', image=testimg)

# Drawing tools
drawtools = tk.Frame(root)
tk.Button(drawtools, text='+', command=incWidth).pack(side='left')
tk.Button(drawtools, text='-', command=decWidth).pack(side='left')
rubberBTN = tk.Button(drawtools, text='□', relief='raised', command=rubberbtn)
rubberBTN.pack(side='left')
tk.Button(drawtools, text='Clear', command=clearbtn).pack(side='bottom')
drawtools.grid(column=1, row=1)

# Test Button
tk.Button(root, text='Test', bd=3, command=lambda: startTest(step)).grid(column=1, row=5)

# Check1
chk1 = tk.Checkbutton(root, text='Algorytm 1', bd=3, relief='raised', var=menuSelect, onvalue=False, offvalue=True)\
    .grid(column=1, row=3)

#Step settings
stepconfig = tk.Frame(root, relief='raised', bd=3)
chk2 = tk.Checkbutton(stepconfig, text='Algorytm 2', var=menuSelect, onvalue=True, offvalue=False).pack(side='top')
tk.Button(stepconfig, text='+', command=incStep).pack(side='left')
tk.Button(stepconfig, text='-', command=decStep).pack(side='left')
stepinfo = tk.Label(stepconfig, text='r step: '+str(step), bd=5)
stepinfo.pack(side='left')
stepconfig.grid(column=1, row=4)

canvas.old_coords = None
canvas.bind('<B1-Motion>', draw)
canvas.bind('<Button-1>', draw)
root.bind('<ButtonRelease-1>', reset_coords)

root.mainloop()
