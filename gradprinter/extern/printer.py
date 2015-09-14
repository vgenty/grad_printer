import os, subprocess

class Printer():

    def __init__(self):
        self.name = 'Printer'
    def __str__(self):
        return 'The printers name is:',self.name

    def send(self,location,filename,doublesided,landscape,copies):
        
        options  = ''
        options += '-# %s ' % copies

        if doublesided:
            options += '-o Duplex=DuplexNoTumble '

        if landscape:
            options += '-o landscape'

        location += filename

        if not os.path.exists(location):
            raise Exception('File does not exist?')
        
        r = subprocess.check_output("lpr %s -P grad_printer %s" % (options,location),shell=True)
        d = subprocess.check_output("rm -rf %s" % location,shell=True)

        print r
        print d
        
        return r
