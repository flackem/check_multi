## Check client only if client is UP and RUNNING


	:::perl
	#
	# check_client.cmd
	#
	# Matthias.Flacke@gmx.de, 8.02.2009
	#
	# to be prepended to other checks for client hosts which are not UP all the time
	# 1. when $HOSTNAME$ is down, a message is printed and nothing is checked
	# 2. when $HOSTNAME$ is up, the following checks are executed
	#
	# Call:  check_multi -f check_client.cmd -f other.cmd -s HOSTNAME=`<hostname>`
	#
	command [ ping     ] = check_icmp -H $HOSTNAME$ -w 500,5% -c 1000,10%
	eval    [ offline  ] = if ($STATE_ping$ != $OK) { print "Host $HOSTNAME$ offline"; exit 0; }


