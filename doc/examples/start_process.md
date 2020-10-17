======= Restart process - check_multi as event handler =======
## Description

This is a short example for a very simple event handler. In Nagios [this is a little bit more complicated ;)](http://nagios.sourceforge.net/docs/3_0/eventhandlers.html).


The example makes use of the check_multi feature to execute child checks sequently. 
 1.  First check if a specific process is running
 2.  Evaluate the result of check 1 and restart process if its not running
 3.  Second check for the process, it checks the result of step 2. (If step 2 was not necessary, it's redundant :-)) 

Simple, isn't it?

## Call / Parameters

    check_multi -f start_process.cmd -s PROC=`<process>` -s ARGS=`<args>`


*  Parameters:
    * PROC - name of the process to monitor and restart
    * ARGS - arguments to start the process (and to distinguish it from others)

## Download

The start_proc.cmd file is available in the check_multi package or [here](http://svn.my-plugin.de/repos/check_multi/trunk/start_process).

## State evaluation

*  OK
    * if process is running

*  UNKNOWN:
    * none

*  WARNING
    * if process was NOT running and was successfully started by start_process.cmd

*  CRITICAL
    * if process was NOT running **and** start_process.cmd was not able to restart it.

## Code: start_process.cmd

	:::perl
	#
	# start_process.cmd
	#
	# (c) Matthias Flacke, 5.4.2008
	# 
	# starts process if not already started and checks result
	#
	# check_multi -f start_proc.cmd -s PROC=`<process>` -s ARGS=`<args>`
	#
	# 1. check for process
	command [ proc_before ] = check_procs -c 1: -C "$PROC$" -a "$ARGS$"
	#
	# 2. start process in background
	eeval [ start_proc ] = \
	        ( $STATE_proc_before$ != 0 ) \
	                ? ( system("$PROC$ $ARGS$ &") != 0 ) \
	                        ? "- failed: $?" \
	                        : "- done" \
	                :  "- not necessary, already running"
	#
	# 3. check process again (ok, maybe redundant ;-))
	command [ proc_after ] = check_procs -c 1: -C "$PROC$" -a "$ARGS$"
	#
	# 4. state evaluation
	state [ OK       ] = proc_before == OK     && proc_after == OK
	state [ WARNING  ] = proc_before != OK     && proc_after == OK
	state [ CRITICAL ] = start_proc =~/failed/ || proc_after == CRITICAL


## Example Output

*  nsca is *not* running - note the WARNING overall state:

	:::bash
	nagios@thinkpad:~> check_multi -f etc/start_process.cmd -s PROC=nsca -s ARGS="-c /usr/local/nagios/etc/nsca.cfg"
	WARNING - 3 plugins checked, 1 critical (proc_before), 2 ok
	[ 1] proc_before PROCS CRITICAL: 0 processes with command name 'nsca', args '-c /usr/local/nagios/etc/nsca.cfg'
	[ 2] start_proc - done
	[ 3] proc_after PROCS OK: 1 process with command name 'nsca', args '-c /usr/local/nagios/etc/nsca.cfg'


*  nsca is already running:

	:::bash
	nagios@thinkpad:~> check_multi -f etc/start_process.cmd -s PROC=nsca -s ARGS="-c /usr/local/nagios/etc/nsca.cfg"
	OK - 3 plugins checked, 3 ok
	[ 1] proc_before PROCS OK: 1 process with command name 'nsca', args '-c /usr/local/nagios/etc/nsca.cfg'
	[ 2] start_proc - not necessary, already running
	[ 3] proc_after PROCS OK: 1 process with command name 'nsca', args '-c /usr/local/nagios/etc/nsca.cfg'



