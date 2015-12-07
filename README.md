# offlinelab
### Remote device configurator and collector: 

Report the state of a network topology.

 - Read commands from test case yaml files and execute them remotely on the devices, this is repeated for each test run. Defining testruns is useful if the state of your network behavior evolves during time.
 - Read commands (status and parameters) from device yaml files, execute them remotely, collect the result and report testcases>testruns>devices>commands to an XML an xml file.
 - The xml file is read by a flash application to show the offline status of the topology under each of the test run of every test case.

For now it supports Cisco IOS/IOU and *nix systems, more to come.


![Screenshot](http://hpnouri.free.fr/Selection_360.jpg)
