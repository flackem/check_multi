	:::perl
	#
	# snmpwalk_loadbalancer.cmd
	#
	# call with:
	# check_multi -f snmpwalk_loadbalancer.cmd -s PoolName="Pool-Prod"
	#
	
	#eeval [ PoolName   ] = "Pool-cpdnsm-Dasa-Prod";
	
	# if no PoolName specified, complain and exit with UNKNOWN
	eval [ PoolName   ] = 
	        if ("x$PoolName$" eq "x") { 
	                print "No PoolName specified. Exit\n"; 
	                exit $UNKNOWN; 
	        } else { 
	                "$PoolName$" 
	        }
	
	# get overall state - if non green, set CRITICAL, otherwise OK
	eeval [ AvailState ] = 
	        my $snmpget=`grep ltmPoolAvailabilityState /tmp/snmpwalk1.txt | grep "$PoolName$"`; 
	        if ($snmpget=~/.* ([^\(]+)\((\d+)\)/) {
	                my $color=$1; my $code=$2;
	                $?=($code==1) ? $OK : $CRITICAL<<8;
	                "$color($code)";
	        } else {
	                $?=3; 
	                "Error parsing ltmPoolAvailabilityState for $PoolName$";
	        }
	
	# dynamically add all IPs with their states: non green maps to WARNING!
	eval  [ loop_over_IPs ] = 
	        for (`grep ltmPoolMbrStatusAvailState /tmp/snmpwalk1.txt | grep "$PoolName$"`) {
	                # F5-BIGIP-LOCAL-MIB::ltmPoolMbrStatusAvailState."Pool-DB2-Eval".ipv4."`<IPADDR>`".50000 = INTEGER: green(1)
	                if (/ltmPoolMbrStatusAvailState\.\"$PoolName$\"\.ipv4\.\"([^\"]*)\".*INTEGER: (\w+)\((\d+)\)/) {
	                        #print "IP:$1 color:$2 code:$3\n";
	                        my $ip=$1; my $color=$2; my $code=$3;
	                        $ip=~s/\./_/g;
	                        parse_lines("eeval \[ $PoolName$_$ip \] = \$? = ($code==1) ? $OK : $WARNING<<8; \"$color\";");
	                }
	        }
	
	# ignore any WARNING states from the looped IPs:
	# the overall RC is determined by AvailState
	state [ WARNING ] = 1==0
	

