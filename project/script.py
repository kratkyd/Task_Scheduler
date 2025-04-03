import os
import sys
import subprocess
import pandas as pd
import click

class Task:
    def __init__(self, taskname, path, interval, duration, dryrun):
        self.taskname = taskname
        self.path = path
        self.interval = interval
        self.duration = duration
        self.dryrun = dryrun

    def validate(self):
        try:
            if not os.path.exists(self.path):
                print(self.path)
                raise ValueError("Invalid path to program")
            if not self.interval.isdigit() or self.interval == '0':
                raise ValueError("Invalid interval")
            dt = pd.Timedelta(self.duration)
            if dt.total_seconds() <= 0:
                raise ValueError("invalid duration")
            if int(self.interval) > dt.seconds:
                raise ValueError("Interval greater than duration")
        except ValueError as e:
            print(f"Error: {e}\n")
            if not self.dryrun:
                print("Run the script with -d flag for input validation.")
            print("Run 'schedule --help' for help")
            return False
        return True
    
    def create_task(self):
        dt = pd.Timedelta(self.duration)
        subprocess.run("schtasks /create /tn {} /tr {} /sc minute /mo {} /du {:04d}:{:02d}".format(self.taskname,\
                     self.path, self.interval, dt.components.hours, dt.components.minutes), shell=True, check=True)
        subprocess.run(f"schtasks /run /tn {self.taskname}")

@click.command(help="""PATH should lead to a batch file to be executed.
                INTERVAL is in seconds, DURATION in ISO8601
                format (P10H11M for 10 hour and 11 minutes).""")
@click.argument('taskname')
@click.argument('path')
@click.argument('interval')
@click.argument('duration')
@click.option('-d', '--dryrun', is_flag=True, help='input validation (dry-run)')
def schedule(taskname, path, interval, duration, dryrun):
    task = Task(taskname, path, interval, duration, dryrun)
    if task.validate():
        print("Valid input")
    else:
        sys.exit()
    if not dryrun:
        task.create_task()

if __name__ == '__main__':
    schedule()