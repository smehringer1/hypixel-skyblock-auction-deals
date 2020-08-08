import schedule
import threading
from db_updater import update_all_auctions, db
import time

def runThreaded(job):
    jobThread = threading.Thread(name='updateThread', target=job)
    jobThread.start()

def scheduleUpdates():
    schedule.every().minute.at(':27').do(runThreaded, update_all_auctions)
    while True:
        threadList = []
        for thread in threading.enumerate():
            threadList.append(thread.getName())
        if 'updateThread' in threadList:
            pass
        else:
            schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    scheduleUpdates()