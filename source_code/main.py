import pygame
from pygame.locals import *
import numpy as np
from tkinter import *
from tkinter import messagebox
import matplotlib
import matplotlib.pyplot as plt
import login
from login import user_name

class Queue:
    def __init__(self):
        self.rear = -1
        self.item = []
    def isEmpty(self):
        if self.rear == -1:
            return True
        else:
            return False
    def enqueue(self, newVal):
        self.item.insert(0, newVal)
        self.rear += 1
    def dequeue(self):
        if self.isEmpty():
            return -1
        else:
            self.rear -= 1
            return self.item.pop()

class Neuron:
    def __init__(self, number, type, sensitivity, receptors):
        self.number = number
        self.type = type
        self.axonHillock_sensitivity = sensitivity
        self.receptors = receptors
        self.LTP_receptors = 1
        self.dendrite_item = Queue()
        self.neuron_item = Queue()
        for i in range(totalTime):
            self.dendrite_item.enqueue(0)
            self.neuron_item.enqueue(0)
    def dendrite_stimulate(self, neuron):
        dendrite_stimulated_voltage = np.sin(np.array([v*np.pi/timeRange for v in range(timeRange)])).tolist()
        if neuron.type == "excitatory":
            for i in range(timeRange):
                self.dendrite_item.item[i] += self.receptors*self.LTP_receptors*dendrite_stimulated_voltage[i]
        elif neuron.type == "inhibitory":
            for i in range(timeRange):
                self.dendrite_item.item[i] -= self.receptors*self.LTP_receptors*dendrite_stimulated_voltage[i]
    def neuron_stimulate(self):
        neuron_stimulated_voltage = np.sin(np.array([v*np.pi/timeRange for v in range(timeRange)])).tolist()
        for i in range(timeRange):
            self.neuron_item.item[i] += neuron_stimulated_voltage[i]
    def conduct(self):
        self.dendrite_item.dequeue()
        self.dendrite_item.enqueue(0)
        self.neuron_item.dequeue()
        self.neuron_item.enqueue(0)
    def get_dendrite_voltage(self):
        return self.dendrite_item.item
    def get_last_dendrite_voltage(self):
        return self.dendrite_item.item[totalTime-1]
    def get_neuron_voltage(self):
        return self.neuron_item.item
    def get_last_neuron_voltage(self):
        return self.neuron_item.item[totalTime-1]

def graph_setting():
    x = range(totalTime)
    lines = []
    plt.grid = True
    plt.ion()
    figure = plt.figure()
    name = ["dendrite5", "dendrite6", "neuron5", "neuron6", "LTP dendrite", "LTP neuron"]
    for i in range(6):
        value = 321 + i
        ax = figure.add_subplot(value)
        y = [0 for i in range(totalTime)]
        line, = ax.plot(x, y)
        lines.append(line)
        plt.title(f"{name[i]}", fontsize=14)
        plt.xlabel("distance", fontsize=8)
        plt.ylabel("voltage", fontsize=8)
        plt.ylim(-10, 10)
    plt.subplots_adjust(hspace=1)
    return lines, figure

def draw_graph(lines, figure):
    ys = [neurons[4].get_dendrite_voltage(), neurons[5].get_dendrite_voltage(), neurons[4].get_neuron_voltage(), neurons[5].get_neuron_voltage(), neurons[6].get_dendrite_voltage(), neurons[6].get_neuron_voltage()]
    x = range(totalTime)
    for i in range(len(ys)):
        y = ys[i]
        lines[i].set_xdata(x)
        lines[i].set_ydata(y)
    figure.canvas.draw()
    figure.canvas.flush_events()

def clicking(img_x, img_y, img_width, img_height):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if img_x <= mouse[0] <= img_x+img_width and img_y <= mouse[1] <= img_y+img_height:
        if click[0]:
            clickSound.play()
            return True
        else:
            return False

