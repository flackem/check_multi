======= Process event handling =======

	:::perl
	command[sys_proc_cpu]=check_procs -v -u root -w 95 -c 99 --metric=CPU
	eeval [shutdown_omnivision]=\
	        if ($STATE_sys_proc_cpu$ != $OK && "$sys_proc_cpu$"=~/omv_bdc/) { \
	                `echo "/etc/init.d/STARomv stop"`; \
	        }`</code>`

	  * the first check_procs checks for processes CPU usage
	  * the second eval checks if the prior CPU check was
	    - non OK
	    - the process name omv_bdc was affected (STARomv - Omnivision)

	  * if yes: stop STARomv
	
	