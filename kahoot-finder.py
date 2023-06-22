import requests, random, string, concurrent.futures
from datetime import datetime
from time import sleep

class KahootGameFinder:
    def __init__(self):
        self.session = requests.Session()

    def get_game_info(self, id):
        # Send a GET request to retrieve kahoot game information
        response = self.session.get(f'https://kahoot.it/reserve/session/{id}')
        return response

    def generate_code(self, length):
        # Generate a random code of specified length
        code = ''.join(random.choice(string.digits) for _ in range(length))
        return code

    def find_game(self):
        sleep(0.04)
        code1 = self.generate_code(6)
        code2 = self.generate_code(7)
        response1 = self.get_game_info(code1)
        response2 = self.get_game_info(code2)

        if response1.reason == "OK":
            # If the first code is valid, print and store it
            print("Working code found! -> " + code1 + f" Reason -> {response1.reason}")
            time = datetime.now().strftime("%H:%M:%S")
            with open("kcodes.txt", "a") as f:
                f.write(f"{code1} Time -> {time}\n")
        elif response1.status_code == 503:
            # If the first request failed due to server error, wait for a short time
            sleep(0.5)

        if response2.reason == "OK":
            # If the second code is valid, print and store it
            print("Working code found! -> " + code2 + f" Reason -> {response2.reason}")
            time = datetime.now().strftime("%H:%M:%S")
            with open("kcodes.txt", "a") as f:
                f.write(f"{code2} Time -> {time}\n")
        elif response2.status_code == 503:
            # If the second request failed due to server error, wait for a short time
            sleep(0.5)

if __name__ == "__main__":
    threads = int(input("Input the amount of threads: "))
    game_finder = KahootGameFinder()
    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Start multiple threads to perform game finding concurrently
            processes = [executor.submit(game_finder.find_game) for _ in range(threads)]
