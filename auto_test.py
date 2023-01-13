import sys
import time
import os
import datetime
from watchdog.events import PatternMatchingEventHandler


if sys.platform == "win32":
    from watchdog.observers.polling import PollingObserver as Observer
else:
    from watchdog.observers import Observer


class AutoTest(PatternMatchingEventHandler):
    patterns = ["*.py"]

    def process(self, event):
        print('\n\nauto test start', os.getcwd())
        print(datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p"))
        os.system('pytest')

    def on_modified(self, event):
        self.process(event)


def main():
    path = '.'
    observer = Observer()
    observer.schedule(AutoTest(), path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()

