import requests, random, string, concurrent.futures
from datetime import datetime
from time import sleep

def gameInfo(id):
    r = requests.get(f'https://kahoot.it/reserve/session/{id}')
    return r

def generateCode(cleng):
    code = ''
    for i in range(cleng):
        code += random.choice(string.digits)
    return code

def gameFinder():
    sleep(0.04)
    code1 = generateCode(6)
    code2 = generateCode(7)
    rsc1 = gameInfo(code1).reason
    rsc2 = gameInfo(code2).reason
    stc1 = gameInfo(code1).status_code
    stc2 = gameInfo(code2).status_code

    if rsc1 == "OK":
        print("Working code found! -> " + code1 + f" Reason -> {rsc1}")
        time = datetime.now().strftime("%H:%M:%S")
        f = open("kcodes.txt", "a")
        f.write(f"{code1} Time -> {time}\n")
    elif stc1 == 503:
        sleep(0.5)
    else:
        pass

    if rsc2 == "OK":
        print("Working code found! -> " + code2 + f" Reason -> {rsc2}")
        time = datetime.now().strftime("%H:%M:%S")
        f = open("kcodes.txt", "a")
        f.write(f"{code2} Time -> {time}\n")
    elif stc2 == 503:
        sleep(0.5)
    else:
        pass

threads = int(input("Input the amount of threads: "))
while True:
    with concurrent.futures.ThreadPoolExecutor() as executer:
        proccs = [executer.submit(gameFinder) for _ in range(threads)]