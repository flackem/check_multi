======= How to ... =======

... do this, how to do that? 
Or: Everything You Always Wanted to Know About *check_multi* But Were Afraid to Ask :-D

The following snippets and small examples should give you an impression how different monitoring jobs can be done with *check_multi*.


If you have other examples or comments or improvements, feel free to send them to me.



======= ... determine where my check_multi check runs better. Either on the Nagios server, or on the remote server? =======
Basically there are two approaches to use check_multi. I've made up a small table to compare them:
 |                                                                                                                                                                                                                                                                                                                                                                  | 1. check_multi running on Nagios server | 2. check_multi running on client server | 
 |                                                                                                                                                                                                                                                                                                                                                                  | ---------------------------------------- | --------------------------------------- | 
 | |{{:check_multi:multi_on_nagios.png|}} |{{:check_multi:nagios_check_multi.png|}} |                                                                                                                                                                                                                                                                              
 | Basic concept | check_multi runs on the Nagios server and accesses the remote server with each child check independently |check_multi is running on the remote server (here called client) and executes the child services locally |                                                                                                                            
 | Resources

Load | 1. The Nagios servers bears most of the execution load and needs more power.\\ 2. The footstep on the client server is not that big.  | 1. The load on the Nagios server is very small.\\ 2. The major work is done on the client, therefore it takes the burden of its own monitoring. |                                                    
 | Network | The network load is higher, especially with SSH transport mechanisms the effort is much higher due to multiple authentication steps. | The network load is very small, there is only one connection to trigger the startup and transport back the results over the network. |                                                                         
 | Configuration | Configuration is easily accessible, there is no need to distribute configuration files | The remote client needs configuration to be distributed and updated. |                                                                                                                                                                                 
 | Plugins | As for configuration, its sufficient to provide plugins only on the central Nagios server. | Plugins have to be distributed and updated. |                                                                                                                                                                                                           
 | Local monitoring vs.

remote monitoring | There are particular local checks like disk monitoring, which need high efforts to be run remotely | Every remote check can also be run as a local check. That means vice versa, that all checks can be run from the remote server, even checks for network services. A plus in terms of homogenity of monitoring |

======= ...evaluate data within check_multi =======
For a flexible interpretation of any data in *check_multi* you can use the builtin state evaluation. It internally works with perl *eval* and therefore is extremely flexible.

See the following SNMP example as a simple introduction:

	:::perl
	# sensor.cmd
	#
	# (c) Matthias Flacke
	# 30.12.2007
	#
	# Flexible interpretation of smmp results
	command [ sensor ] = /usr/bin/snmpget -v 1 -c $COMMUNITY$ -Oqv $HOSTNAME$ XYZ-MIB::Sensor.0
	
	state [ UNKNOWN  ] =  $sensor$  !~ /[4627859]/
	state [ OK       ] = ( $sensor$ == 4 || $sensor$ == 6 )
	state [ WARNING  ] = ( $sensor$ == 2 || $sensor$ == 7 || $sensor$ == 8 )
	state [ CRITICAl ] = ( $sensor$ == 5 || $sensor$ == 9 )
	


**Note:** This example really does not more than standard plugin also can do. But it shows how fast and reliable you can do develop such a SNMP plugin with *check_multi*. And if you want to change a value afterwards, you does not need to bother a developer. Any administrator can do this.

*check_multi* can do all the standard tasks like a normal plugin: 

*  gathering data

*  validating the retrieved data (-> state [ UNKNOWN ] line)

*  evaluating the different results against rules 

======= ... monitor devices which are not up and online all the time =======

**Offline hosts**: The following snippet shows how to monitor devices (clients, printers...) which are not up and running all the time. And the major task is *not* to check if they're online or running. \\
But you want to check several attributes like patch levels, disk fillup etc. and do this when the hosts are up.


During the other time the state of the hosts remains OK and a message is shown that the host is offline.

	:::perl
	#
	# check_client.cmd
	# 08.02.2009
	#
	# (c) Matthias Flacke
	#
	# Call:  check_multi -f check_client.cmd -s HOSTNAME=`<host>`
	command [ ping     ] = check_icmp -H $HOSTNAME$ -w 500,5% -c 1000,10%
	eval    [ offline  ] = if ($STATE_ping$ != $OK) { print "Host offline"; exit 0; }
	
	# execute these commands only if host online
	command [ command1 ]  = ...
	command [ command2 ]  = ...
	


