__author__ = 'AJ NOURI'
__date__ = ''
__license__ = ''
__version__ = ''
__email__ = 'ajn.bin@gmail.com'

#!/usr/bin/env python
import yaml
import pexpect
import multiprocessing
import logging
from xml.dom.minidom import Document
import time
from input import *

"""
TODO:
- add pause between test cases.
- optional command arguments:
    - set cases
        - possibility to set cases without collecting device states or xml output
    - collect states (file log)
        - xml output file (always with file log)
- memorise last finished test, continue from there
- manual collect for each case without applying casefiles

- manual including cases
- manual including initializing state

TRBL:
- flog=300, issue with order of parameters in the function.
- python logging from inside functions

"""


logger = logging.getLogger(__name__)

### Manually set logging level
arg1 = '-vv'
if arg1 == '-v':
    logging.basicConfig(level=logging.INFO)
elif arg1 == '-vv':
    logging.basicConfig(level=logging.DEBUG)

handler = logging.FileHandler('initconfig.log', mode='w')
# Create logging format and bind to root logging object
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
# Create file handler
handler.setFormatter(formatter)
logger.addHandler(handler)
#arg2 = '-m'
arg2 = ''
arg3 = '-c'
#arg3 = ''
arg4 = '-x'
#arg4 = ''
arg5 = '-s'
#arg5 = ''
if arg3 == '-c':
    filelog = True
else:
    filelog = False

class Connect(object):
    def __init__(self, ip=" ", hostname=" ", login="admin", passwd="cisco", \
                 cmdlist=[], ci=1, flog=False, \
                 telnetport="23", sshport="22", \
                 testrun=1, iteration=1, tout=30):

        self.ip = str(ip)
        self.hostname = str(hostname)
        self.login = str(login)
        self.passwd = str(passwd)
        self.cmdlist = cmdlist
        self.ci = ci
        self.flog = flog
        self.telnetport = str(telnetport)
        self.sshport = str(sshport)
        self.testrun = testrun
        self.iteration = iteration
        self.tout = tout


    def telnet(self):
        try:
            logger.debug('telnet()- ip: ' + self.ip)
            logger.debug('telnet()- login: ' + self.login)
            logger.debug('telnet()- password: ' + self.passwd)
            logger.debug('telnet()- telnetport: ' + str(self.telnetport))
            logger.debug('telnet()- tout: ' + str(self.tout))

            self.child = pexpect.spawn('telnet', ['-l', self.login, self.ip, self.telnetport], self.tout)
            self.child.setecho(False) # Turn off tty echo
            index = self.child.expect(['.*sername.*'])
            self.child.sendline(self.login)
            index = self.child.expect(['.*assword.*'])
            # privileged level
            self.child.sendline(self.passwd)
            self.child.expect(['.*#.*'])

            # No terminal length limit
            self.child.sendline('term len 0')
            self.child.expect(['.*#.*'])
        except pexpect.ExceptionPexpect, e:
            print e.value
        logger.info('Successful authentication to host ' + self.ip)


    def sendCmds(self):

        logger.debug('sendCmds()- hostname : ' + self.hostname)
        logger.debug('sendCmds()- flog : ' + str(self.flog))

        if self.flog:
            logger.debug('sendCmds()- file logging enabled ')
        else:
            logger.debug('sendCmds()- file logging disabled ')

        for cmdi in self.cmdlist:
            logger.debug('sendCmds()- cmdi: ' + cmdi)
            self.child.sendline(cmdi)
            self.child.expect(['.*#.*'])

            if self.flog:

                logger.debug('sendCmds()- Logging command result to file...')
                precommand = cmdi.replace(':', '_')
                precommand = precommand.replace('.', '_')
                precommand = precommand.replace('/', '_')
                filename = 'C' + str(self.ci+1) + '_TR' + str(self.testrun) + '_IT'\
                           + str(self.iteration) + '_' + self.hostname + '_' + precommand
                filename = filename.replace(' ', '_')
                fout = file(filename, 'w')
                fout.write(self.child.after)
                self.child.logfile = fout
                return filename
            else:

                logger.debug(self.ip + ': ' + cmdi + ' done...')
        # Close the socket after executing the list of commands
        self.child.close()
        logger.debug('\n ### sendCmds()- All commands for host ' +
                     self.hostname + ': ' + self.ip + ' Successfully executed\n\n')



def remoteDev(cmdfile, flg=False, timeout=300):

    stream = open(cmdfile)
    rdata = yaml.load(stream)
    logger.debug('\n\n\n### remoteDev()- File ' + cmdfile)
    if rdata:
        for key, value in rdata.iteritems():
            cmdlist = []
            #print key.strip('\r\n')
            hostname = key.strip('\r\n')
            #logger.debug(value)

            #logger.debug('ip: ' + value[0]['ip'])
            ip = value[0]['ip']

            #logger.debug('login: ' + value[1]['login'])
            login = value[1]['login']

            #logger.debug('password: ' + value[2]['password'])
            password = value[2]['password']

            #logger.debug('sleep: ' + str(value[3]['sleep']))
            sleep = value[3]['sleep']
            for cmd in value[4:len(value)+1]:
                #print cmd
                cmdlist.append(cmd)
            print cmdlist
            conn = Connect(ip, hostname, login, password, cmdlist, ci=1, flog=flg, tout=timeout)
            conn.telnet()
            conn.sendCmds()

            logger.info('Sleeping : ' + str(sleep) + ' seconds... (remoteDev)')
            time.sleep(sleep)
    else:
        logger.debug('File ' + cmdfile + ' empty')


