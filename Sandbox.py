import pygame, sys, image, number
from SaveInfoSteve import get, updateFile

pygame.init()

isRunning = True

resource = pygame.font.SysFont("Arial", 18)

window = pygame.display.set_mode((256,256), pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption("Resource Manipulator")

def buttonClick():
    pygame.mixer.music.set_volume(0.24)
    pygame.mixer.music.load("sounds\\buttonclick.mp3")
    pygame.mixer.music.play()


saveinfo1 = ""
saveinfo = ""
with open("sand.box", "r") as file:
    saveinfo1 = "maps\\" + file.readlines()[0]
#print(saveinfo1)
with open(saveinfo1, "r") as file:
    saveinfo = file.readlines()

steel = int(get(saveinfo, "steel"))
wood = int(get(saveinfo, "wood"))
stone = int(get(saveinfo, "stone"))
foodAmount = int(get(saveinfo, "food"))

camera = {'x' : int(get(saveinfo, "cx")), 'y' : int(get(saveinfo, "cy"))}

while isRunning:

    window.fill((255,255,255))
    
    foodb = window.blit(image.food, (16,32))
    stoneb = window.blit(image.stoner, (16,64))
    woodb = window.blit(image.woodr, (16,96))
    steelb = window.blit(image.steelr, (16,128))
    

    window.blit(resource.render(number.stringified(foodAmount), True, (0,0,0)), (56, 32+6))
    window.blit(resource.render(number.stringified(stone), True, (0,0,0)), (56, 64+6))
    window.blit(resource.render(number.stringified(wood), True, (0,0,0)), (56, 96+6))
    window.blit(resource.render(number.stringified(steel), True, (0,0,0)), (56, 128+6))

    resetFood = window.blit(image.resetresources, (56+128, 32+6))
    resetStone = window.blit(image.resetresources, (56+128, 64+6))
    resetWood = window.blit(image.resetresources, (56+128, 96+6))
    resetSteel = window.blit(image.resetresources, (56+128, 128+6))

    update = window.blit(image.updateresources, (256-131, 256-35))
    currentSaveInfo = ["steel:" + str(steel), "wood:" + str(wood), "stone:" + str(stone), "food:" + str(foodAmount), "cx:" + str(camera['x']), "cy:" + str(camera['y'])]
    m = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left
            if foodb.collidepoint(m):
                foodAmount += 999999
                buttonClick()
            elif steelb.collidepoint(m):
                steel += 999999
                buttonClick()
            elif stoneb.collidepoint(m):
                stone += 999999
                buttonClick()
            elif woodb.collidepoint(m):
                wood += 999999
                buttonClick()
            elif update.collidepoint(m):
                updateFile(currentSaveInfo, saveinfo1[5:])
                isRunning = False
            elif resetFood.collidepoint(m):
                foodAmount = 0
                buttonClick()
            elif resetStone.collidepoint(m):
                stone = 0
                buttonClick()
            elif resetWood.collidepoint(m):
                wood = 0
                buttonClick()
            elif resetSteel.collidepoint(m):
                steel = 0
                buttonClick()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Middle
            print(m)
    pygame.display.update()

import main
pygame.quit()
sys.exit()
