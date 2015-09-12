import os, subprocess

class Printer():

    def __init__(self):
        self.name = 'Printer'
    def __str__(self):
        return 'The printers name is:',self.name

    def send(self,location,filename):
        
        the_file = "%s%s" % (location,filename)

        if not os.path.exists(the_file):
            raise Exception('File does not exist?')

        r = subprocess.check_output("lpr -P grad_printer %s" % the_file,shell=True)
        d = subprocess.check_output("rm -rf %s" % the_file,shell=True)
        
        return r