# https://076923.github.io/posts/Python-tkinter-7/
# https://qastack.kr/programming/111155/how-do-i-handle-the-window-close-event-in-tkinter
def revise_neuron(i):
    def check():
        nonlocal neuron_type
        neuron_type = RadioVariety.get()

    def confirm1():
        nonlocal v
        volt = float(ent1.get())
        if minV <= volt <= maxV:
            lbl_V["text"] = "사용 가능한 값입니다."
            v = volt
        else:
            lbl_V["text"] = "범위를 벗어났습니다. 다시 입력해 주세요."
            v = 0

    def confirm2():
        nonlocal n
        N = float(ent2.get())
        if minN <= N <= maxN:
            lbl_N["text"] = "사용 가능한 값입니다."
            n = N
        else:
            lbl_N["text"] = "범위를 벗어났습니다. 다시 입력해 주세요."
            n = 0

    def on_closing():
        if neuron_type == "none" and v == 0 and n == 0:
            if messagebox.askokcancel("Quit", "변경사항 없이 끝내겠습니까?"):
                w.destroy()
        else:
            if messagebox.askokcancel("Quit", "변경하시겠습니까?"):
                w.destroy()

    w = Tk()
    w.title(f"Neuron{neurons[i].number} 정보 수정")
    w.geometry("420x160")
    lbl_title = Label(w, text=f"Revise Neuron{neurons[i].number}", font=(FONT, 20, "bold"))
    lbl1 = Label(w, text="유형(type)")
    lbl2 = Label(w, text="축삭둔덕 역치전위")
    lbl3 = Label(w, text="가지돌기 수용체 수")
    lbl_title.grid(row=0, column=1)
    lbl1.grid(row=1, column=0)
    lbl2.grid(row=2, column=0)
    lbl3.grid(row=4, column=0)
    neuron_type = "none"
    v = 0
    n = 0
    if neurons[i].type == "excitatory":
        RadioVariety = StringVar(None, "excitatory")
    else:
        RadioVariety = StringVar(None, "inhibitory")
    radio1 = Radiobutton(w, text="흥분성", value="excitatory", variable=RadioVariety, command=check)
    radio2 = Radiobutton(w, text="억제성", value="inhibitory", variable=RadioVariety, command=check)
    radio1.grid(row=1, column=1)
    radio2.grid(row=1, column=2)
    ent1 = Entry(w)
    ent1.insert(0, f"{neurons[i].axonHillock_sensitivity}")
    ent1.grid(row=2, column=1)
    btn1 = Button(w, text="확인", command=confirm1)
    btn1.grid(row=2, column=2)
    lbl_V = Label(w, text=f"최소 전위: {minV}, 최대 전위: {maxV}")
    lbl_V.grid(row=3, column=0, columnspan=3)
    ent2 = Entry(w)
    ent2.insert(0, f"{neurons[i].receptors}")
    ent2.grid(row=4, column=1)
    btn2 = Button(w, text="확인", command=confirm2)
    btn2.grid(row=4, column=2)
    lbl_N = Label(w, text=f"최소 개수: {minN}, 최대 개수: {maxN}")
    lbl_N.grid(row=5, column=0, columnspan=3)
    w.protocol("WM_DELETE_WINDOW", on_closing)
    w.mainloop()
    if neuron_type == "none":
        neuron_type = neurons[i].type
    if v == 0:
        v = neurons[i].axonHillock_sensitivity
    if n == 0:
        n = neurons[i].receptors
    return neuron_type, v, n

#학습지 참조
def information():
    def Next():
        nonlocal n
        n += 1
        if n > len(files)-1:
            n = 0
        photo = PhotoImage(file=files[n])
        name = names[n]
        lbl_photo['image'] = photo
        lbl_photo.image = photo
        lbl_name['text'] = name

    def Prev():
        nonlocal n
        n -= 1
        if n < 0:
            n = len(files)-1
        photo = PhotoImage(file=files[n])
        name = names[n]
        lbl_photo['image'] = photo
        lbl_photo.image = photo
        lbl_name['text'] = name

    files = ["explain1.png", "explain2.png", "explain3.png"]
    names = ["신경 전달 메커니즘", "LTP", "조작법"]
    n = 0
    t = Tk()
    t.title("Information")
    t.geometry("605x450")
    btnPrev = Button(t, text="이전", command=Prev)
    btnNext = Button(t, text="다음", command=Next)
    photo = PhotoImage(file=files[0])
    bg = PhotoImage(file="explain_bg.png")
    bg_label = Label(t, image=bg)
    bg_label.grid(row=0, column=0, rowspan=2, columnspan=2)
    lbl_name = Label(t, text=names[0], width=20, height=1, bg="Violet", relief="raised", font=(FONT, 10, "bold"))
    lbl_photo = Label(t, image=photo)
    lbl_name.grid(row=0, column=0, columnspan=2)
    lbl_photo.grid(row=1, column=0, columnspan=2)
    btnPrev.grid(row=2, column=0)
    btnNext.grid(row=2, column=1)
    t.mainloop()

timeRange = 3*int(np.pi)
totalTime = 20
minV=1; maxV=5
minN=1; maxN=3
to_synapse_last_voltage = 0.9
waiting5_d = 0
waiting6_d = 0
waiting7_d = 0
waiting5_n = 0
waiting6_n = 0
LTP_waiting=0
LTPing = 0

FONT = "배달의민족 한나체 Pro 보통"
neurons = [Neuron(i, "excitatory", 2, 1) for i in range(1, 8)]
FPS = 30
fpsClock = pygame.time.Clock()
pygame.init()
screen_width=1120
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("LTPS")
running = True
showing = False

try:
    clickSound = pygame.mixer.Sound("clickSound.wav")
    background = pygame.image.load("main_page.png")
    graph_image = pygame.image.load("graph.png")
    graph_delete_image = pygame.image.load("graph_delete.png")
    info_image1 = pygame.image.load("info1.png")
    info_image2 = pygame.image.load("info2.png")
    info_image3 = pygame.image.load("info3.png")
    info_image4 = pygame.image.load("info4.png")
    info_image5 = pygame.image.load("info5.png")
    info_image6 = pygame.image.load("info6.png")
    info_image7 = pygame.image.load("info7.png")
    program_info_image = pygame.image.load("program_info.png")
