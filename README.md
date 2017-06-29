# OfflineLab
### Remote device configurator and collector: 

Report the state of a network topology.

 - A test case defines a particular configuration of the network (for each device: credentias + configuration commands) for which you want to collect the network state.    
 - The program reads commands from test case yaml files and executes them remotely on the devices to set a particular situation, and then for each device (yaml file with the name of the device) it reads the commands that will collect inf.
 - If your network changes its state overtime with the same configurations, then you need to recollect inf. after defined periods of time.
 - For each command for each device, the results are saved into a file and an XML file is built with all inf. about testcases, testruns and result file names.
 - The xml file is read by a flash application to show the offline status of the topology under each of the test run of every test case.

For now it supports Cisco IOS/IOU/IOSv and *nix systems, more to come.

Example of Cisco device command file: IOU-cmd.yaml

    # YAML
    IOU1:
      - device: cisco
      - ip: 192.168.0.201
      - login: admin
      - password: cisco
      - enablepassword: 
      - sleep:  0
      - sh ip cef vrf CustomerA
      - sh ip cef vrf CustomerA detail
      - sh ip vrf interfaces CustomerA
      - sh ip protocols vrf CustomerA
      - sh ip route vrf CustomerA
      - sh ip cef vrf CustomerB
    ...

Example of Linux device command file: PC1-cmd.yaml

    # YAML
    PC4:
      - device: linux
      - ip: 172.17.0.4
      - login: root
      - password: gns3vpc
      - enablepassword:
      - sleep:  0
      - uname -a
      - lsb-release -a
      - ping -c3 100.5.0.5
      - traceroute 100.5.0.5
      - ip -4 route show
      - ip -6 route show
      - ip -6 a
      - ifconfig
      - ip -6 neighbor show
      - cat /proc/net/if_inet6
      - sysctl -a
      - free mto
    ...

Example of test case configuration file for a Cisco device: case1.yaml

    # YAML
    R4:
      - ip: 192.168.0.204
      - login: admin
      - password: cisco
      - enablepassword: cisco
      - sleep: 10
      - conf t
      - interface e0/0
      - sh
    R1:
      - ip: 192.168.0.201
      - login: admin
      - password: cisco
      - enablepassword: cisco
      - sleep: 10
      - conf t
      - interface e0/0
      - sh


An example of deployment:

python offlinelab.py

    INFO:main: **** Test run 1 started ****
    INFO:main: **** Case 1 collecting device states ****
    INFO:paramiko.transport:Connected (version 2.0, client Cisco-1.25)
    INFO:paramiko.transport:Authentication (password) successful!
    INFO:basessh.cisco:paraSsh: sh run DONE Output File ==> ./output/C1_TR1_IT1_Internet_sh_run
    INFO:paramiko.transport:Connected (version 2.0, client Cisco-1.25)
    INFO:paramiko.transport:Authentication (password) successful!
    ...
    INFO:basessh.cisco:paraSsh: sh run DONE Output File ==> ./output/C1_TR1_IT1_IOU44_sh_run
    INFO:main: **** Test run 1 COMPLETED SUCCESSFULLY ****
    INFO:main: **** Case 1 collecting device states COMPLETED SUCCESSFULLY ****
    INFO:main:XML report built successfully

And the resulting xml file: http://hpnouri.free.fr/ospfalle2/mycombos.xml

Here is a link to the final outcome: OSPF topology offline lab http://hpnouri.free.fr/ospfalle2/offlinelabv1.swf

![screenshot](http://hpnouri.free.fr/Selection_360.jpg)
