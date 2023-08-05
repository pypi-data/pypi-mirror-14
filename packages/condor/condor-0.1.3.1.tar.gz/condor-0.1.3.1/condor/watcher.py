from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler 
import sys, time, logging
from subprocess import call

class CondorSystemEventHandler(PatternMatchingEventHandler):
	"""
	Event handler for file system changes
	"""

	def __init__(self, pattern, action):
		PatternMatchingEventHandler.__init__(self, patterns=pattern)
		if not callable(action):
			raise AttribureError("Action should be callable")
		self.action = action

	def on_modified(self, event):
		self.action(event)

class Watcher:
    """
    Test
    """

    def __init__(self, path, pattern, action, controller):
        self.action = action
        self.path = path
        self.controller = controller
        self.pattern = pattern

    def register(self):
        """
        Register self as watcher in watcher controller
        """
        self.controller.add_watcher(self)

class WatcherController:
    """
    Controller/manager for registered watchers
    """

    def __init__(self):
        self.isWatchRunning = False
        self.empty = True
        self.observer = Observer()

    def add_watcher(self, watcher: Watcher):
        """
        Adds new watcher instance into controller
        """
        self.empty = False
        if self.isWatchRunning:
            self.stop()
        event_handler = CondorSystemEventHandler(watcher.pattern, watcher.action)
        self.observer.schedule(event_handler, watcher.path, recursive=True)
        self.start()

    def is_empty(self):
        return self.empty

    def start(self):
        if not self.empty:
            self.isWatchRunning = True
            self.observer.start()

    def stop(self):
        self.isWatchRunning = False
        self.observer.stop()