except Exception as err:
    print("그림 또는 효과음 삽입에 문제가 있습니다:", err)
    pygame.quit()
    exit(-1)

lines=[]
figure = matplotlib.figure.Figure
while running:
    info_size = info_image1.get_rect().size
    info_width = info_size[0]; info_height = info_size[1]
    graph_size = graph_image.get_rect().size
    graph_width = graph_size[0]; graph_height = graph_size[1]
    program_info_size = program_info_image.get_rect().size
    program_info_width = program_info_size[0]; program_info_height = program_info_size[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_1:
                neurons[4].dendrite_stimulate(neurons[0])
            elif event.key == K_2:
                neurons[4].dendrite_stimulate(neurons[1])
            elif event.key == K_3:
                neurons[5].dendrite_stimulate(neurons[2])
            elif event.key == K_4:
                neurons[5].dendrite_stimulate(neurons[3])
        if clicking(850, 30, graph_width, graph_height) and not showing:
            lines, figure = graph_setting()
            showing = True
        if clicking(900, 30, graph_width, graph_height) and showing:
            plt.close()
            showing = False
        if clicking(220, 50, info_width, info_height):
            t, v, n = revise_neuron(0)
            neurons[0].type = t
            neurons[0].axonHillock_sensitivity = v
            neurons[0].receptors = n
        if clicking(220, 180, info_width, info_height):
            t, v, n = revise_neuron(1)
            neurons[1].type = t
            neurons[1].axonHillock_sensitivity = v
            neurons[1].receptors = n
        if clicking(220, 320, info_width, info_height):
            t, v, n = revise_neuron(2)
            neurons[2].type = t
            neurons[2].axonHillock_sensitivity = v
            neurons[2].receptors = n
        if clicking(220, 460, info_width, info_height):
            t, v, n = revise_neuron(3)
            neurons[3].type = t
            neurons[3].axonHillock_sensitivity = v
            neurons[3].receptors = n
        if clicking(540, 100, info_width, info_height):
            t, v, n = revise_neuron(4)
            neurons[4].type = t
            neurons[4].axonHillock_sensitivity = v
            neurons[4].receptors = n
        if clicking(580, 370, info_width, info_height):
            t, v, n = revise_neuron(5)
            neurons[5].type = t
            neurons[5].axonHillock_sensitivity = v
            neurons[5].receptors = n
        if clicking(1030, 280, info_width, info_height):
            t, v, n = revise_neuron(6)
            neurons[6].type = t
            neurons[6].axonHillock_sensitivity = v
            neurons[6].receptors = n
        if clicking(950, 35, program_info_width, program_info_height):
            information()
    for neuron in neurons:
        neuron.conduct()
    waiting5_d-=1
    waiting6_d-=1
    waiting7_d-=1
    waiting5_n-=1
    waiting6_n-=1
    if LTP_waiting > 0:
        LTP_waiting-=1
    if LTPing > 0:
        LTPing-=1
    if neurons[4].get_last_dendrite_voltage() > neurons[4].axonHillock_sensitivity and waiting5_d < 0:
        neurons[4].neuron_stimulate()
        waiting5_d = timeRange
    if neurons[5].get_last_dendrite_voltage() > neurons[5].axonHillock_sensitivity and waiting6_d < 0:
        neurons[5].neuron_stimulate()
        waiting6_d = timeRange
    if neurons[6].get_last_dendrite_voltage() > neurons[6].axonHillock_sensitivity and waiting7_d < 0:
        neurons[6].neuron_stimulate()
        waiting7_d = timeRange
        LTP_waiting += 20
    if neurons[4].get_last_neuron_voltage() > to_synapse_last_voltage and waiting5_n < 0:
        neurons[6].dendrite_stimulate(neurons[4])
        waiting5_n = timeRange
    if neurons[5].get_last_neuron_voltage() > to_synapse_last_voltage and waiting6_n < 0:
        neurons[6].dendrite_stimulate(neurons[5])
        waiting6_n = timeRange
    if LTP_waiting > 60 and LTPing == 0 and neurons[6].LTP_receptors < maxN:
        neurons[6].LTP_receptors += 1
        LTPing = 20
    if LTP_waiting == 0 and neurons[6].LTP_receptors > minN:
        neurons[6].LTP_receptors -= 1
    if showing:
        draw_graph(lines, figure)
    screen.blit(background, (0,0))
    screen.blit(graph_image, (850, 30))
    screen.blit(graph_delete_image, (900, 30))
    screen.blit(info_image1, (220, 50))
    screen.blit(info_image2, (220, 180))
    screen.blit(info_image3, (220, 320))
    screen.blit(info_image4, (220, 460))
    screen.blit(info_image5, (540, 100))
    screen.blit(info_image6, (580, 370))
    screen.blit(info_image7, (1030, 280))
    screen.blit(program_info_image, (950, 35))
    pygame.draw.ellipse(screen, (0, 200, 0), (1010, 30, 50, 50), 0)
    fontObj = pygame.font.Font("AdobeFanHeitiStd-Bold.otf", 18)
    textSurfaceObj = fontObj.render(user_name, True, (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (1035, 55)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()
    fpsClock.tick(FPS)
pygame.quit()