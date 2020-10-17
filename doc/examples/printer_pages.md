[See this thread in nagios-portal.de](http://www.nagios-portal.org/wbb/index.php?page=Thread&postID=161147#post161147)

	:::perl
	#
	# save_offline.cmd
	# checks host / service for reachability and returns saved value, if available.
	# 
	# Call:  check_multi -f save_offline.cmd -s HOSTNAME=`<host>` -s COMMAND="check_xyz..."
	
	#--- parameters
	eval    [ command   ] = if (! "$COMMAND$") { print "No command specified\n"; exit $UNKNOWN; } else { "$COMMAND$" }
	eval    [ savedir   ] = "/var/tmp/save_offline";
	eval    [ createdir ] = mkdir "$savedir$" if (! -d "$savedir$");
	eval    [ savefile  ] = (split(' ',`echo "$HOSTNAME$ $COMMAND$" | md5sum`))[0];
	
	#--- check if host / service should be available
	command [ is_online ] = check_icmp -H $HOSTNAME$ -w 500,5% -c 1000,10%
	#command [ is_online ] = check_tcp -H $HOSTNAME$ -p $PORT$
	
	#--- if the host / service is offline: 
	#--- provide saved state and bail out gracefully
	eval    [ if_offline ] = 
		if ($STATE_is_online$ != $OK) {
			if (-f "$savedir$/$savefile$") {
				open(SAVE,"$savedir$/$savefile$") || die "Cannot open $savedir$/$savefile$:$!";
				print "Saved result: ",<SAVE>,"\n";	
				close SAVE;
			} else {
				print "I'm sorry, Dave, there is no saved result available\n";
			}
			exit $OK;
		}
	
	#--- execution of the passed COMMAND
	command [ exec_command ] = $COMMAND$
	
	#--- save result
	eval    [ save_value ] =
		#--- alter this regex for your needs, saved data between ()
		if (qq($exec_command$)=~/[A-Za-z- ]*(.*)/) {
			open (SAVE, ">$savedir$/$savefile$") || die "Cannot open $savedir$/$savefile$ for writing:$!";
			print SAVE $1;
			close SAVE or die "Cannot write to $savedir$/$savefile$:$!";
		}
	
	#--- provide original output instead of check_multi one
	output [ HEAD ] = qq($exec_command$)

