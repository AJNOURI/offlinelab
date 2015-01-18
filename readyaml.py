__author__ = 'AJ NOURI'
__date__ = ''
__license__ = ''
__version__ = ''
__email__ = 'ajn.bin@gmail.com'

#!/usr/bin/env python
import yaml
import pexpect
import logging
from xml.dom.minidom import Document
import time

"""
TODO:
Ignore lines beginning with # commands ==> looks like enabled by default for yaml files ??
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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create file handler
handler.setFormatter(formatter)
logger.addHandler(handler)


class Connect(object):

    def __init__(self, ip=" ", hostname=" ", login="admin", passwd="cisco", \
                 cmdlist=[], ci=1, flog=False, \
                 telnetport="23", sshport="22", \
                 testrun=1, iteration=1, tout=30):

        self.ip = ip
        self.hostname = hostname
        self.login = login
        self.passwd = passwd
        self.cmdlist = cmdlist
        self.ci = ci
        self.flog = flog
        self.telnetport = telnetport
        self.sshport = sshport
        self.testrun = testrun
        self.iteration = iteration
        self.tout = tout


    def telnet(self):
        ######################### TELNET
        try:
            self.child = pexpect.spawn('telnet', ['-l', self.login, self.host, self.telnetport], self.tout)

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

        for cmdi in self.cmdlist:
            print cmdi
            self.child.sendline(cmdi)
            #logger.debug('sending command ' + cmdi + ' to ' + self.hostname + '...')
            self.child.expect(['.*#.*'])

            if self.flog:
                logger.debug('Logging command result to file...')
                precommand = cmdi.replace(':', '_')
                precommand = precommand.replace('.', '_')
                precommand = precommand.replace('/', '_')
                filename = 'C' + str(self.ci) + '_TR' + str(self.testrun) + '_IT'\
                           + str(self.iteration) + '_' + self.hostname + '_' + precommand
                filename = filename.replace(' ', '_')
                fout = file(filename, 'w')
                fout.write(self.child.after)
                self.child.logfile = fout
                self.child.close()
                return filename
            else:
                logger.debug('No file logging of  ' + cmdi)
                logger.debug(self.ip + ': ' + cmdi + ' done...')
                self.child.close()
        logger.debug('')
        logger.debug('All commands for host ' + self.hostname + ': ' + self.ip + ' Successfully executed')



def remoteDev(cmdfile, flog=False, tout=300):

    stream = open(cmdfile)
    rdata = yaml.load(stream)
    if rdata:
        for key, value in rdata.iteritems():
            cmdlist = []
            #print key.strip('\r\n')
            hostname = key.strip('\r\n')
            logger.debug(value)

            logger.debug('ip: ' + value[0]['ip'])
            ip = value[0]['ip']

            logger.debug('login: ' + value[1]['login'])
            login = value[1]['login']

            logger.debug('password: ' + value[2]['password'])
            password = value[2]['password']

            logger.debug('sleep: ' + str(value[3]['sleep']))
            sleep = value[3]['sleep']
            for cmd in value[4:len(value)+1]:
                #print cmd
                cmdlist.append(cmd)
            #print cmdlist
            conn = Connect(ip, hostname, login, password, cmdlist, flog, tout)
            conn.telnet()
            conn.sendCmds()
            logger.info('Sleeping : ' + str(sleep) + ' seconds...')
            time.sleep(sleep)
    else:
        logger.debug('File ' + cmdfile + ' empty')

collectfilelist = [
    "R1-cmd.txt"]
"""    ,
    "R2-cmd.txt",
    "R3-cmd.txt",
    "R4-cmd.txt",
    "R5-cmd.txt"
    ]
