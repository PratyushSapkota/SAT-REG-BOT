FILENAME = "log.txt"

def writeLine(line):
    with open(FILENAME, "a") as file:
        file.write(f"{line} \n")

def clearFile():
    with open(FILENAME, "w") as file:
        file.write("")

def getFileName():
    return FILENAME