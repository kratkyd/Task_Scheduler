## Python Task Scheduler Wrapper
Python script creating tasks in Windows Task Scheduler using **_schtasks_** command. After _'pip install Task_Scheduler'_, **_schedule_** command can be used with 4 parameters:

_$schedule \<taskname\> \<path\> \<interval\> \<duration\> (-d)_

where _path_ chooses program to be run by task scheduler. _interval_ is in minutes, _duration_ in ISO8601 duration format ("P10H11M" for 10 hours 11 minutes). Optional flag _-d_ turns on dry run (program just validates input).

**_pytest_** runs prepared unit tests.

Dependencies are Pandas, Click and Pytest, which are installed when using _'pip install Task_Scheduler'_