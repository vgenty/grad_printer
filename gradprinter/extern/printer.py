import os, subprocess

class Printer():

    def __init__(self):
        self.name = 'Printer'
    def __str__(self):
        return 'The printers name is:',self.name

    def send(self,location,filename,doublesided,landscape,copies,page_start,page_end):

        # print "page_start:",page_start
        # print "page_end:",page_end
        # print "type: ",type(page_start)
        # print "type: ",type(page_end)
        
        options  = ''
        options += '-# %s ' % copies

        if doublesided:
            options += '-o Duplex=DuplexNoTumble '

        if landscape:
            options += '-o landscape'
        
        if page_start is not None and page_end is not None:
            try:
                if int(page_end) > int(page_start):
                    options += '-o page-ranges=' + str(page_start) + '-' + str(page_end)
            except:
                options += ''
            
        location += filename

        if not os.path.exists(location):
            raise Exception('File does not exist?')
        
        r = subprocess.check_output("lpr %s -P grad_printer %s" % (options,location),shell=True)
        d = subprocess.check_output("rm -rf %s" % location,shell=True)
        
        return r
