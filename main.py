import processing
import time
from myconfigurations import ITEMS, FREQUENCY


if __name__ == "__main__":
    starttime = time.time()

    while True:
        try:
            for i in ITEMS:
                processing.find_stuff(i)
        except KeyboardInterrupt:
            print ("Interrupt")
            sys.exit(1)
        # time.sleep(600)
        time.sleep(FREQUENCY - ((time.time() - starttime) % FREQUENCY))

