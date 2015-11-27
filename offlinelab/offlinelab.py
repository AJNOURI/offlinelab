#!/usr/bin/env python

import yaml
import pexpect
import multiprocessing
import logging
from xml.dom.minidom import Document
import time
from logmod import *
import cisco

__author__ = 'AJ NOURI'
__date__ = '26/11/2015'
__license__ = 'MIT'
__version__ = '0.1'
__email__ = 'ajn.bin@gmail.com'


def main():

    """
    TODO
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

    TRBL
    - flog=300, issue with order of parameters in the function.
    - python logging from inside functions
    """
    logger = logging.getLogger(__name__)
    handler = logInit(level=logging.DEBUG)
    logger.addHandler(handler)

    #arg2 = '-m'
    arg2 = ''
    arg3 = '-c'
    #arg3 = ''
    arg4 = '-x'
    #arg4 = ''
    #arg5 = '-s'
    arg5 = ''
    if arg3 == '-c':
        filelog = True
    else:
        filelog = False

    # There is 14 test cases:
    if arg4 == '-x':
        # *** XML ***
        # Create the minidom document
        doc = Document()
        # Create the <lab> base element
        lab = doc.createElement("lab")
        doc.appendChild(lab)
        # *** XML ***

    collectfilelist = [
        "IOU1-cmd.txt",
        "IOU2-cmd.txt",
        "IOU3-cmd.txt",
        "IOU4-cmd.txt",
        "IOU5-cmd.txt"
        ]

    caselist = [
        {'case': 'Case1 -Everything OK', 'casefile': 'case1'},
        {'case': 'Case2 -IOU3 e0/0 DOWN', 'casefile': 'case2'},
        {'case': 'Case3 -IOU4 e0/0 DOWN', 'casefile': 'case3'}
    ]

    testruns = 1
    iterations = 1

    for casei in xrange(0,len(caselist)):

        if arg2 == '-m':
            ### manually start test cases (controlled through CLI argument -m)
            ctn = raw_input('Press any Key to continue with the case '+ str(casei+1) + ' ... ')


        casetext = caselist[casei]['case']
        casefile = caselist[casei]['casefile'] + '.yaml'

        if arg5 == '-s':
            # Initialize device prior to each test caselist
            #
            logger.info(' **** Initialization started... ****')
            cisco.remoteDev("init.yaml", flg=False)
            logger.info(' **** Initialization COMPLETED ****')

            # Apply state conditions for each test case
            #
            logger.info(' **** Applying Case ' + str(casei+1) + ' conditions **** ')
            cisco.remoteDev(casefile, flg=False)
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
                                conn = cisco.Connect(ip, hostname, login, password, cmdlist, ci=casei+1, flog=filelog, tout=300)
                                # para_ssh: a single command
                                rcmdfile = conn.paraSsh()


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
                        logger.error('file %s NOT found', collectfile)

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

if __name__ == "__main__":
    main()

