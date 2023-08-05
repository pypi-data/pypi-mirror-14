from condor.task import Task, TaskController
from condor.watcher import Watcher, WatcherController
from condor.utilities.condor_logger import CondorLogger
import os, sys, argparse

condor_logger = CondorLogger()

watcher_controller = WatcherController()
task_controller = TaskController(condor_logger)

parser = argparse.ArgumentParser()

tasks_names = []
arguments = []

commands_shortcuts = {
    'tasklist': '-t', 
    'arguments': '-a'
    }

def add_task_names(names):
    tasks_names.extend(names)
    print(tasks_names)

def log_error(message):
    condor_logger.log_error(message)

def log_success(message):
    condor_logger.log_success(message)

def log_warning(message):
    condor_logger.log_warning(message)

def setup(name, wdir, task):

    print("Setting up Condor for {0}".format(name))

    parser.add_argument(commands_shortcuts['tasklist'], nargs='*')
    parser.add_argument(commands_shortcuts['arguments'], nargs='*')

    parsed_arguments = vars(parser.parse_args())
    task_names = parsed_arguments['t']
    arguments = parsed_arguments['a']

    for t in task:
        print("Creating task {0}".format(t['name']) )

        task_controller.set_active_tasks(task_names)

        if t['args'] != None:
            t['args'].update({'argv' : arguments})
        else:
            t['args'] = {'argv' : arguments}
        condor_task = Task(t['name'], wdir, t['args'], t['pipe'])
        if 'watch' in t.keys() and 'action' in t.keys():
            raise AttributeError("Task should not contain both action and watchers")
        if 'actions' in t.keys():
            for action in t['actions']:
                condor_task.add_action(action)
        if 'watch' in t.keys():
            for w in t['watch']:
                watcher_path = ""
                if os.path.exists(wdir + w['path']):
                    watcher_path = wdir + w['path']
                elif os.path.exists(w['path']):
                    watcher_path = w['path']
                else:
                    condor_logger.log_warning("Could not find specified path for watcher, neither relative nor absolute: {0}".format(w['path']))
                    continue
                condor_watcher = Watcher(watcher_path, w['pattern'], w['action'], watcher_controller)
                condor_task.add_watcher(condor_watcher)
                print("Added watcher for task {0} for {1}".format(condor_task.name, condor_watcher.path + condor_watcher.pattern))
        task_controller.add_task(condor_task)

    print("Condor is set up and now running...")

    task_controller.run()

    if not watcher_controller.is_empty():
        try:
            while True:
                pass
        except KeyboardInterrupt:
            exit(0)
    else:
        # Workaround for AttributeError issue.
        # Should find another solution
        exit(0)


