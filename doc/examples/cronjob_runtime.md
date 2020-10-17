======= Runtime of cronjobs =======
## Description

## Call / Parameters

    check_multi -f cronjob_runtime.cmd


*  Defaults
    * WARNING:  1 day
    * CRITICAL: 2 days


*  Parameters:
    * none (settings to be adjusted inside the command file)

## Download

cronjob_runtime.cmd is available in the check_multi package or [here](http://svn.my-plugin.de/repos/check_multi/trunk/sample_config/nagiostats).

## Child checks

 | Name | Code | Comment | 
 | ---- | ---- | ------- | 
 |      |      |         | 
## State evaluation

There is no specific state evaluation, all check_disk results are passed through.

## Code: nagiostats.cmd

	:::perl
	eeval [ cron_pid     ] = (split(/\s+/,`ps -e -o pid,fname | grep -v grep | grep cron`))[0]
	eeval [ warn_minutes ] = 1*24*60; # 1 day
	eeval [ crit_minutes ] = 2*24*60; # 2 days
	
	#--- get cronjobs out of ptree and check their runtime
	eeval [ cronjob_runtime ] = 
	        my $output=""; 
	        my $error="";
	        my $warn=0;
	        my $crit=0;
	        open(PTREE,'/usr/bin/ptree $cron_pid$|') ; #|| print "Cannot execute /usr/bin/ptree $cron_pid$:$!"; exit 3;
	        while (`<PTREE>`) {
	                if (! /\s*(\d+)\s+(.*)/) {
	                        $error.="Invalid ptree line: $_ ";
	                        next;
	                }
	                my $pid=$1;
	                my $cmdline=$2; $cmdline=~s/\|/PIPE/g;
	                #    ELAPSED
	                # 54-12:35:25
	                my $elapsed=`/bin/ps -p $pid -o etime`;
	
	                if ($elapsed=~/(\d*)[-]*(\d*)[:]*(\d+):(\d+)/s) {
	                        my $d=($1)?$1:0;
	                        my $h=($2)?$2:0;
	                        my $m=($3)?$3:0;
	                        my $s=($4)?$4:0;
	                        $elapsed=$d*12*60*60+$h*60*60+$m*60;
	                        next if ($pid==$cron_pid$); # don't count cron itself
	                        $output.=sprintf "%02dd %02dh %02dm elapsed for %5d - %s\n", $d, $h, $m, $pid, $cmdline;
	                        if ($elapsed>$warn_minutes$) { 
	                                $crit++;
	                        } elsif ($elapsed>$crit_minutes$) {
	                                $warn++;
	                        }
	                } else {
	                        $error.="Invalid timeformat in '$elapsed' ";
	                }
	        }
	        close PTREE;
	        $?=(1<<8) if ($warn);
	        $?=(2<<8) if ($crit);
	        return "$crit CRITICAL $warn WARNING\n$output\n";




## Extinfo Output

{{:check_multi:examples:???.png|To be added}}



