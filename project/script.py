import os
import sys
import subprocess
import pandas as pd
import click

class Task:
    # Task object is created for each task (to be created) or dry run
    def __init__(self, taskname: str, path: str, interval: str, duration: str, dryrun: bool):
        self.taskname = taskname
        self.path = path
        self.interval = interval
        self.duration = duration
        self.dryrun = dryrun

    # Returns True if inputs are valid, prints errors and returns false if not
    def validate(self):
        try:
            # Does path exist
            if not os.path.exists(self.path):
                print(self.path)
                raise ValueError("Invalid path to program")
            # Is the interval valid
            if not self.interval.isdigit() or self.interval == '0':
                raise ValueError("Invalid interval")
            # Is the duration valid
            dt = pd.Timedelta(self.duration)
            if dt.total_seconds() <= 0:
                raise ValueError("invalid duration")
            # Is duration greater or equal to interval (otherwise the program just runs immediately)
            if int(self.interval)*60 > dt.total_seconds():
                raise ValueError("Interval greater than duration")
        except ValueError as e:
            print(f"Error: {e}\n")
            if not self.dryrun:
                print("Run the script with -d flag for input validation.")
            print("Run 'schedule --help' for help")
            return False
        return True
    
    # Creates task in Windows task manager based on it's variables
    def create_task(self):
        dt = pd.Timedelta(self.duration)
        subprocess.run("schtasks /create /tn {} /tr {} /sc minute /mo {} /du {:04d}:{:02d}".format(self.taskname,\
                     self.path, self.interval, dt.components.hours, dt.components.minutes), check=True)
        subprocess.run(f"schtasks /run /tn {self.taskname}")


# Click funciton defining the "schedule" command in setup.py
# Creates Task object and creates a task if -d flag was not used
@click.command(help="""PATH should lead to a batch file to be executed.
                INTERVAL is in seconds, DURATION in ISO8601
                format (P10H11M for 10 hour and 11 minutes).""")
@click.argument('taskname')
@click.argument('path')
@click.argument('interval')
@click.argument('duration')
@click.option('-d', '--dryrun', is_flag=True, help='input validation (dry-run)')
def schedule(taskname: str, path: str, interval: str, duration: str, dryrun: bool):
    task = Task(taskname, path, interval, duration, dryrun)
    if task.validate():
        print("Valid input")
    else:
        sys.exit()
    if not dryrun:
        task.create_task()


# main in case script.py is run directly
if __name__ == '__main__':
    schedule()