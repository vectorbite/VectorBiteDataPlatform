Start the scheduler as a Linux service (upstart)

To install the scheduler as a permanent daemon on Linux (w/ Upstart), put the following into /etc/init/web2py-scheduler.conf, 
assuming your web2py instance is installed in <user>'s home directory, running as <user>, with app <myapp>, on network interface eth0.

description "web2py task scheduler"
start on (local-filesystems and net-device-up IFACE=eth0)
stop on shutdown
respawn limit 8 60 # Give up if restart occurs 8 times in 60 seconds.
exec sudo -u <user> python /home/<user>/web2py/web2py.py -K <myapp>
respawn
You can then start/stop/restart/check status of the daemon with:

sudo start web2py-scheduler
sudo stop web2py-scheduler
sudo restart web2py-scheduler
sudo status web2py-scheduler

Notes

Remember to call db.commit() at the end of every task if it involves inserts/updates to the database. 
web2py commits by default at the end of a successful action but the scheduler tasks are not actions.

Start a worker: 

cd '/home/matthew/PycharmProjects/vectorbite/web2py' 
matthew@matthew-ThinkPad-X240:~/PycharmProjects/vectorbite/web2py$ python web2py.py -K VectorBiteDataPlatform 
web2py Web Framework
Created by Massimo Di Pierro, Copyright 2007-2019
Version 2.17.2-stable+timestamp.2018.10.06.18.54.02
Database drivers available: sqlite3, psycopg2, pyodbc, pymysql, imaplib
starting single-scheduler for "VectorBiteDataPlatform".