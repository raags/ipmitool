import sys, unittest
from ipmi import ipmitool, IPMIError

class testIPMItool(unittest.TestCase):
    console = 'console.internal.network'
    password = 'password'

    def testSubprocessMethod(self):
        sys.platform = 'linux2'
        ipmi = ipmitool(self.console, self.password)
        ipmi.execute('chassis status')

        print "Output : {0}".format(ipmi.output)
        print "Status : {0}".format(ipmi.status)
        print "Error  : {0}".format(ipmi.error)
        
        self.assertEqual(ipmi.status, 0)
        
    def testExpectMethod(self):
        sys.platform  = 'sunos5'
        ipmi = ipmitool(self.console, self.password)
        ipmi.execute('chassis status')
        
        print "Output : {0}".format(ipmi.output)
        print "Status : {0}".format(ipmi.status)
        print "Error  : {0}".format(ipmi.error)
        
        self.assertEqual(ipmi.status, None)
        
    def testFailure(self):
        sys.platform  = 'linux2'
        ipmi = ipmitool(self.console+'df', self.password)
        self.assertRaises(IPMIError, ipmi.execute, 'chassis status')

if __name__ == '__main__':
    unittest.main()
