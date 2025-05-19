import time
from datetime import datetime

def now():
    return datetime.now().strftime("%H:%M:%S")

def cooking_pasta():
    print(f"{now()} cooking yummy pasta")
    time.sleep(3)
    print(f"{now()} pasta done")

def making_tea():
    print(f"{now()} making chai")
    time.sleep(2)
    print(f"{now()} tea done")

def main():
    cooking_pasta()
    making_tea()

main()
