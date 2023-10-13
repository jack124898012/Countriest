import pygame, sys

pygame.init()

options = open("game.options", "r")
temp = options.readlines()
options.close()
options = temp
del temp
for option in range(len(options)):
    options[option] = options[option].replace("\n", "")

def getOption(option):
    if "NO.OPTION" in option: return
    for o in options:
        if option + ": " in o:
            return o.replace(option + ": ", "")

def setOption(option, value):
    if "NO.OPTION" in option: return
    for o in range(len(options)):
        if option + ": " in options[o]:
            options[o] = option + ": " + value
            break
    # update options file
    with open("game.options", "w") as of:
        of.writelines(options)
        of.close()