# There is 14 test cases:
if arg4 == '-x':
    # *** XML ***
    # Create the minidom document
    doc = Document()
    # Create the <lab> base element
    lab = doc.createElement("lab")
    doc.appendChild(lab)
    # *** XML ***

for casei in xrange(0,len(caselist)):

    if arg2 == '-m':
        ### manually start test cases (controlled through CLI argument -m)
        ctn = raw_input('Press any Key to continue with the case '+ str(casei+1) + ' ... ')


    casetext = caselist[casei]['case']
    casefile = caselist[casei]['casefile'] + '.yaml'

    if arg5 == '-s':
        # Initialize device prior to each test case
        #
        logger.info(' **** Initialization started... ****')
        remoteDev("init.yaml", flg=False)
        logger.info(' **** Initialization COMPLETED ****')

        # Apply state conditions for each test case
        #
        logger.info(' **** Applying Case ' + str(casei+1) + ' conditions **** ')
        remoteDev(casefile, flg=False)
        logger.info(' **** Case ' + str(casei+1) + ' conditions APPLIED SUCCESSFULLY **** ')


    if arg3 == '-c':    # collecting file

        if arg4 == '-x':  # xml file output

            # *** XML ***
            # Create case element
            case = doc.createElement("mycase")
            case.setAttribute("id", str(casei+1))
            lab.appendChild(case)
            # Create a casename element
            casename = doc.createElement("casename")
            case.appendChild(casename)
            # Give the casename elemenet text
            casetext = caselist[casei]['case']
            casenametext = doc.createTextNode(casetext)
            casename.appendChild(casenametext)
            # Create a topo element
            topo = doc.createElement("topo")
            case.appendChild(topo)
            # Give the topo elemenet text
            topotext = doc.createTextNode("top"+str(casei+1)+".jpg")
            topo.appendChild(topotext)
            # *** XML ***


        for trun in xrange(1, testruns+1):

            logger.info(' **** Test run ' + str(trun) + ' started **** ')

            if arg4 == '-x':
                # *** XML ***
                # Create testrun element
                testrun = doc.createElement("testrun")
                testrun.setAttribute("id", str(trun))
                case.appendChild(testrun)
                # *** XML ***

            logger.info(' **** Case ' + str(casei+1) + ' collecting device states **** ')
            for collectfile in collectfilelist:
                print collectfile
                #remoteDev(collectfile, flog=True)

                try:
                    stream = open(collectfile)
                    rdata = yaml.load(stream)

                    for key, value in rdata.iteritems():
                        cmdlist = []
                        hostname = key.strip('\r\n')
                        logger.debug('hostname: ' + hostname)
                        logger.debug('ip: ' + value[0]['ip'])
                        ip = value[0]['ip']
                        logger.debug('login: ' + value[1]['login'])
                        login = value[1]['login']
                        logger.debug('password: ' + value[2]['password'])
                        password = value[2]['password']
                        logger.debug('sleep: ' + str(value[3]['sleep']))
                        sleep = value[3]['sleep']

                        if arg4 == '-x':
                            # *** XML ***
                            # Create router element
                            router = doc.createElement("router")
                            router.setAttribute("id", hostname)
                            testrun.appendChild(router)
                            # *** XML ***

                        for cmd in value[4:len(value)+1]:
                            cmdlist = []
                            cmdlist.append(cmd)
                            conn = Connect(ip, hostname, login, password, cmdlist, ci=casei+1, flog=filelog, tout=300)
                            conn.telnet()
                            rcmdfile = conn.sendCmds()

                            logger.debug('File:  %s', rcmdfile)
                            logger.debug('Command: = %s', cmd)

                            if arg4 == '-x':
                                # *** XML ***
                                 # Create a command node tag
                                command = doc.createElement("command")
                                router.appendChild(command)
                                # Create a cmdname node tag
                                cmdname = doc.createElement("cmdname")
                                command.appendChild(cmdname)
                                # Give the cmdname node tag text
                                cmdnametext = doc.createTextNode(cmd)
                                cmdname.appendChild(cmdnametext)
                                # Create a cmdfile element
                                cmdfile = doc.createElement("cmdfile")
                                command.appendChild(cmdfile)
                                # Give the cmdfile elemenet text
                                # filename returned from cisco_telnet
                                cmdfiletext = doc.createTextNode(rcmdfile)
                                cmdfile.appendChild(cmdfiletext)
                            # *** XML ***

                except IOError:
                    logger.error('file %s-cmd.txt NOT found', collectfile)

        logger.info(' **** Test run ' + str(trun) + ' COMPLETED SUCCESSFULLY **** ')
    logger.info(' **** Case ' + str(casei+1) + ' collecting device states COMPLETED SUCCESSFULLY **** ')

if arg4 == '-x':
    # *** XML ***
    logger.debug(doc.toprettyxml(indent="  "))
    f = open('mycombos.xml', 'w')
    doc.writexml(f)
    f.close()
    logger.info('XML report built successfully')
    # *** XML ***

