# ipmitool.py

ipmitool.py is a command line utility to run ipmitools command 
and gather the output from large number of consoles. It uses the 
ipmi module that abstracts the interaction with the ipmitool utility.

[ipmitool](http://ipmitool.sourceforge.net) is required to be installed

## Features

- The ipmi module uses subprocess in Linux to communicate with ipmitool.
Solaris ipmitool does not support passing the password on the command line. So, it 
uses expect if the Solaris Platform is detected.

- Threaded to execute the commands in parallel

- Collated output makes it easy to understand the status and output of large number of hosts

## Installing

    pip install ipmitool
    
This will install ipmitool.py in your path.

e.g. :

    $ ipmitool.py -f console_list.txt status
    Password: 
    Chassis Power is on -- [6] app322-console.prod, app323-console.prod, app324-console.prod, app325-console.prod, app326-console.prod, app327-console.prod

## Extending

The ipmitool.py utlity is used for chassis power changes and status. But you can write your own on top of the ipmi module :

e.g. :

    >>> ipmi = ipmitool(console, password)
    >>> ipmi.execute("chassis status")
    >>> ipmi.execute("chassis status")
    0
    >>> print ipmi.output
    System Power         : on
    Power Overload       : false
    Power Interlock      : inactive
    Main Power Fault     : false
    Power Control Fault  : false
    ...
