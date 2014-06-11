"""
Abstracts interaction with the ipmitool utilty 
by providing a pythonic interface
"""
import sys, pexpect, subprocess

class ipmitool(object):
    """Provides an interface to run the ipmitool commmands via 
    subprocess or expect depending on the platform. ipmitool 
    on sunos does not support passing the console password on 
    command line
    e.g :
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
    """
    
    def __init__(self, console, password, username='root'):
        """
        :param console: The console dns or ip address
        :param password: Console password
        :param username: Console username
        """
        
        self.console = console
        self.username = username
        self.password = password
        self.output = None
        self.error = None
        self.status = None
        
        self._ipmitool_path = self._get_ipmitool_path()
        if not self._ipmitool_path:
             raise IOError("Failed to locate ipmitool command!")
        
        self.args = ['-I', 'lanplus', '-H', self.console, '-U', self.username]
        
        if sys.platform == 'linux2':
            self.args.extend(['-P', self.password])
            self.method = self._subprocess_method
                    
        elif sys.platform == 'sunos5':
            self.method = self._expect_method
        
        else:
            self.method = self._expect_method
    
    def execute(self, command):
        """Primary method to execute ipmitool commands
        :param command: ipmi command to execute, str or list
        
        e.g.
        > ipmi = ipmitool('consolename.prod', 'secretpass')
        > ipmi.execute('chassis status')
        >
        """
        if isinstance(command, str):
            self.method(command.split())
        elif isinstance(command, list):
            self.method(command)
        else:
            raise TypeError("command should be either a string or list type")

        if self.error:
            raise IPMIError(self.error)
        else:
            return self.status
        
    def _subprocess_method(self, command):
        """Use the subprocess module to execute ipmitool commands
        and and set status
        """
        p = subprocess.Popen([self._ipmitool_path] + self.args + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output, self.error = p.communicate()
        self.status = p.returncode
        
    def _expect_method(self, command):
        """Use the expect module to execute ipmitool commands
        and set status
        """
        child = pexpect.spawn(self._ipmitool_path, self.args + command)
        
        i = child.expect([pexpect.TIMEOUT, 'Password: '], timeout=10)
        if i == 0:
            child.terminate()
            self.error = 'ipmitool command timed out'
            self.status = 1
        else:
            child.sendline(self.password)
        
        i = child.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=10)
        if i == 0:
            child.terminate()
            self.error = 'ipmitool command timed out'
            self.status = 1
        else:
            if child.exitstatus:
                self.error = child.before
            else:
                self.output = child.before

            self.status = child.exitstatus
            child.close()

    def _get_ipmitool_path(self, cmd='ipmitool'):
        """Get full path to the ipmitool command using the unix
        `which` command
        """
        p = subprocess.Popen(["which", cmd], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)                
        out, err =  p.communicate()
        return out.strip()
    
    
    # common ipmi command shortcuts
    def chassis_on(self):
        self.execute("chassis power on")
    
    def chassis_off(self):
        self.execute("chassis power off")
        
    def chassis_reboot(self):
        self.execute("chassis power reset")
    
    def chassis_status(self):
        self.execute("chassis power status")
        
    def boot_to_pxe(self):
        self.execute("chassis bootdev pxe")
    
    def boot_to_disk(self):
        self.execute("chassis bootdev disk")


class IPMIError(Exception):
    """IPMI exception"""
    pass     
    
    
        
