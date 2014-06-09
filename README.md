# ipmitool.py

ipmitool.py is a command line utility to run and gather output from
large number of consoles. It uses the ipmi module that abstracts
the interaction with the ipmitool utility.

[ipmitool](http://ipmitool.sourceforge.net) utility is required to be installed

## Features

- The ipmi module uses subprocess in Linux to communicate with ipmitool.
Solaris ipmitool does not support passing the password on the command line. So, it 
uses expect if the Solaris Platform is detected.

- Threaded to execute the commands in parallel

- Collated output makes it easy to understand the status of large number of hosts

## Installing

    pip install ipmitool
    
This will install ipmitool.py in your path.

e.g. :
    $ ipmitool.py -f console_list.txt status
    Password: 
    Chassis Power is on -- [6] app322-console.prod, app323-console.prod, app324-console.prod, app325-console.prod, app326-console.prod, app327-console.prod
