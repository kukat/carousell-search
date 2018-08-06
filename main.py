import processing
import time
from myconfigurations import ITEMS, FREQUENCY
import arrow
import slackclient as robot

if __name__ == "__main__":
    starttime = time.time()

    while True:
        try:
            for idx, i in enumerate(ITEMS):
                try:
                    processing.find_stuff(idx, i)
                except Exception as e:
                    robot.post_message("ERROR: %s" % e)
            print("END CYCLE %s" % arrow.now().format('DD/MM/YYYY HH:MM'))
        except KeyboardInterrupt:
            print ("Interrupt")
            sys.exit(1)
        # time.sleep(600)
        time.sleep(FREQUENCY - ((time.time() - starttime) % FREQUENCY))

