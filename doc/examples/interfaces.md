======= Interfaces =======
Up to now just an exercise ;-)
### if.cmd

	
	#
	# (c) Matthias Flacke, 12/2009
	#
	# call: check_multi -f if.cmd -s HOSTNAME=localhost
	# needs a running snmpd on the mentioned host
	#
	snmp [ number_of_interfaces  ] = $HOSTNAME$:1.3.6.1.2.1.2.1.0
	#command [ test ] = snmpwalk -v 1 -O qnv  -c public $HOSTNAME$ .1.3.6.1.2.1.2.2.1.1
	eval [ get_indices           ] = @{$opt{set}{indices}}=split(/\n/,`snmpwalk -v 1 -O qnv  -c $opt{set}{snmp_community} $HOSTNAME$ .1.3.6.1.2.1.2.2.1.1`);
	eval [ loop_over_interfaces  ] = 
	        for (my $i=0; $i < $number_of_interfaces$; $i++) {
	                my $index=$opt{set}{indices}[$i];
	                my $name=`snmpget -v 1 -O qnv -c $opt{set}{snmp_community} $HOSTNAME$ 1.3.6.1.2.1.2.2.1.2.$index`; chomp $name;
	                parse_lines("command [ $name       ] = check_multi -r 1 -s empty_output_is_unknown=0 " .
	                        "-x 'snmp [ name        ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.2.$index' " .
	                        "-x 'snmp [ mtu         ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.4.$index' " .
	                        "-x 'snmp [ speed       ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.5.$index' " .
	                        "-x 'snmp [ mac         ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.6.$index' " .
	                        "-x 'snmp [ state       ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.7.$index' "
	                        );
	        }

