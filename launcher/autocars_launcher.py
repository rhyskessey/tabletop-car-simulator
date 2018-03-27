import pygame
from os import listdir
from os.path import isfile

#Defining my colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (30,180,30)
BLUE = (0,0,255)
CYAN = (50,220,220)
YELLOW = (220,220,50)

#Load all available maps
#Currently does not support usb
currentMap = 0
map_paths = []
map_info_paths = []
for folder in listdir("./maps"):
    if ((not isfile(folder)) and (folder[:8] == "autocars")):
        for file in listdir("./maps/" + folder):
            if ((file[-4:] == ".png") and (file[:3] == "map")):
                map_paths.append("./maps/" + folder + "/" + file)
            if ((file[-4:] == ".txt") and (file[:3] == "map")):
                map_info_paths.append("./maps/" + folder + "/" + file)

strategy_paths = []
for file in listdir("./strategies"):
    if ((file[-3:] == ".py") and (file[:5] == "strat")):
        strategy_paths.append("./strategies/" + file)
#strategy_paths = ["./strategies/strategy_default.py","./strategies/strategy_wild.py"]
#Initialise output constructs
currentCar = 0
vision_modes = ["Normal Vision", "Realistic Vision", "Impaired Vision"]
car_types = ["Normal Car", "Motorbike", "Tank"]
en_text = ["Enabled", "Disabled"]
#car_data -> [desc,MAC,enabled,stratFile,visMode,carType]
car_data = [["Red Car", "00:06:66:61:A4:6B", 1,0,0,0],
            ["Green Car","00:06:66:61:A9:3D", 1,0,0,0],
            ["Orange Car","00:06:66:61:9B:2D", 1,0,0,0],
            ["Pink Car","00:06:66:47:0A:0A", 1,0,0,0]]
car_paths = ["./res/red_car.png","./res/green_car.png","./res/orange_car.png","./res/pink_car.png"]

#Label class
class Label:
    def __init__(self,x,y,text):
        self.text = text
        self.font_size = 14
        self.font = pygame.font.SysFont("comicsansms", self.font_size)
        self.font.set_bold(1)
        self.color = WHITE
        self.x = x
        self.y = y
        labels.append(self)

    def render(self):
        screen.blit(self.font.render(self.text, True, self.color), [self.x, self.y])

#Button class
class Button:
    def __init__(self,x,y,w,h):
        self.id = "Blank"
        self.text = ""
        self.font_size = 12
        self.font = pygame.font.SysFont("comicsansms", self.font_size)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.next = [-1,-1,-1,-1]
        self.img = -1
        self.colors = [BLUE,YELLOW,BLACK,CYAN]
        self.border_w = 5
        self.hover = 0
        self.selected = 0
        buttons.append(self)

    #Draw background then border
    def render(self):
        if (self.img == -1):
            #Fill color
            temp_bg_color = self.colors[0]
            if (self.selected == 1):
                temp_bg_color = self.colors[1]
            pygame.draw.rect(screen, temp_bg_color, (self.x,self.y,self.w,self.h), 0)
        else:
            #Draw image
            button_img = pygame.image.load(self.img)
            button_img = pygame.transform.scale(button_img, (self.w,self.h))
            screen.blit(button_img,(self.x,self.y))

        #Draw text
        if (self.text != ""):
            screen.blit(self.font.render(self.text, True, WHITE), [self.x + 8, self.y + self.h/2 - self.font_size/2 - 4])

        temp_bd_color = self.colors[2]
        if (self.hover == 1):
            temp_bd_color = self.colors[3]
        pygame.draw.rect(screen, temp_bd_color, (self.x,self.y,self.w,self.h), self.border_w)

    #Based on current direction options and input, change hover states
    def go_next(self,direction):
        if (self.next[direction] != -1):
            self.hover = 0
            buttons[self.next[direction]].hover = 1

    def onClick(self,button):
        print("You clicked button " + button + " and I'm not doing anything!")
            

def checkOverflow(num,min,max):
    result = num
    if (result < min):
            result = max
    if (result > max):
            result = min
    return result

def loadMap(map_index):
    buttons[0].img = map_paths[map_index]
    labels[0].text = map_paths[map_index]
    labels[1].text = map_info_paths[map_index]

def loadCar(car_index):
    buttons[1].img = car_paths[car_index]
    buttons[2].selected = 1 - car_data[car_index][2]
    buttons[3].text = strategy_paths[car_data[car_index][3]]
    buttons[4].text = vision_modes[car_data[car_index][4]]
    buttons[5].text = car_types[car_data[car_index][5]]
    labels[2].text = car_data[car_index][0] + "  |  " + car_data[car_index][1]
    labels[3].text = en_text[buttons[2].selected]
    labels[3].color = buttons[2].colors[buttons[2].selected]

#Button onClick methods
def onClick_map_image_button(button):
    global currentMap
    currentMap += (-2*button + 1)
    currentMap = checkOverflow(currentMap,0,len(map_paths)-1)
    loadMap(currentMap)

def onClick_car_image_button(button):
    global currentCar
    currentCar += (-2*button + 1)
    currentCar = checkOverflow(currentCar,0,len(car_data)-1)
    loadCar(currentCar)

def onClick_car_enabled_button(button):
    car_data[currentCar][2] = 1 - car_data[currentCar][2]
    loadCar(currentCar)

def onClick_strategy_text_button(button):
    car_data[currentCar][3] += (-2*button + 1)
    car_data[currentCar][3] = checkOverflow(car_data[currentCar][3],0,len(strategy_paths)-1)
    loadCar(currentCar)

