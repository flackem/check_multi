======= read_services ========

Funktion to read all host-services-rc-output-long_output from status.dat

It returns hash $ref->{host}->{service}->{attribute}

	:::perl
	sub read_services {
	        my ($STATUSDAT)=@_;
	        my $result={};
	        print " DEBUG: parsing $STATUSDAT\n";
	        open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	
	        while (`<DAT>`) {
	                if (/^servicestatus\s+\{/) {
	                        my $host_name="";
	                        my $service_description="";
	                        while (`<DAT>`) {
	                                NEXT: if (/\thost_name=(.+)$/) {
	                                        $host_name=$1;
	                                } elsif (/\tservice_description=(.+)$/) {
	                                        $service_description=$1;
	                                } elsif (/\tcurrent_state=(.*)/) {
	                                        $result->{$host_name}->{$service_description}->{current_state}=$1;
	                                } elsif (/\tplugin_output=(.*)/) {
	                                        $result->{$host_name}->{$service_description}->{plugin_output}=$1;
	                                } elsif (/\tlong_plugin_output=(.*)/) {
	                                        chomp($result->{$host_name}->{$service_description}->{long_plugin_output}=$1);
	                                        while (`<DAT>`) {
	                                                if (/^\t/) {
	                                                        goto NEXT;
	                                                } else {
	                                                        chomp;
	                                                        $result->{$host_name}->{$service_description}->{long_plugin_output}.="\n$_";
	                                                }
	                                        }
	                                } elsif (/^\t\}$/) {
	                                        last;
	                                }
	                        }
	                } else {
	                        next;
	                }
	        }
	        close DAT;
	        return $result;
	}

