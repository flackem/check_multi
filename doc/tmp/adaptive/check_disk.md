# check_disk

The following example shows adaptive monitoring: if a partition size is smaller than 100GB, it will be checked with -w 20% and -c 10%, otherwise the thresholds are -w 10% -c 5%.

	:::perl
	# partition size is prefetched from perfdata 
	# to set the thresholds depending on size
	eeval [ partition_size ]     = (split(/;/,`check_disk -w 1 -c 2 $PARTITION$`))[5]
	eeval [ warning_threshold ]  = ($partition_size$ < 100000) ? "20%" : "10%"
	eeval [ critical_threshold ] = ($partition_size$ < 100000) ? "10%" :  "5%"
	#
	# now run check_disk with determined thresholds
	command [ partition ]        = check_disk -w $warning_threshold$ -c $critical_threshold$ $PARTITION$


You can call the command file with the following service definition

	:::bash
	define service {
	   name                 disk_root
	   service_description  root partition
	   host_name            localhost
	   check_command        check_multi!-f disk_adaptive.cmd -s PARTITION=/
	   use                  local-service
	}`</code>`
	