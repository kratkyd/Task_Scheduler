import os
import sys
import argparse
import subprocess
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('taskname')
    parser.add_argument('path', help='global path to chosen .bat file')
    parser.add_argument('interval', help='repeat interval in minutes')
    parser.add_argument('duration', help='duration in ISO8601 format ("P10H11M" for 10 hour 11 minutes)')
    parser.add_argument('-d', action='store_true') #dry-run flag
    args = vars(parser.parse_args())

    try:
        if not os.path.exists(args['path']):
            raise ValueError("Invalid path to program")
        
        if not sys.argv[3].isdigit() or sys.argv[3] == '0':
            raise ValueError("Invalid interval")

        dt = pd.Timedelta(sys.argv[4])

        if dt.total_seconds() <= 0:
            raise ValueError("invalid duration")

        if int(sys.argv[3]) > dt.seconds:
            raise ValueError("Interval greater than duration") #program would run only once?
    except ValueError as e:
        print(f"Error: {e}")
        print('Run the script with -d flag for input validation, run "script -h" for help')
        input()
        sys.exit()

    if (args['d'] == True):
        print("Valid input")
        input()
        sys.exit()
    #if (len(sys.argv) != 5):
        #raise ValueError("Invalid arguments\n Expected: script <Task name> <Path to program> <Interval in minutes> <Duration in ISO8601>")
    # try:
    #     pass
    # except ValueError as e:
    #     pass
    # except TypeError:
    #     pass
        #subprocess.run("schtasks /create /tn {0}_start /tr {1} /st /sc once".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]), shell=True, check=True)

        # dt = pd.Timedelta(sys.argv[4]) defined above
    print("{:04d}:{:02d}".format(dt.components.hours, dt.components.minutes))
        #subprocess.run("schtasks /create /tn {0} /tr {1} /sc minute /mo {2} /du {3}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]), shell=True, check=True)
        #subprocess.run("schtasks /run /tn {0}".format(sys.argv[1]))
    input()