"""
caselist = [
    {'case': 'Traffic between R1 10.10.0.1 (area 123) to R5 50.10.0.5 (area0): Default interface ospf costs', 'casefile': 'case1'},
    {'case': 'Traffic from R1 10.10.0.1 (area123) to R5 50.20.0.5 (backbone) : R1 fa1/0 cost = 10, R2 fa1/2 cost = 10', 'casefile': 'case2'},
    {'case': 'Traffic from R1 10.10.0.1 (area 123) to R5 50.10.0.2 (backbone): R1 fa1/0 cost = 10, R3 fa1/2 cost = 100', 'casefile': 'case3'},
    {'case': 'Traffic from R1 10.10.0.1 (area 123) to R5 50.10.0.2 (backbone): R1 fa1/0 cost = 10, R3 fa1/2 cost = 10', 'casefile': 'case4'},
    {'case': 'Traffic from R5 50.10.0.5 (backbone) to R1 10.10.0.1 (area 123): R3 fa1/1 cost = 10', 'casefile': 'case5'},
    {'case': 'Traffic from R5 50.10.0.5 (backbone) to R1 10.10.0.1 (area 123): R3 fa1/1 cost = 10, R4 fa1/1 cost = 5', 'casefile': 'case6'},
    {'case': 'Traffic from R1 10.10.0.1 (area123) to R2 20.10.0.2 (area 123): R1 fa1/0 cost = 100', 'casefile': 'case7'},
    {'case': 'Traffic from R1 10.10.0.1 (area123) to R2 20.10.0.2 (area 123): R1-R2 link down (no inter-area route to 20.10.0.2)', 'casefile': 'case8'},
    {'case': 'Intra-area traffic from R4 40.10.0.4 (backbone) to R2 20.10.0.2 (backbone): R4 f1/1 cost = 100', 'casefile': 'case9'},
    {'case': 'Traffic from R1 10.10.0.2 (area123) to R2 20.20.0.2 (backbone): R4-R2 link down (no inter-area route to 20.20.0.2)', 'casefile': 'case10'},
    {'case': 'Traffic between two non-backbone areas. From area123 to area25: Default interface costs', 'casefile': 'case11'},
    {'case': 'Traffic generated from R2: 20.10.0.2 (area 123) to R5 50.20.0.5 (area 25): R2 fa1/2 cost = 100', 'casefile': 'case12'},
    {'case': 'R2 fa1/1 Down', 'casefile': 'case13'},
    {'case': 'R2 fa1/1 Down, R1 fa1/1 Down', 'casefile': 'case14'}
]

testruns = 1
iterations = 1

# There is 14 test cases:

# *** XML ***
# Create the minidom document
doc = Document()
# Create the <lab> base element
lab = doc.createElement("lab")
doc.appendChild(lab)
# *** XML ***

for casei in xrange(0,len(caselist)):

    # Initialize device prior to each test case
    logger.info(' **** Initialization started... ****')
    remoteDev("init.yaml", flog=False)
    logger.info(' **** Initialization COMPLETED ****')

    # Apply state conditions for each test case
    logger.info(' **** Applying Case ' + str(casei+1) + ' conditions **** ')
    casetext = caselist[casei]['case']
    casefile = caselist[casei]['casefile'] + '.yaml'
    remoteDev(casefile, flog=False)
    logger.info(' **** Case ' + str(casei+1) + ' conditions APPLIED SUCCESSFULLY **** ')

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

                    # *** XML ***
                    # Create router element
                    router = doc.createElement("router")
                    router.setAttribute("id", hostname)
                    testrun.appendChild(router)
                    # *** XML ***

                    for cmd in value[4:len(value)+1]:
                        cmdlist = []
                        cmdlist.append(cmd)
                        conn = Connect(ip, hostname, login, password, cmdlist, ci=casei+1, flog=True, tout=300)
                        conn.telnet()
                        rcmdfile = conn.sendCmds()

                        logger.debug('File:  %s', rcmdfile)
                        logger.debug('Command: = %s', cmd)

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

# *** XML ***
logger.debug(doc.toprettyxml(indent="  "))
f = open('mycombos.xml', 'w')
doc.writexml(f)
f.close()
# *** XML ***

logger.info('XML report built successfully')