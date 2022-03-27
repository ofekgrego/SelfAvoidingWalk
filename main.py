import random
from tkinter import *
from array import *
import tkinter
import math
import time

WindowX = 700
WindowY = 700
lines = 4

grid = [[False]*lines for _ in range(lines)]
steps = []
failure = {}
SplaceX, SplaceY = 0,0
placeX, placeY = SplaceX,SplaceY
grid[SplaceX][SplaceY] = True

root = Tk()
root.title("Self Avoiding Walk")
root.resizable(False, False)
root.geometry(str(WindowX) + "x" + str(WindowY))
mainCanvas = Canvas(root, width=WindowX, height=WindowY, background="white")
mainCanvas.pack()

for i in range(lines):
    mainCanvas.create_line(0, i*(WindowX/lines),WindowY,i*(WindowX/lines),fill="#000")
    mainCanvas.create_line(i * (WindowY / lines),0, i * (WindowY / lines),WindowX, fill="#000")

for i in range(lines):
    for j in range(lines):
        mainCanvas.create_text(i*(WindowX/lines)+12,j * (WindowY / lines)+5,text=str(i) + ", " + str(j), font=('Helvetica',str(math.floor(50/lines))))

def draw():
    mainCanvas.create_rectangle(WindowX/lines*(placeX+0.25),
                                WindowY / lines * (placeY+0.25),
                                WindowX/lines*(placeX+0.75),
                                WindowY/lines*(placeY+0.75),fill="#F00")

def drawNew():
    for i in range(lines):
        mainCanvas.create_line(0, i * (WindowX / lines), WindowY, i * (WindowX / lines), fill="#000")
        mainCanvas.create_line(i * (WindowY / lines), 0, i * (WindowY / lines), WindowX, fill="#000")

    for i in range(lines):
        for j in range(lines):
            mainCanvas.create_text(i * (WindowX / lines) + 12, j * (WindowY / lines) + 5, text=str(i) + ", " + str(j),
                                   font=('Helvetica', str(math.floor(50 / lines))))

    for i in range(lines):
        for j in range(lines):
            if(grid[i][j] == True):
                mainCanvas.create_rectangle(WindowX/lines*(i+0.25),
                                WindowY / lines * (j+0.25),
                                WindowX/lines*(i+0.75),
                                WindowY/lines*(j+0.75),fill="#F00")
    placeX,placeY = SplaceX,SplaceY
    for P in steps:
        if (P == 'L'):
                    placeX -= 1
                    mainCanvas.create_line(WindowX / lines * (placeX + 1.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.75), WindowY / lines * (placeY + 0.5), width=3)
        elif (P == 'R'):
                    placeX += 1
                    mainCanvas.create_line(WindowX / lines * (placeX - 0.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.25), WindowY / lines * (placeY + 0.5), width=3)
        elif (P == 'U'):
                    placeY -= 1
                    mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 1.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.75), width=3)
        elif (P == 'D'):
                    placeY += 1
                    mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY - 0.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.25), width=3)


def checkIfFinish():
    for i in range(lines):
        for j in range(lines):
            if(grid[i][j] == False):
                return False
    return True

def findNext(oriArr):
    global placeX,placeY,grid,steps
    print(str(placeX) + "  " + str(placeY))
    print("steps: " + str(steps))
    print("oriArr: " + str(oriArr))
    arr = [item[:] for item in oriArr]
    stop = False
    while((stop == False) & (len(arr) > 0)):
        P = random.choice(arr)
        if(P == 'L'):
            if(placeX != 0):
                if(grid[placeX-1][placeY] == False):
                    stop = True
                    placeX -= 1
                    grid[placeX][placeY] = True
                    steps.append('L')
                    mainCanvas.create_line(WindowX / lines * (placeX + 1.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.75), WindowY / lines * (placeY + 0.5), width=3)
                else:
                    arr.remove('L')
            else:
                arr.remove('L')
        elif(P == 'R'):
            if (placeX != lines - 1):
                if(grid[placeX+1][placeY] == False):
                    stop = True
                    placeX += 1
                    grid[placeX][placeY] = True
                    steps.append('R')
                    mainCanvas.create_line(WindowX / lines * (placeX - 0.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.25), WindowY / lines * (placeY + 0.5), width=3)
                else:
                    arr.remove('R')
            else:
                arr.remove('R')
        elif(P == 'U'):
            if (placeY != 0):
                if(grid[placeX][placeY-1] == False):
                    stop = True
                    placeY -= 1
                    grid[placeX][placeY] = True
                    steps.append('U')
                    mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 1.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.75), width=3)
                else:
                    arr.remove('U')
            else:
                arr.remove('U')
        elif(P == 'D'):
            if (placeY != lines - 1):
                if (grid[placeX][placeY + 1] == False):
                    stop = True
                    placeY += 1
                    grid[placeX][placeY] = True
                    steps.append('D')
                    mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY - 0.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.25), width=3)
                else:
                    arr.remove('D')
            else:
                arr.remove('D')
    if(len(arr) == 0):
        P = steps[len(steps)-1]
        steps.pop(-1)
        grid[placeX][placeY] = False
        if (P == 'L'):
                placeX += 1
        elif (P == 'R'):
                placeX -= 1
        elif (P == 'U'):
                placeY += 1
        elif (P == 'D'):
                placeY -= 1
        if tuple(steps) in failure.keys():
            array = failure.get(tuple(steps))
            array.append(P)
            failure.update({tuple(steps): array})
        else:
            failure.update({tuple(steps): [P]})
        mainCanvas.delete(ALL)
        drawNew()
        newArr = [x for x in ['L','R','U','D'] if x not in failure.get(tuple(steps))]
        mainCanvas.after(100, findNext, newArr)
        # findNext(newArr)
    else:
        draw()
        if(checkIfFinish() == False):
            mainCanvas.after(100, findNext, ['L', 'R', 'U', 'D'])
            # findNext(['L', 'R', 'U', 'D'])
            print(steps)
        else:
            print("Done!")

draw()
findNext(['L','R','U','D'])

# while(checkIfFinish() == False):
#     findNext(['L','R','U','D'])
print(steps)

root.mainloop()