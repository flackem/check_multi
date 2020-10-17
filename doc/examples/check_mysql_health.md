======= check_mysql_health =======


*  check_mysql_health.cmd

	:::sh
	#
	# check_mysql_health.cmd
	# collection of check_mysql_health calls (plugin of Gerhard Lausser)
	#
	# Call with following parameters:
	# check_multi -f check_mysql_health.cmd -s HOSTNAME=$HOSTNAME$ -s USERNAME=`<username>` -s PASSWORD=`<$USERn$>`
	
	command [ uptime                      ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode uptime
	command [ connection-time             ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode connection-time
	command [ threads-connected           ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode threads-connected --warning 30 --critical 5
	command [ threadcache-hitrate         ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode threadcache-hitrate
	command [ index-usage                 ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode index-usage
	command [ qcache-hitrate              ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode qcache-hitrate
	command [ qcache-lowmem-prunes        ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode qcache-lowmem-prunes
	command [ keycache-hitrate            ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode keycache-hitrate
	command [ bufferpool-hitrate          ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode bufferpool-hitrate
	command [ bufferpool-wait-free        ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode bufferpool-wait-free
	command [ log-waits                   ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode log-waits
	command [ tablecache-hitrate          ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode tablecache-hitrate
	command [ table-lock-contention       ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode table-lock-contention
	command [ slow-queries                ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode slow-queries
	command [ tmp-disk-tables             ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode tmp-disk-tables
	command [ long-running-procs          ] = check_mysql_health --hostname $HOSTNAME$ --user $USERNAME$ --password $PASSWORD$ --mode long-running-procs --warning 30 --critical 5


