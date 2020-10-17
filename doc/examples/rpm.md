	:::perl
	#
	# rpm checker (linux)
	# Matthias Flacke, 10 / 2010
	#
	# check the last 20 rpm changes for its date
	# to determine if patching has been neglected ;)
	#
	##--- thresholds and number of rpms to check
	eval    [ WARNING_DAYS          ] = 30
	eval    [ CRITICAL_DAYS         ] = 180
	eval    [ PATCHNUMBER           ] = 20
	
	#--- number of installed rpm packages
	command   [ number_of_rpms      ] = rpm -qa | wc -l
	
	#--- list of recently installed or changed rpm packages
	command [ last_changed_rpms     ] = (echo; 
		rpm -qa --queryformat '%{installtime} %{installtime:date} %{name}-%{version}-%{release}\n' 
		| sort -nr | head -5 | sed -e 's/^[^ ]* //' )
	
	#---calculate the average age of the last patches
	eeval   [ avg_age_days_last_patches ] = 
		my $sum = 0;
		foreach my $time (`rpm -qa --queryformat '%{installtime}\n' | sort -nr | head -$PATCHNUMBER$`) {
			chomp $time;
			$sum+=$time;
		}
		my $days=sprintf "%.2f", (time-$sum/$PATCHNUMBER$)/(24*60*60);
		sprintf "%.2f | rpms=%d avgdays=%.2f;%d;%d", 
			$days, 
			$number_of_rpms$, $days, $WARNING_DAYS$, $CRITICAL_DAYS$;
	
	attribute [ avg_age_days_last_patches::WARNING  ] = ($avg_age_days_last_patches$ > $WARNING_DAYS$)
	attribute [ avg_age_days_last_patches::CRITICAL ] = ($avg_age_days_last_patches$ > $CRITICAL_DAYS$)

