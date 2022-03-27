import random
from tkinter import *
import math
import sys



sys.setrecursionlimit(1000000000)
WindowX = 1000
WindowY = 1000
lines = 6
speed = 1
SplaceX, SplaceY = 0,0

color = [(217, 237, 146),(24,78,119),(217,237,146)]
no_steps = int(lines*lines/2)+1
gradient = []
for i in range(len(color)-2):
    for j in range(no_steps):
        rgb = (int(color[i][0]+(color[i+1][0]-color[i][0])*j/no_steps),int(color[i][1]+(color[i+1][1]-color[i][1])*j/no_steps),int(color[i][2]+(color[i+1][2]-color[i][2])*j/no_steps))
        gradient.append('%02x%02x%02x' % rgb)
gradient.extend(list(reversed(gradient)))

func = 0
blocksArr = []
linesArr = []
grid = [[False]*lines for _ in range(lines)]
steps = []
failure = {}
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
    global blocksArr

    rect = mainCanvas.create_rectangle(WindowX/lines*(placeX+0.25),
                                WindowY / lines * (placeY+0.25),
                                WindowX/lines*(placeX+0.75),
                                WindowY/lines*(placeY+0.75),fill="#" + gradient[len(steps)])
    blocksArr.append(rect)

def findNext(oriArr):
    global placeX,placeY,grid,steps,linesArr,blocksArr,func
    # print(str(placeX) + "  " + str(placeY))
    # print(steps)
    # print(failure)
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
                    line = mainCanvas.create_line(WindowX / lines * (placeX + 1.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.75), WindowY / lines * (placeY + 0.5),fill="#000", width=3)
                    linesArr.append(line)
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
                    line = mainCanvas.create_line(WindowX / lines * (placeX - 0.25), WindowY / lines * (placeY + 0.5),
                                           WindowX / lines * (placeX + 0.25), WindowY / lines * (placeY + 0.5),fill="#000", width=3)
                    linesArr.append(line)
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
                    line = mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 1.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.75),fill="#000", width=3)
                    linesArr.append(line)
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
                    line = mainCanvas.create_line(WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY - 0.25),
                                           WindowX / lines * (placeX + 0.5), WindowY / lines * (placeY + 0.25),fill="#000", width=3)
                    linesArr.append(line)
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
        # mainCanvas.delete(ALL)
        # drawNew()
        mainCanvas.delete(blocksArr[-1])
        mainCanvas.delete(linesArr[-1])
        blocksArr, linesArr = blocksArr[:-1],linesArr[:-1]
        newArr = [x for x in ['L','R','U','D'] if x not in failure.get(tuple(steps))]
        func = mainCanvas.after(speed, findNext, newArr)
    else:
        draw()
        if(len(steps) + 1 != lines*lines):
        # if(checkIfFinish() == False):
            func = mainCanvas.after(speed, findNext, ['L', 'R', 'U', 'D'])
        else:
            print("Done!")
            print(steps)

draw()
findNext(['L','R','U','D'])


def reset(event):
    global blocksArr,linesArr,gid,steps,failure,SplaceX,SplaceY,placeX,placeY,grid,func
    if (event.keysym == 'space'):
        print("Reset")
        mainCanvas.delete(ALL)
        for i in range(lines):
            mainCanvas.create_line(0, i * (WindowX / lines), WindowY, i * (WindowX / lines), fill="#000")
            mainCanvas.create_line(i * (WindowY / lines), 0, i * (WindowY / lines), WindowX, fill="#000")

        for i in range(lines):
            for j in range(lines):
                mainCanvas.create_text(i * (WindowX / lines) + 12, j * (WindowY / lines) + 5,
                                       text=str(i) + ", " + str(j), font=('Helvetica', str(math.floor(50 / lines))))

        blocksArr = []
        linesArr = []
        grid = [[False] * lines for _ in range(lines)]
        steps = []
        failure = {}
        placeX, placeY = SplaceX, SplaceY
        grid[SplaceX][SplaceY] = True
        draw()
        mainCanvas.after_cancel(func)
        findNext(['L', 'R', 'U', 'D'])

root.bind("<KeyRelease>", reset)

# while(checkIfFinish() == False):
#     findNext(['L','R','U','D'])

root.mainloop()