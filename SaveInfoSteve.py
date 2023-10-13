def get(saveinfo, line):
    for l in saveinfo:
        if line + ":" in l: return l[len(line)+1:]


def updateFile(newinfo, name):
    file = open("maps\\" + name, "w")
    print("SAVED " + str(newinfo) + " TO maps\\" + name)
    for line in newinfo: file.write(line + "\n")
    file.close()
