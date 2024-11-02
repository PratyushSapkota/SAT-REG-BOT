import asyncio
FILENAME = "log.txt"
from datetime import datetime, timedelta

def check():
    global lastCheck
    dateNow = datetime.now()
    delta = dateNow - lastCheck
    if delta >= timedelta(days=1):
        clearFile()
        lastCheck = datetime.now()

def initilizeFile():
    global lastCheck 
    lastCheck = datetime.now()
    clearFile()
    
def writeLine(line):
    with open(FILENAME, "a") as file:
        file.write(f"{line} \n")

def clearFile():
    print(f"File Cleared")
    writeLine(f"File Cleared")
    with open(FILENAME, "w") as file:
        file.write("")
    

def getFileName():
    return FILENAME
