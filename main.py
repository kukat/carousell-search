import sys

import helpers
import processing
import time
from myconfigurations import ITEMS, FREQUENCY, FREQUENCY_SLOW, DELAY_START, DELAY_STOP
import schedule


def job_delay_alter(inFrequency):
    global frequency
    frequency = inFrequency
    helpers.postMessage("JOB UPDATED")


if __name__ == "__main__":
    starttime = time.time()
    frequency = FREQUENCY
    schedule.every().day.at(DELAY_START).do(job_delay_alter, FREQUENCY_SLOW)
    schedule.every().day.at(DELAY_STOP).do(job_delay_alter, FREQUENCY)

    while True:
        schedule.run_pending()
        try:
            for idx, i in enumerate(ITEMS):
                try:
                    processing.find_stuff(idx, i)
                except Exception as e:
                    type, fname, lineno = helpers.getFormattedException()
                    message = helpers.multiplyEmoji(":x:", 3) + "ERROR: {} \n{} {} {}".format(e, type, fname, lineno)
                    print(message)
                    helpers.postMessage(message)
            print("END CYCLE %s" % time.ctime())
        except KeyboardInterrupt:
            print("Interrupt")
            sys.exit(1)
        time.sleep(frequency - ((time.time() - starttime) % frequency))
