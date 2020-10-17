## Examples

*Under construction*  
 This example section is kind of a construction site at the moment. In the next weeks I subsequently will add plenty of examples how check_multi can be used practically.


It does not mean that the examples are non functional ^_^ 

*Call for examples*   
If you have an example which you like to share with other people, just provide me all needed information and I will publish it under this section.
You don't know how to contact me? Have a look on the [contact page](contact).

#### stable 0.20

The [stable 0.20 and the new development versions (since SVN222)](download) contain a new directory structure and some example files under sample-config. Each example published here will also be added to the sample-config directory.

### Distributed service checks

*  [Details, code, output examples - see here](blog/2009/distributed_service_checks_with_check_multi)
This example shows how a particular service could be monitored from several sites, hosts.

And all within one generic reusable check where you only have to define:
 1.  the service command to be run
 2.  the list of hosts
 3.  the thresholds for the combined check 

### Nagiostats

*  [Details, code, output examples - see here.](examples/nagiostats.md) 
[Nagiostats](examples/nagiostats.md) is the check_multi version of monitoring Nagios itself.
It contains two major parts: alarming and performance data.

 
You will be able to get aware of all short term problems of your Nagios server. And you can identify long term performance issues with the performance graphs provided by [PNP](http://www.pnp4nagios.org/pnp/start).


### Network interface settings

*  [Details, code, output examples - see here.](examples/network_interface.md) 
[Network interface monitoring](examples/network_interface.md) in this example is not meant as a monitoring of the throughput during runtime. It's instead a monitoring if all hardware settings are correct:
 1.  Is the interface speed at least ''100Mbit''?
 2.  Is it set to ''full duplex''?
 3.  Autonegotiation is also displayed, but not monitored

### Start process - event handler

*  [Details, code, output examples - see here.](examples/start_process.md) 

[projects:check_multi:examples:start_process](examples/start_process.md) is a very simple event handler to check and restart processes.


Note that check_multi will visualize the whole process: 
 1.  Check if the process is running before: green or red
 2.  Restart of the process if necessary: the RC depends on the process startup
 3.  Final check of the process again: green or red
 4. 