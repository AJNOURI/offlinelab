#!/usr/bin/env python
import yaml
import pexpect
import paramiko
import multiprocessing
import logging
from xml.dom.minidom import Document
import time

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
            logging.debug('telnet()- ip: ' + self.ip)
            logging.debug('telnet()- login: ' + self.login)
            logging.debug('telnet()- password: ' + self.passwd)
            logging.debug('telnet()- telnetport: ' + str(self.telnetport))
            logging.debug('telnet()- tout: ' + str(self.tout))

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
        logging.info('Successful authentication to host ' + self.ip)

    def paraSsh(self):

        for cmdi in self.cmdlist:
            sshobj = paramiko.SSHClient()
            sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshobj.connect(self.ip, username=self.login, password=self.passwd, allow_agent=False, look_for_keys=False)
            stdin, stdout, stderr=sshobj.exec_command(cmdi)

            if self.flog:
                precommand = cmdi.replace(':', '_')
                precommand = precommand.replace('.', '_')
                precommand = precommand.replace('/', '_')
                filename = 'C' + str(self.ci+1) + '_TR' + str(self.testrun) + '_IT'\
                        + str(self.iteration) + '_' + self.hostname + '_' + precommand
                filename = filename.replace(' ', '_')
                file=open(filename, "w")
                for line in stdout.readlines():
                    file.write(line.strip('\r\n')+'\r\n')
                file.close()
                return filename
                print 'paraSsh: ', cmdi, ' DONE',' Output File ==> ', filename
            else:
                return
            sshobj.close()


    def sendCmds(self):

        logging.debug('sendCmds()- hostname : ' + self.hostname)
        logging.debug('sendCmds()- flog : ' + str(self.flog))

        if self.flog:
            logging.debug('sendCmds()- file logging enabled ')
        else:
            logging.debug('sendCmds()- file logging disabled ')

        for cmdi in self.cmdlist:
            logging.debug('sendCmds()- cmdi: ' + cmdi)
            self.child.sendline(cmdi)
            self.child.expect(['.*#.*'])

            if self.flog:

                logging.debug('sendCmds()- Logging command result to file...')
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

                logging.debug(self.ip + ': ' + cmdi + ' done...')
        # Close the socket after executing the list of commands
        self.child.close()
        logging.debug('\n ### sendCmds()- All commands for host ' +
                    self.hostname + ': ' + self.ip + ' Successfully executed\n\n')



def remoteDev(cmdfile, flg=False, timeout=300):

    stream = open(cmdfile)
    rdata = yaml.load(stream)
    logging.debug('\n\n\n### remoteDev()- File ' + cmdfile)
    if rdata:
        for key, value in rdata.iteritems():
            cmdlist = []
            #print key.strip('\r\n')
            hostname = key.strip('\r\n')
            #logging.debug(value)

            #logging.debug('ip: ' + value[0]['ip'])
            ip = value[0]['ip']

            #logging.debug('login: ' + value[1]['login'])
            login = value[1]['login']

            #logging.debug('password: ' + value[2]['password'])
            password = value[2]['password']

            #logging.debug('sleep: ' + str(value[3]['sleep']))
            sleep = value[3]['sleep']
            for cmd in value[4:len(value)+1]:
                #print cmd
                cmdlist.append(cmd)
            print cmdlist
            conn = Connect(ip, hostname, login, password, cmdlist, ci=1, flog=flg, tout=timeout)
            # para_ssh: a single command
            rcmdfile = conn.paraSsh()
            logging.info('Sleeping : ' + str(sleep) + ' seconds... (remoteDev)')
            time.sleep(sleep)
    else:
        logging.debug('File ' + cmdfile + ' empty')


