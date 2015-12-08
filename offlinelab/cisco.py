#!/usr/bin/env python
import yaml
import paramiko
import logging
from xml.dom.minidom import Document
import time

class connect(object):
    def __init__(self,ci,cmdfile,flog=False,testrun=1,iteration=1,sleep=0,tout=30):

        self.ci = ci
        self.flog = flog
        self.testrun = testrun
        self.iteration = iteration
        self.sleep = sleep
        self.tout = tout

        try:
            stream = open(cmdfile)
            self.rdata = yaml.load(stream)
            logging.debug('\n\n\n### Reading CMD list from YAML file: ' + cmdfile)
            self.cmdlist = []
            if self.rdata:
                for key, value in self.rdata.iteritems():

                    #print key.strip('\r\n')
                    self.hostname = key.strip('\r\n')
                    #logging.debug(value)

                    #logging.debug('device: ' + value[0]['ip'])
                    self.device = value[0]['device']


                    #logging.debug('ip: ' + value[1]['ip'])
                    self.ip = value[1]['ip']

                    #logging.debug('login: ' + value[1]['login'])
                    self.login = value[2]['login']

                    #logging.debug('password: ' + value[2]['password'])
                    self.passwd = value[3]['password']

                    self.enpasswd = value[4]['enablepassword']

                    #logging.debug('sleep: ' + str(value[3]['sleep']))
                    self.sleep = value[5]['sleep']
                    for cmd in value[6:len(value)+1]:
                        #print cmd
                        self.cmdlist.append(cmd)
            else:
                    logging.debug('File ',cmdfile,' is empty')
        except IOError:
            logger.error('File ',cmdfile,' NOT found')
            sys.exit(0)


    def paraSsh(self):
        if self.rdata:
            MAXBYTES = 999999
            outlist = []

            sshobj = paramiko.SSHClient()
            sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshobj.connect(self.ip, username=self.login, password=self.passwd)
            sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            channel = sshobj.invoke_shell()

            channel.send('en\n')
            time.sleep(1)
            resp = channel.recv(MAXBYTES)
            #print ('en :', resp)

            if (self.device.lower() == 'cisco') and (self.enpasswd):
                    # enablepassword
                    channel.send(self.enpasswd + '\n')
                    time.sleep(1)
                    resp = channel.recv(MAXBYTES)
                    # entire command output once
                    channel.send('terminal length 0\n')
                    time.sleep(1)

            for cmdi in self.cmdlist:
                # first we enable!
                channel.send(cmdi + '\n')
                time.sleep(10)
                cmdoutput = channel.recv(MAXBYTES)
                #print cmdoutput

                if self.flog:
                    precommand = cmdi.replace(':', '_')
                    precommand = precommand.replace('.', '_')
                    precommand = precommand.replace('/', '_')
                    filename = 'C' + str(self.ci) + '_TR' + str(self.testrun) + '_IT'\
                            + str(self.iteration) + '_' + self.hostname + '_' + precommand
                    filename = filename.replace(' ', '_')

                    with open(filename, 'w') as file_out:
                        file_out.write(cmdoutput)
                    file_out.close()
                    print 'paraSsh: ', cmdi, ' DONE',' Output File ==> ', filename
                    outlist.append({filename:cmdi})
                else:
                    print cmdoutput

                logging.debug(cmdi, ': Sent successfully')

            if self.device.lower() == 'cisco':
                channel.send('do no terminal pager 0\n')

            time.sleep(1)

            sshobj.close()
            time.sleep(self.sleep)

            return outlist

