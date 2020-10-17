======= Network interface settings =======

### Description

This example checks the correct setup of the default gateway interface on a Linux server. 

*  The interface name is taken from the default route (''/proc/net/route'')

*  ''ethtool'' is used to get information about the interface settings. Since ''ethtool'' needs root permissions ''sudo'' will be the door openener. Please adjust the ''sudo'' settings -> ''visudo''.

### Call / Parameters

    check_multi -f interface.cmd


*  no Parameters

**Note**: this command file autodetects the default gateway for a host. If you want to monitor multiple devices of a host, you can either build a loop over all interfaces or add a parameter ''-s IF=`<interface>`.

### Child checks

*  Link: is the link up?

*  Speed: interface speed (10,100,1000,10000) 

*  Duplex: Full duplex or half duplex

*  Autoneg: on or off

### State evaluation

*  UNKNOWN: empty result or ''ethtool'' error

*  WARNING: Speed < 100 or duplex not full

*  CRITICAL: Link not up
### Code: interface.cmd

	:::sh
	#
	# network_interface.cmd (adopted for Linux hosts)
	#
	# Copyright (c) 2008-2009 Matthias Flacke (matthias.flacke at gmx.de)
	#
	# Matthias Flacke, 20.01.2008
	
	# determine def_gw interface from /proc/net/route
	command [ def_gw  ] = awk '$2 == "00000000" {print $1}' /proc/net/route | head -1
	
	# get ethtool output and store it in temporary file
	command [ ethtool ] = sudo /sbin/ethtool $def_gw$ > /tmp/if_$def_gw$.txt
	                      && echo OK
	
	# get interface settings using ethtool
	command [ link    ] = awk '/Link detected:/    {print $3}' /tmp/if_$def_gw$.txt 
	command [ speed   ] = awk '/Speed:/            {print $2}' /tmp/if_$def_gw$.txt 
	command [ duplex  ] = awk '/Duplex:/           {print $2}' /tmp/if_$def_gw$.txt 
	command [ autoneg ] = awk '/Auto-negotiation:/ {print $2}' /tmp/if_$def_gw$.txt 
	
	# evaluate results
	state   [ UNKNOWN ] =  "$def_gw$"  eq "" || ethtool != OK
	state   [ WARNING ] = ("$speed$"   && "$speed$"   !~ /100/)   ||
	                      ("$duplex$"  && "$duplex$"  !~ /FULL/i)
	state   [ CRITICAL] =  "$link$"    && "$link$"    eq "no"


### Example output

{{:check_multi:examples:network_interface.png|network interface settings}}
