import os
import sys
import subprocess
import pandas as pd
import click

def add(a, b):
    return a+b

def validate(path, interval, duration, dryrun):
    try:
        if not os.path.exists(path):
            raise ValueError("Invalid path to program")
        if not interval.isdigit() or interval == '0':
            raise ValueError("Invalid interval")
        dt = pd.Timedelta(duration)
        if dt.total_seconds() <= 0:
            raise ValueError("invalid duration")
        if int(duration) > dt.seconds:
            raise ValueError("Interval greater than duration")
    except ValueError as e:
        print(f"Error: {e}\n")
        if not dryrun:
            print("Run the script with -d flag for input validation.")
        print("Run 'schedule --help' for help")
        sys.exit()
    if (dryrun):
        click.echo("Input valid")
        sys.exit()
        

@click.command(help="""PATH should lead to a batch file to be executed.
                INTERVAL is in seconds, DURATION in ISO8601
                format (P10H11M for 10 hour and 11 minutes).""")
@click.argument('taskname')
@click.argument('path')
@click.argument('interval')
@click.argument('duration')
@click.option('-d', '--dryrun', is_flag=True, help='input validation (dry-run)')
def schedule(taskname, path, interval, duration, dryrun):
    validate(path, interval, duration, dryrun)
    dt = pd.Timedelta(duration)
    subprocess.run("schtasks /create /tn {} /tr {} /sc minute /mo {} /du {:04d}:{:02d}".format(taskname, path, interval, dt.components.hours, dt.components.minutes), shell=True, check=True)
    subprocess.run(f"schtasks /run /tn {taskname}")

if __name__ == '__main__':
    schedule()