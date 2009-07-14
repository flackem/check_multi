#
# start_proc.cmd
#
# (c) Matthias Flacke, 5.4.2008
# 
# starts process if not already started and checks result
#
# check_multi -f start_process.cmd -s PROC=<process> -s ARGS=<args>
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
