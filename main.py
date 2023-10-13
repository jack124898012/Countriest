import pygame, sys, math, mapmanager, os, threading, save
from maps import default
import time, iconmanager
import build as Building
import options as gameoptions
from image import *
import number
from SaveInfoSteve import get as getLine
import SaveInfoSteve as saveman
import random

# buildings
from buildings import House, Bakery, Road, Tree

# When getting external info from menu (ex which map to use, or if the game should be full screen, use launch.options)
pygame.init()

options = open("misc\\launch.options", "r")
launch = options.readlines()
options.close()

mapname = launch[0] + ".map"
sandboxenabled = True
saveinfo = None

with open("maps\\" + launch[0] + ".saveinfo", "r") as file:
    saveinfo = file.readlines() 

appletime = 0
showfps = gameoptions.getOption("fps") == "SHOW"
showxy = gameoptions.getOption("xy") == "SHOW"
speed = int(gameoptions.getOption("cameraspeed"))
fpscap = int(gameoptions.getOption("fpscap"))
fpscapon = gameoptions.getOption("fpscap-enabled") == "YES"
saveint = int(gameoptions.getOption("saveint"))

if speed < 10: speed = 10
if speed > 250: speed = 250
if fpscap < 10: fpscap = 10
if fpscap > 1000: fpscap = 1000
if saveint < 5: saveint = 5
if saveint > 300: saveint = 300
speed *= 10

resourcebaroffset = 64
fps = 10
fullscreen = False
width, height = 800, 600

window = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF)
if fullscreen: window = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)

pygame.display.set_caption("Countriest - " + str(mapname))

BLACK = (0, 0, 0)

isRunning = True

loaded_map = []
persons = [[0,0],[5,0]]

scrimg.set_colorkey((255,255,255))

clock = pygame.time.Clock()

arial = pygame.font.SysFont("Arial", 30)
resource = pygame.font.SysFont("Arial", 18)
infoText = ""
count = 0
prevFps = 0

pygame.mouse.set_pos(0, 0)

# resources

steel = int(getLine(saveinfo, "steel"))
wood = int(getLine(saveinfo, "wood"))
stone = int(getLine(saveinfo, "stone"))
foodAmount = int(getLine(saveinfo, "food"))

camera = {'x' : int(getLine(saveinfo, "cx")), 'y' : int(getLine(saveinfo, "cy"))}
#camera = {'x' : (32*16)-160, 'y' : (32*15)-64}

currentSaveInfo = ["steel:" + str(steel), "wood:" + str(wood), "stone:" + str(stone), "food:" + str(foodAmount), "cx:" + str(camera['x']), "cy:" + str(camera['y'])]

resourcedisplay = window.blit(resourcebar, (0,0))
destroy = window.blit(bulldoze, (-1000,-1000))
scrbut = window.blit(scrimg, (0+1,height-16-1))
arrowup = window.blit(arrowupimg, (width-74-43+20, 30))
theSidebar = window.blit(sidebar, (width, 0))
building = window.blit(buildimg, (width, 0))
building2 = window.blit(buildimg2, (width, 0))
building3 = window.blit(buildimg3, (width, 0))
building4 = window.blit(buildimg4, (width, 0))
building5 = window.blit(buildimg5, (width, 0))
xbutton = window.blit(xbuttoni, (width, 550))
savemap = window.blit(savebutton, (1, height-100))
arrowdown = window.blit(arrowdownimg, (width-74-43+20, 30+46+46+46+46+15+15+15+15+61+61))
selectedTile = window.blit(sel, (0,0))
personmove = 0
build = False
#mapmanager.saveMap("1.map", (15, 10), default.make((15, 10)))
sandbox = window.blit(sandboxi, (16,16))
loaded_map = mapmanager.getMap(mapname) 
arrownum = 0
canTakeScreenshot = True
selectTile = (0,0)
mapTile = (0,0)
buildclick = 0

