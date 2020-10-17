======= HA-Linux (Heartbeat 2) =======
*Thanks to Michael Schwartzkopff for his comprehensive Cluster course!*

### heartbeat.cmd

	
	#
	# heartbeat.cmd
	#
	# Copyright (c) 2008 Matthias Flacke (matthias.flacke at gmx.de)
	#
	# This program is free software; you can redistribute it and/or
	# modify it under the terms of the GNU General Public License
	# as published by the Free Software Foundation; either version 2
	# of the License, or (at your option) any later version.
	#
	# This program is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
	#
	# You should have received a copy of the GNU General Public License
	# along with this program; if not, write to the Free Software
	# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
	#
	#
	# heartbeat.cmd dynamically determines the heartbeat ressources and checks its state
	#
	# Call: check_multi -f heartbeat.cmd -r 15 -s HOSTADDRESS=$HOSTADDRESS$ -s COMMUNITY=`<community string>`
	#
	
	command [ nodes_total   ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.1.1.0
	command [ nodes_alive   ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.1.2.0
	command [ nresources    ] = snmpwalk -v 1 -c $COMMUNITY$ -mALL $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.2 | wc -l
	
	eeval   [ get_resources ] = \
	        for (my $i=1; $i<=$nresources$; $i++) { \
	                my $name=`snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.2.$i`; \
	                chomp $name; $name=~s/[^A-Za-z0-9_-]*//g; \
	                parse_lines("command [ $name       ] = check_multi -r 15 " . \
	                        "-x 'command [ name        ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.2.$i' " . \
	                        "-x 'command [ type        ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.3.$i' " . \
	                        "-x 'command [ state       ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.5.$i' " . \
	                        "-x 'command [ failcount   ] = check_snmp -H $HOSTADDRESS$ -l \"\" -o .1.3.6.1.4.1.4682.8.1.7.$i -w 0 -c 0:1' " . \
	                        "-x 'command [ managed     ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.6.$i' " . \
	                        "-x 'command [ node        ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.4.$i' " . \
	                        "-x 'command [ parent      ] = snmpget  -v 1 -c $COMMUNITY$ -Ovqa $HOSTADDRESS$ 1.3.6.1.4.1.4682.8.1.8.$i' "); \
	        } \
	        $i; 

