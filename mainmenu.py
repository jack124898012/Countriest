import pygame,sys
from maps import mapgetter
from maps import default
import mapmanager
import generatename as mapname
import image

pygame.init()

blankbuttonw = pygame.image.load("graphics\\blankbuttonw.png")
window = pygame.display.set_mode((800, 600), pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption("Countriest")

isRunning = True

loadmap = window.blit(pygame.image.load("graphics\\loadmap.png"), (400-64, 300-16-32-16))
createmap = window.blit(pygame.image.load("graphics\\createmap.png"), (400-64, 300-22))
al = window.blit(pygame.image.load("graphics\\arrowl.png"), (400-24, 500-24))
ar = window.blit(pygame.image.load("graphics\\arrowr.png"), (400-24, 300-24))
selectmap = window.blit(pygame.image.load("graphics\\selectmap.png"), (211+128+32+24, 300-24))
menuOpen = False
load = False
sload = 0
foundmaps = []
arial = pygame.font.SysFont("Arial", 12)
arials = pygame.font.SysFont("Arial", 20)
create = False
maxsize = 100
cmapname = window.blit(blankbuttonw, (211+32+96, 300-24+32+16))
csize = 15
text = mapname.make()
createmap2 = window.blit(pygame.image.load("graphics\\createmap.png"), (400-64, 300-22-32-16))
newname = window.blit(pygame.image.load("graphics\\name.png"), (211+32+96+64, 300-24+32+16))
launch = "misc\\launch.options"

while isRunning:
    while text + ".map" in mapgetter.getMaps():
        text = mapname.make()
    m = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # ON LEFT CLICK
            if selectmap.collidepoint(m) and load:
                pygame.mixer.music.set_volume(0.24)
                pygame.mixer.music.load("sounds\\buttonclick.mp3")
                pygame.mixer.music.play()
                with open(launch, "w") as file:
                    file.write(foundmaps[sload])
                import main
                isRunning = False
            if ar.collidepoint(m) and load:
                if sload > 0: sload -= 1
            if al.collidepoint(m) and load:
                if sload < len(foundmaps)-1: sload += 1
            if ar.collidepoint(m) and create:
                if csize > 0: csize -= 1
            if al.collidepoint(m) and create:
                if csize < maxsize: csize += 1
            if not menuOpen and loadmap.collidepoint(m):
                load = True
                foundmaps = mapgetter.getMaps()
                menuOpen = True
            if newname.collidepoint(m) and create:
                text = mapname.make()
            if not menuOpen and createmap.collidepoint(m):
                menuOpen = True
                create = True
            if create and createmap2.collidepoint(m):
                mapmanager.saveMap(text + ".map", (csize, csize), default.make((csize, csize)))
                
                pygame.mixer.music.set_volume(0.24)
                pygame.mixer.music.load("sounds\\buttonclick.mp3")
                pygame.mixer.music.play()
                
                with open(launch, "w") as file:
                    file.write(text)

                with open("maps\\" + text + ".saveinfo", "w") as file:
                    file.write("stone:500\nwood:500\nfood:2000\nsteel:0\ncx:0\ncy:0")
                import main
                isRunning = False
                
            if (not menuOpen and (loadmap.collidepoint(m) or createmap.collidepoint(m))):
                pygame.mixer.music.set_volume(0.24)
                pygame.mixer.music.load("sounds\\buttonclick.mp3")
                pygame.mixer.music.play()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if al.collidepoint(m) and create and csize < maxsize-10: csize += 10
            if ar.collidepoint(m) and create and csize > 10: csize -= 10
    window.fill((0,0,0))
    m = pygame.mouse.get_pos()
    b = pygame.image.load("graphics\\gamebackground.jpg").convert()
    b.set_alpha(100)
    window.blit(b, (0,0))
    #print(text)
    if not load and not create:
        loadmap = window.blit(pygame.image.load("graphics\\loadmap.png"), (400-64, 300-16-32-16))
        createmap = window.blit(pygame.image.load("graphics\\createmap.png"), (400-64, 300-22))
        

    if load: # Load map menu
        #print(sload)
        al = window.blit(pygame.image.load("graphics\\arrowl.png"), (400-24+128, 300-24))
        ar = window.blit(pygame.image.load("graphics\\arrowr.png"), (400-128-24, 300-24))
        selmap = window.blit(pygame.image.load("graphics\\blankbutton.png"), (211+128, 300-24))
        selectmap = window.blit(pygame.image.load("graphics\\selectmap.png"), (211+128, 300+32-10))
        window.blit(arial.render(foundmaps[sload], False, (0,0,0)), (211+128+10, 300-32+10))

        if al.collidepoint(m) or ar.collidepoint(m): window.blit(image.Help().changemap, (m[0]-96, m[1]-122))
        if selmap.collidepoint(m): window.blit(image.Help().loadmapname, (m[0]-96, m[1]-122))
        if selectmap.collidepoint(m): window.blit(image.Help().loadmap, (m[0]-96, m[1]-122))
        
    if create: # Create map menu

        al = window.blit(pygame.image.load("graphics\\arrowl.png"), (400-24+128, 300-24))
        ar = window.blit(pygame.image.load("graphics\\arrowr.png"), (400-128-24, 300-24))
        size = window.blit(pygame.image.load("graphics\\sizedisplay.png"), (211+32+128, 300-24))
        window.blit(arials.render(str(csize), False, (0,0,0)), (211+32+128+10, 300-32+10))
        createmap2 = window.blit(pygame.image.load("graphics\\createmap.png"), (400-64, 300-22-32-16))
        cmapname = window.blit(pygame.image.load("graphics\\blankbutton.png"), (211+32+96, 300-24+32+16))
        newname = window.blit(pygame.image.load("graphics\\name.png"), (211+32+96+128+16, 300-24+32+16+6))
        window.blit(arial.render(text, False, (0,0,0)), (211+32+96+10, 300-24+32+16+10))


        if al.collidepoint(m): window.blit(image.Help().mapsize1, (m[0]-96, m[1]-122))
        if ar.collidepoint(m): window.blit(image.Help().mapsize2, (m[0]-96, m[1]-122))
        if newname.collidepoint(m): window.blit(image.Help().changename, (m[0]-96, m[1]-122))
        if cmapname.collidepoint(m): window.blit(image.Help().mapname, (m[0]-96, m[1]-122))
        if size.collidepoint(m): window.blit(image.Help().size, (m[0]-96, m[1]-122))
        if createmap2.collidepoint(m): window.blit(image.Help().create, (m[0]-96, m[1]-122))
        
    pygame.display.update()

pygame.quit()
sys.exit()