gridSize = (loaded_map[0][0]-1, loaded_map[0][1]-1)
def buttonClick():
    pygame.mixer.music.set_volume(0.24)
    pygame.mixer.music.load("sounds\\buttonclick.mp3")
    pygame.mixer.music.play()
def screenshot():
    global canTakeScreenshot
    if not canTakeScreenshot: return
    canTakeScreenshot = False
    pygame.mixer.music.load("sounds\\scrshot.mp3")
    pygame.mixer.music.play()
    i = sum([len(files) for r,d, files in os.walk("screenshots")])+1
    pygame.image.save(window,"screenshots\\screenshot" + str(i) + ".jpg")

saver = 0
nobuilderror = True
deltatime = 1/fps
addpersons = 0
personoffset = [[1,6],[2,3]]
# optimize test
while isRunning:
    if fps < 1:
        deltatime = 1
    else:
        deltatime = 1/fps
    build = False
    m = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save.update(mapname, loaded_map)
            saveman.updateFile(currentSaveInfo, launch[0] + ".saveinfo")
            isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2: # ON MIDDLE CLICK
            print(m)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # ON LEFT CLICK
            if savemap.collidepoint(m):
                save.update(mapname, loaded_map)
                saveman.updateFile(currentSaveInfo, launch[0] + ".saveinfo")
                buttonClick()
            if scrbut.collidepoint(m):
                screenshot()
            if arrowup.collidepoint(m):
                if arrownum > 0:
                    arrownum -= 1
                    buttonClick()
            if arrowdown.collidepoint(m):
                if len(iconmanager.buildings) > arrownum + 5:
                    arrownum += 1
                    buttonClick()
            build = True
            if building.collidepoint(m):
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 1+arrownum
                build = False
            if building2.collidepoint(m):
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 2+arrownum
                build = False
            if building3.collidepoint(m):
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 3+arrownum
                build = False
            if building4.collidepoint(m):
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 4+arrownum
                build = False
            if building5.collidepoint(m):
                # building[4+arrownum]
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 5+arrownum
                build = False
            if xbutton.collidepoint(m):
                buttonClick() # On click on tile build until xbutton.png clicked
                buildclick = 0

            if destroy.collidepoint(m):
                buildclick = -1
                buttonClick()
            if sandboxenabled and sandbox.collidepoint(m):
                with open("sand.box", "w") as file:
                    file.writelines([launch[0] + ".saveinfo"])
                os.system("python Sandbox.py")
                isRunning = False
                
    # Camera movement
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w] and camera['y'] < height+(gridSize[1]*16):
        camera['y'] += int(speed*deltatime)+1
    elif key_pressed[pygame.K_s] and camera['y'] > (height+gridSize[1]*16)*-1:
        camera['y'] -= int(speed*deltatime)+1
    elif key_pressed[pygame.K_a] and camera['x'] < width+gridSize[0]*16:
        camera['x'] += int(speed*deltatime)+1
    elif key_pressed[pygame.K_d] and camera['x'] > (width+gridSize[0]*16)*-1:
        camera['x'] -= int(speed*deltatime)+1
    # Logic
    count += 1
    if count >= math.floor(fps):
        appletime += 1
        personmove += 1
        prevFps = fps
        count = 0
        saver += 1
        canTakeScreenshot = True
        if saver >= saveint:
            saver = 0
            save.update(mapname, loaded_map)
            saveman.updateFile(currentSaveInfo, launch[0] + ".saveinfo")
        if appletime >= 120:
            appletime = 0
            for c in range(len(loaded_map[1])):
                if loaded_map[1][c][2] == 9:
                    foodAmount += 1
        if personmove >= 3: # make people move
            personmove = 0
            if addpersons > 0:
                for offset in range(len(personoffset)):
                    personoffset[offset][0] = random.randint(1,16)
                    personoffset[offset][1] = random.randint(1,16)
                for person in range(len(persons)):
                    c = persons[person]
                    countp = 0
                    while c in persons:
                        countp += 1
                        c = persons[person]
                        if countp >= 10:
                            del persons[person]
                            addpersons += 1
                            break
                        else:
                            mp = -1
                            i = random.randint(0, 1)
                            if random.randint(1, 2) == 2: mp = 1
                            if c[i] <= 1: mp = 1
                            if c[i] >= loaded_map[0][i]-1: mp = -1
                            c[i] += mp
                            if not c in persons and mapmanager.getTile(loaded_map[1], c[0], c[1]) == 0:
                                persons[person] == c
                                break
                
    if addpersons > 0:
        addpersons -= 1
        persons.append([0,0])
    currentSaveInfo = ["steel:" + str(steel), "wood:" + str(wood), "stone:" + str(stone), "food:" + str(foodAmount), "cx:" + str(camera['x']), "cy:" + str(camera['y'])]
    infoText = ""
    if showxy:
        infoText += "X: " + str(camera['x']) + ", Y: " + str(camera['y'])
    if showfps and showxy:
        infoText += ", "
    if showfps:
        infoText += "FPS: " + str(prevFps)
    
    selectedTile = None
    nobuilderror = True
    if buildclick != 0:
        sel = mapmanager.builds[buildclick]
        for cn in range(len(loaded_map[1])):
                    c = loaded_map[1][cn]
                    if c[0] == mapTile[0] and c[1] == mapTile[1]:
                        if c[2] != 0:
                            sel = nobuild
                            sel.set_alpha(200)
                        break
        
    else:
        sel = seldef
        sel.set_alpha(255)
        for cn in range(len(loaded_map[1])):
                    c = loaded_map[1][cn]
                    if c[0] == mapTile[0] and c[1] == mapTile[1]:
                        if c[2] != 0:
                            sel.set_alpha(130)
                        break

    gridSize = (loaded_map[0][0]-1, loaded_map[0][1]-1)
    # Display
    window.fill(BLACK)

    '''for x in range(0, gridSize[0]*32+1, 32):
        for y in range(0, gridSize[1]*32+1, 32):
            toblit = test
            tileimg = mapmanager.getTile(loaded_map[1], x, y)
            toblit = pygame.image.load(tileimg)
            blitted = window.blit(toblit, (x+camera['x'], y+camera['y']))
            if blitted.collidepoint(m) and not theSidebar.collidepoint(m):
                selectedTile = window.blit(sel, (x+camera['x'], y+camera['y']))
                selectTile = (x+camera['x'], y+camera['y'])
                mapTile = (x,y)'''

    for tile in loaded_map[1]:
        x = tile[0]*32
        y = tile[1]*32
        #ms = time.time()
        toblit = mapmanager.builds[tile[2]]
        # print(1000*(time.time()-ms))
        #if tile[2] >= 3 and tile[2] <= 9: 
        window.blit(test, (x+camera['x'], y+camera['y']))
        blitted = window.blit(toblit, (x+camera['x'], y+camera['y']))
        if blitted.collidepoint(m) and not (theSidebar.collidepoint(m) or resourcedisplay.collidepoint(m) or scrbut.collidepoint(m) or savemap.collidepoint(m)):
            selectedTile = window.blit(sel, (x+camera['x'], y+camera['y']))
            selectTile = (x+camera['x'], y+camera['y'])
            mapTile = (x/32,y/32)

    if build and buildclick != 0 and selectedTile != None:
        for cn in range(len(loaded_map[1])):
                    c = loaded_map[1][cn]
                    if c[0] == mapTile[0] and c[1] == mapTile[1]:
                        if c[2] != 0:
                            # Tried to build on top of building
                            nobuilderror = False
                        break
        cost = None
        if buildclick < 0 and not nobuilderror:
            cost = Building.buildingCost({"steel" : 0, "wood" : 0, "stone": 0, "food" : 0})
        if buildclick == 1 and nobuilderror:
            cost = House.HouseBuilding().cost
        if buildclick == 2 and nobuilderror:
            cost = Bakery.BakeryBuilding().cost
        if buildclick >= 3 and buildclick <= 8 and nobuilderror:
            cost = Road.RoadBuilding().cost
        if buildclick == 9 and nobuilderror:
            cost = Tree.TreeBuilding().cost
        if cost != None and (nobuilderror and ((cost.steel <= steel and cost.stone <= stone and cost.wood <= wood and cost.food <= foodAmount)) or (not nobuilderror and buildclick < 0)):
            print(((cost.steel, cost.wood, cost.stone),(steel,wood,stone)))
            steel -= cost.steel
            stone -= cost.stone
            wood -= cost.wood
            foodAmount -= cost.food
            for cn in range(len(loaded_map[1])):
                c = loaded_map[1][cn]
                if c[0] == mapTile[0] and c[1] == mapTile[1]:
                    print(loaded_map[1][cn][2])
                    if buildclick < 0:
                        loaded_map[1][cn][2] = 0
                    else:
                        loaded_map[1][cn][2] = buildclick
                    print(loaded_map[1][cn][2])
                    break
        else:
            if not nobuilderror and buildclick > 0:
                print("Built ontop of building") # User attempted to build on top of an existing building
            elif nobuilderror:
                print("Not enough resources") # Not enough resources to build or clicked on grass with bulldozer
    for person in persons:
        print(person)
        window.blit(persona, ((person[0]*32)+camera['x'], (person[1]*32)+camera['y']))
    theSidebar = window.blit(sidebar, (width-160, 0))
    if sandboxenabled:
        sandbox = window.blit(sandboxi, (width-33,height-33))
    resourcedisplay = window.blit(resourcebar, (0,0))
    savemap = window.blit(savebutton, (1, 1+resourcebaroffset))
    arrowup = window.blit(arrowupimg, (width-74-43+20, 30))
    building = window.blit(iconmanager.buildings[arrownum+1], (width-74-43, 30+61))
    building2 = window.blit(iconmanager.buildings[arrownum+2], (width-74-43, 30+46+15+61))
    building3 = window.blit(iconmanager.buildings[arrownum+3], (width-74-43, 30+46+46+15+15+61))
    building4 = window.blit(iconmanager.buildings[arrownum+4], (width-74-43, 30+46+46+46+15+15+15+61))
    building5 = window.blit(iconmanager.buildings[arrownum+5], (width-74-43, 30+46+46+46+46+15+15+15+15+61))
    xbutton = window.blit(xbuttoni, (width-74-43, height-(46+30)))
    arrowdown = window.blit(arrowdownimg, (width-74-43+20, 30+46+46+46+46+15+15+15+15+61+61))
    scrbut = window.blit(pygame.transform.scale2x(scrimg), (1,height-32-1))
    destroy = window.blit(bulldoze, (width-16-160-32, 1+resourcebaroffset))
    window.blit(food, (6,4))
    window.blit(stoner, (73,4))
    window.blit(woodr, (73+67,4))
    window.blit(steelr, (73+67+67,4))
    #print(type(number.stringified(stone)))
    window.blit(resource.render(number.stringified(foodAmount), True, (0,0,0)), (40, 8))
    window.blit(resource.render(number.stringified(stone), True, (0,0,0)), (36+73, 8))
    window.blit(resource.render(number.stringified(wood), True, (0,0,0)), (73+67+36, 8))
    window.blit(resource.render(number.stringified(steel), True, (0,0,0)), (36+73+67+63, 8))
    # Display basic information
    window.blit(arial.render(infoText, False, (164, 47, 22)), (139,1+resourcebaroffset))
    pygame.display.update()
    
    mousep = m
    if not fpscapon: # Limit fps
        clock.tick()
    else:
        clock.tick(fpscap)
    fps = math.floor(clock.get_fps())
pygame.quit()
sys.exit()
