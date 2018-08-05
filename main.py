import processing
import time
from myconfigurations import ITEMS, FREQUENCY


if __name__ == "__main__":
    starttime = time.time()

    while True:
        try:
            for idx, i in enumerate(ITEMS):
                processing.find_stuff(idx, i)
            print("END CYCLE")
        except KeyboardInterrupt:
            print ("Interrupt")
            sys.exit(1)
        # time.sleep(600)
        time.sleep(FREQUENCY - ((time.time() - starttime) % FREQUENCY))