def onClick_vision_text_button(button):
    car_data[currentCar][4] += (-2*button + 1)
    car_data[currentCar][4] = checkOverflow(car_data[currentCar][4],0,len(vision_modes)-1)
    loadCar(currentCar)

def onClick_cartype_text_button(button):
    car_data[currentCar][5] += (-2*button + 1)
    car_data[currentCar][5] = checkOverflow(car_data[currentCar][5],0,len(car_types)-1)
    loadCar(currentCar)

def onClick_launch_button(button):
    global done
    if (button == 0):
        done = 1
        #Call michael's program from here using params
    
def init_buttons():
    #Map image button
    t = Button(50,50,225,150)
    t.id = "map_image_button"
    t.img = "./maps/autocars_map_basic/map_basic.png"
    t.next = [-1,6,1,-1]
    t.onClick = onClick_map_image_button
    t.hover = 1

    #Car image button
    t = Button(50,250,225,150)
    t.id = "car_image_button"
    t.img = car_paths[0]
    t.next = [0,2,3,-1]
    t.onClick = onClick_car_image_button

    #Car enabled button
    t = Button(300,350,50,50)
    t.id = "car_enabled_button"
    t.next = [-1,6,-1,1]
    t.onClick = onClick_car_enabled_button
    t.colors = [GREEN,RED,BLACK,CYAN]

    #Strategy text button
    t = Button(100,450,400,30)
    t.id = "strategy_text_button"
    t.next = [1,6,4,-1]
    t.onClick = onClick_strategy_text_button
    t.text = "Default"

    #Agent type text button
    t = Button(100,500,400,30)
    t.id = "agent_type_button"
    t.next = [3,6,5,-1]
    t.onClick = onClick_vision_text_button
    t.text = "Default"

    #Car type text button
    t = Button(100,550,400,30)
    t.id = "car_type_button"
    t.next = [4,6,-1,-1]
    t.onClick = onClick_cartype_text_button
    t.text = "Default"

    #Launch button
    t = Button(580,330,200,250)
    t.id = "launch_button"
    t.next = [-1,-1,-1,1]
    t.onClick = onClick_launch_button
    t.colors = [DARKGREEN,RED,BLACK,CYAN]
    t.text = "Launch"
    t.font = pygame.font.SysFont("comicsansms", 40)

def init_labels():
    #Map file label
    t = Label(300,50,"Default")
    #Map data file label
    t = Label(300,80,"Default")
    #Car ID label
    t = Label(300,250,"Default")
    #Car Enabled label
    t = Label(380,365,"Default")
    t.color = GREEN
    #Strategy file label
    t = Label(22,452,"Strategy:")
    #Vision mode label
    t = Label(5,502,"Vision Mode:")
    #Car type label
    t = Label(24,552,"Car Type:")














#Initialise pygame module
pygame.init()
#Initialise screen with chosen size
size = [800, 600]
screen = pygame.display.set_mode(size)
#Give my game window a title
pygame.display.set_caption("Title Screen")
#Install sexy background (same as screen size)
bg = pygame.image.load("./res/bg_black.jpg")
#Initialise pygame clock
clock = pygame.time.Clock()
#Initialise pygame joystick functions
pygame.joystick.init()
#Initialise buttons
buttons = []
labels = []
init_buttons()
init_labels()
loadCar(currentCar)
loadMap(currentMap)
#Remember last state of the joystick hat
last_hat = [0,0]
#Used to break out of the loop when required
done = 0
while (done == 0):
    button_tapped = -1
    #Check if a joystick is connected
    if (pygame.joystick.get_count() < 1):
        print("No gamepad detected. Exiting...")
        break
    #Given a joystick is connected, initialise it
    #If more than one is connected, we only use the first one
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    #Handle user input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1
        if event.type == pygame.JOYBUTTONDOWN:
            #Note which button was tapped
            #0=A, 1=B, X,Y,LB,RB,St,Se
            index = 0
            while (index < 8):
                if (joystick.get_button(index)):
                    button_tapped = index
                    break
                index += 1
        if event.type == pygame.JOYHATMOTION:
            #Parse hat directions
            this_hat = joystick.get_hat(0)
            #Get difference between hat states
            hat_diff = [this_hat[0] - last_hat[0], this_hat[1] - last_hat[1]]
            #Did we push left or right?
            if (hat_diff[0] != 0 and this_hat[0] != 0):
                for b in buttons:
                    if (b.hover == 1):
                        temp = -1*hat_diff[0]+2
                        if (temp >= 0 and temp <= 3):
                            b.go_next(temp)
                        break
            #Did we push up or down?
            if (hat_diff[1] != 0 and this_hat[1] != 0):
                for b in buttons:
                    if (b.hover == 1):
                        temp = -1*hat_diff[1]+1
                        if (temp >= 0 and temp <= 3):
                            b.go_next(temp)
                        break
            last_hat = this_hat

    #Deal with button tap
    if (button_tapped != -1):
        #We hit a button!
        for b in buttons:
            if (b.hover == 1):
                b.onClick(button_tapped)

    #Wash with clean background
    screen.blit(bg,(0,0))

    #Draw all buttons
    for b in buttons:
        b.render()

    #Draw all labels
    for l in labels:
        l.render()

    #Update screen with new contents
    pygame.display.flip()

    #Limit game fps
    clock.tick(40)

pygame.quit()
quit()




