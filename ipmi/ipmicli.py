from __future__ import print_function
import re, sys, site, getpass, socket, argparse, collections
from threading import Thread
from ipmi import ipmitool

# Todo: add logging
class Runner(Thread):
    """
    Build ipmitool object and run through tasks as per requested command
    """
    
    ipmi_map = { "reboot" : "chassis power reset",
                 "pxe" : "chassis bootdev pxe",
                 "fix" : "chassis bootdev cdrom",
                 "disk" : "chassis bootdev disk", 
                 "status": "chassis power status",
                 "off": "chassis power off",
                 "on": "chassis power on" }
                    
    def __init__(self, console, password, command="disk", username="root"):
        """
        :param console: The console dns or ip address
        :param command: The ipmi command to execute specified in `ipmi_map`
        :param username: Console username
        :param password: Console password
        """
        Thread.__init__(self)
        
        self.console = console   
        self.command = command
        self.username = username
        self.password = password
        
        try:
            socket.inet_aton(self.console)
            self.consoleip = socket.gethostbyname(self.console)
        except socket.error:
            try:
                self.consoleip = socket.gethostbyname(self.console)
            except socket.gaierror:
                raise NameError('Console Ip or dns name is invalid')
        
        self.error = None
        self.output = None
        self.status = None
        
    def ipmi_method(self, command):       
        """Use ipmitool to run commands with ipmi protocol
        """
        ipmi = ipmitool(self.console, self.password, self.username)
        
        if command == "reboot":
            self.ipmi_method(command="status")
            if self.output == "Chassis Power is off":
                command = "on"
        
        ipmi.execute(self.ipmi_map[command])
        
        if ipmi.status:
            self.error = ipmi.error.strip()
        else:
            self.output = ipmi.output.strip()        
        self.status = ipmi.status
        
    def run(self):
        """Start thread run here
        """
        try:
            if self.command == "pxer":
                self.ipmi_method(command="pxe")
                if self.status == 0 or self.status == None:
                    self.command = "reboot"
                else:
                    return
                    
            self.ipmi_method(self.command)
        
        except Exception as e:
            self.error = str(e)
            #raise
            

def print_report(runner_results):
    """
    Print collated report with output and errors if any
    """
    error_report = collections.defaultdict(list)
    output_report = collections.defaultdict(list)
    success_report = list()
    
    for runner_info in runner_results:
        hostname = runner_info['console']
        error = runner_info['error']
        output = runner_info['output']
        
        if error:
            error_report[error].append(hostname)
        elif output:
            output_report[output].append(hostname)
        else:
            success_report.append(hostname)
            
    if error_report:
        print("Errors : ")
        for error in error_report:
            print("{0} -- [{1}] {2}".format(error.strip(), len(error_report[error]), ", ".join(error_report[error])))
            print()
    
    if output_report:        
        for output in output_report:
            print("{0} -- [{1}] {2}".format(output, len(output_report[output]), ", ".join(output_report[output])))
    
    if success_report:
        print("Completed config on {0} hosts".format(len(success_report)))

def main():
    parser = argparse.ArgumentParser(
        description="Run ipmitool commands on consoles")
    
    group = parser.add_argument_group("Host selectors")
    group.add_argument("-H", "--host", help="Console Ip or Dns Name")
    group.add_argument("-f", "--file", help="File with list of Consoles")
    group.add_argument("-u", "--username", default='root', help="Console username to use") 
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("command", choices=["pxer", "pxe", "disk", "reboot", "off", "on", "status"], 
                        help= "pxer - set to PXE and reboot host")
    
    args = parser.parse_args()
    
    if args.file:
        try:
            host_list = open(args.file).read().split()
        except IOError as err:
            print("Error: cannot open {0} ({1})".format(hostfile, err))
            exit(1)           
    elif args.host:
        host_list = [args.host]
    else:
        parser.print_usage()
        sys.exit(1)
         
    # Confirm with user for host power changes
    if args.command == "reboot" or args.command == "off" or args.command == "pxer":
        print("Power will be changed for the following hosts: ")
        for host in host_list:
            print(host) 
        choice = raw_input("Do you want to proceed? (y/n): ")
        if not choice == "y":
            exit(1)
            
    # Get console password
    passwd = getpass.getpass()
    if not passwd:
        print("Please provide the console password")
        exit(1)
                
    runner_list = []
    for host in host_list:
        runner_thread = Runner(host, command=args.command, username=args.username, password=passwd)
        runner_thread.start()
        runner_list.append(runner_thread)
    
    runner_results = list()  
    for runner in runner_list:
        runner.join()
        runner_info = { 'console': runner.console, 'error': runner.error, 'output': runner.output }
        runner_results.append(runner_info)
    
    print_report(runner_results)


if __name__ == "__main__":
    main()



# vim: autoindent tabstop=4 expandtab smarttab shiftwidth=4 softtabstop=4 tw=0
