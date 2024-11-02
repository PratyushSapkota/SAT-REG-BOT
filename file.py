import asyncio

FILENAME = "log.txt"

def writeLine(line):
    with open(FILENAME, "a") as file:
        file.write(f"{line} \n")

async def clearFile():
    while True:
        print(f"File Cleared")
        writeLine(f"File Cleared")
        with open(FILENAME, "w") as file:
            file.write("")
        asyncio.sleep(24 * 60 * 60)

def runClear():
    asyncio.create_task(clearFile())
    

def getFileName():
    return FILENAME
