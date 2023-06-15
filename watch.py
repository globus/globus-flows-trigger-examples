import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileTrigger:
    def __init__(self, watch_dir, patterns, FlowRunner=None):
        self.observer = Observer()
        self.watch_dir = watch_dir
        self.patterns = patterns
        self.FlowRunner = FlowRunner

    def run(self):
        print("Watcher Started\n")

        if not self.FlowRunner:
            print("No callback function defined for events.")
            print("Using system print()")
            self.FlowRunner = print

        if not os.path.isdir(self.watch_dir):
            print("Watch directory does not exist.")
            os.mkdir(self.watch_dir)
            print("Directory " + self.watch_dir + " was created")

        os.chdir(self.watch_dir)
        print(f"Monitoring: {self.watch_dir}\n")

        event_handler = Handler(self.FlowRunner, self.patterns)
        self.observer.schedule(event_handler, self.watch_dir, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Watcher stopped.")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, FlowRunner, patterns):
        super(FileSystemEventHandler).__init__()
        self.logic_function = FlowRunner
        self.patterns = patterns

    # This is the callback function for file events.
    # You can edit it to trigger at file creation, modification or deletion,
    # and have different behaviors for each.
    def on_any_event(self, event):
        if event.event_type == "created":
            if event.is_directory:
                # print("directory created")
                # self.logic_function(event.src_path)
                return None
            else:
                print(f"File created: {os.path.basename(event.src_path)}")
                for pattern in self.patterns:
                    if event.src_path.endswith(pattern):
                        print(f"File ends with {pattern}")
                        print("Starting flow...")
                        self.logic_function(event.src_path)
                        return None
        # elif (event.event_type == 'modified'):
        #     self.logic_function(event.src_path)
        #     return None
