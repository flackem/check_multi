======= submit_service.cmd =======

	:::perl
	command [ procs ] = check_procs
	command [ users ] = check_users -w 10 -c 20
	eval [ SUBMIT_hostname ] = \
	        if ("$HOSTNAME$" eq "") { \
	                print "HOSTNAME not defined\n"; \
	                exit 3; \
	        }
	eval [ SUBMIT_tmpfile ] = \
	        if (! defined($ENV{NAGIOS_SUBMIT_tmpfile})) { \
	                $ENV{NAGIOS_SUBMIT_tmpfile}="/tmp/submit_services.$$"; \
	        } \
	        return $ENV{NAGIOS_SUBMIT_tmpfile};
	eval [ SUBMIT_cmdfile ] = \
	        if (! defined($ENV{NAGIOS_SUBMIT_cmdfile})) { \
	                $ENV{NAGIOS_SUBMIT_cmdfile}="/usr/local/nagios/var/rw/nagios.cmd"; \
	        } \
	        if (! -w "$ENV{NAGIOS_SUBMIT_cmdfile}") { \
	                print "Cannot write to Nagios cmdfile $ENV{NAGIOS_SUBMIT_cmdfile}\n"; \
	                exit 3; \
	        } \
	        return "$ENV{NAGIOS_SUBMIT_cmdfile}";
	eval [ SUBMIT_create_service_file ] = \
	        if (!open(SUBMIT,">$SUBMIT_tmpfile$")) { \
	                print "Error opening $SUBMIT_tmpfile$:$?\n"; \
	                exit 3; \
	        } \
	        for (my $i=1; $i <= keys %cmds; $i++) { \
	                next if ($cmds{$i}{name}=~/^SUBMIT/); \
	                printf SUBMIT "[%d] PROCESS_SERVICE_CHECK_RESULT;%s;%s;%s;%s\n", \
	                        time,\
	                        "$HOSTNAME$",\
	                        "$cmds{$i}{name}",\
	                        $cmds{$i}{rc},\
	                        "$cmds{$i}{output}";\
	        } \
	        close SUBMIT;
	eval [ SUBMIT_feed_services ] = \
	        if (!open(CMD,">$ENV{NAGIOS_SUBMIT_cmdfile}")) { \
	                print "Cannot open cmd file \'$ENV{NAGIOS_SUBMIT_cmdfile}\' for writing:$?"; \
	                exit 3; \
	        } \
	        printf CMD "[%d] PROCESS_FILE;%s;%s", \
	                time, \
	                "$SUBMIT_tmpfile$", \
	                1; \
	        close CMD;


### Variante 2

	:::perl
	eval [ SUBMIT_hostname ] = \
	        if ("$HOSTNAME$" eq "") { \
	                print "HOSTNAME not defined\n"; \
	                exit 3; \
	        }
	eval [ SUBMIT_tmpfile ] = \
	        if (! defined($ENV{NAGIOS_SUBMIT_tmpfile})) { \
	                $ENV{NAGIOS_SUBMIT_tmpfile}="/tmp/submit_services.".int(time/120); \
	        } \
	        return $ENV{NAGIOS_SUBMIT_tmpfile};
	eval [ SUBMIT_cmdfile ] = \
	        if (! defined($ENV{NAGIOS_SUBMIT_cmdfile})) { \
	                $ENV{NAGIOS_SUBMIT_cmdfile}="/usr/local/nagios1/var/rw/nagios.cmd"; \
	        } \
	        if (! -w "$ENV{NAGIOS_SUBMIT_cmdfile}") { \
	                print "Cannot write to Nagios cmdfile $ENV{NAGIOS_SUBMIT_cmdfile}\n"; \
	                exit 3; \
	        } \
	        return "$ENV{NAGIOS_SUBMIT_cmdfile}";
	eval [ SUBMIT_create_service_file ] = \
	        if (!open(SUBMIT,">>$SUBMIT_tmpfile$")) { \
	                print "Error opening $SUBMIT_tmpfile$:$?\n"; \
	                exit 3; \
	        } \
	        for (my $i=1; $i <= keys %cmds; $i++) { \
	                next if ($cmds{$i}{name}=~/^SUBMIT/); \
	                printf SUBMIT "[%d] PROCESS_SERVICE_CHECK_RESULT;%s;%s;%s;%s\n", \
	                        time,\
	                        "$HOSTNAME$",\
	                        "$cmds{$i}{name}",\
	                        $cmds{$i}{rc},\
	                        "$cmds{$i}{output}";\
	        } \
	        close SUBMIT;
	eval [ SUBMIT_feed_services ] = \
	        my $count=0; \
	        while ($count-- > 0) { \
	                if (!open(CMD,">$ENV{NAGIOS_SUBMIT_cmdfile}")) { \
	                        print "Cannot open cmd file \'$ENV{NAGIOS_SUBMIT_cmdfile}\' for writing:$?\n"; \
	                        sleep 1; \
	                        next; \
	                } \
	                printf CMD "[%d] PROCESS_FILE;%s;%s", \
	                        time, \
	                        "$SUBMIT_tmpfile$", \
	                        1; \
	                close CMD; \
	                sleep 1; \
	                last if (! -f "$SUBMIT_tmpfile$"); \
	        } 
	eval [ SUBMIT_feed_services ] = \
	        my @files=`find /tmp -maxdepth 1 -type f -name 'submit_services[\.]*[0-9]*' -mmin +2`; \
	        my $count=0; \
	        foreach my $file (@files) { \
	                chomp($file); \
	                if (!open(CMD,">$ENV{NAGIOS_SUBMIT_cmdfile}")) { \
	                        print STDERR "Cannot open cmd file \'$ENV{NAGIOS_SUBMIT_cmdfile}\' for writing:$?\n"; \
	                        sleep 1; \
	                        next; \
	                } \
	                printf CMD "[%d] PROCESS_FILE;%s;%s", \
	                        time, \
	                        "$file", \
	                        1; \
	                close CMD; \
	                print STDERR "File processed: $file\n"; \
	                $count++; \
	        } \
	        return $count;

