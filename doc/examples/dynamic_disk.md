======= (Dynamic) Disk monitoring =======
## Description

check_disk is a powerful plugin, but it lacks a clear and simple visualization. Practical experiences show that with multiple FS monitored the administrator does not know **which** particular FS breaks a threshold:

	
	DISK CRITICAL - free space: / 5174 MB (33% inode=87%); /dev 501 MB (99% inode=99%); /phys/sda3 5821 MB (2% inode=99%); /phys/sdb1 6984 MB (3% inode=86%); /phys/sdc1 44533 MB (19% inode=99%); /phys/sdd2 691 MB (0% inode=51%);| /=10131MB;14512;15318;0;16125 /dev=0MB;450;475;0;501 /phys/sda3=197842MB;193106;203834;0;214563 /phys/sdb1=215807MB;211243;222979;0;234715 /phys/sdc1=178258MB;211243;222979;0;234715 /phys/sdd2=222950MB;205385;216795;0;228206
	


*check_multi* presents a solution: all filesystems are monitored individually and the particular results are bound in one multi-check. There are no problems or side effects towards performance data, it's just clearer which FS breaks the line:

	
	CRITICAL - 6 plugins checked, 3 critical (df_phys_sda3, df_phys_sdb1, df_phys_sdd2), 3 ok
	[ 1] partitions 5
	[ 2] df_root DISK OK - free space: / 5174 MB (33% inode=87%);
	[ 3] df_phys_sda3 DISK CRITICAL - free space: /phys/sda3 5821 MB (2% inode=99%);
	[ 4] df_phys_sdb1 DISK CRITICAL - free space: /phys/sdb1 6984 MB (3% inode=86%);
	[ 5] df_phys_sdc1 DISK OK - free space: /phys/sdc1 44533 MB (19% inode=99%);
	[ 6] df_phys_sdd2 DISK CRITICAL - free space: /phys/sdd2 691 MB (0% inode=51%);|check_multi::check_multi::plugins=6 time=0.044049 df_root::check_disk::/=10131MB;14512;15318;0;16125 df_phys_sda3::check_disk::/phys/sda3=197842MB;193106;203834;0;214563 df_phys_sdb1::check_disk::/phys/sdb1=215807MB;211243;222979;0;234715 df_phys_sdc1::check_disk::/phys/sdc1=178258MB;211243;222979;0;234715 df_phys_sdd2::check_disk::/phys/sdd2=222950MB;205385;216795;0;228206
	


## Call / Parameters

    check_multi -f dynamic_disk.cmd [-s WARNING|WARNING_PERCENT="string"] [-s CRITICAL|CRITICAL_PERCENT="string"]


*  Defaults
    * WARNING
    * WARNING_PERCENT
    * CRITICAL
    * CRITICAL_PERCENT


*  Parameters (optional):
    * WARNING
    * WARNING_PERCENT
    * WARNING_`<fs>`
    * WARNING_PERCENT_`<fs>`
    * CRITICAL
    * CRITICAL_PERCENT
    * CRITICAL_`<fs>`
    * CRITICAL_PERCENT_`<fs>`

## Download

All files (nagiostats.cmd, nagiostats.php) are available in the check_multi package or [here](http://svn.my-plugin.de/repos/check_multi/trunk/sample_config/nagiostats).

## Child checks

 | Name       | Code                                                                             | Comment                                                                                                                              | 
 | ----       | ----                                                                             | -------                                                                                                                              | 
 | partitions | see dynamic_disk.cmd                                                             | 1. discovery of disk partitions

2. assignment of thresholds                                                                        | 
 | df_`<fs>`    | check_disk

-w WARNING\\ -w WARNING_PERCENT\\ -c CRITICAL\\ -c CRITICAL_PERCENT | all `<fs>` are provided with the following thresholds:\\ 1. defaults if none specified\\ 2. generic, if any\\ 3. `<fs>`-specific, if any | 

## State evaluation

There is no specific state evaluation, all check_disk results are passed through.

## Code: nagiostats.cmd

	:::perl
	
	#
	# dynamic_disk.cmd
	#
	# (c) 2007-2009 Matthias Flacke (matthias.flacke at gmx.de)
	#
	# dynamic_disk.cmd is a check_multi wrapper for check_disk and
	# determines the available FS from check_disk output.
	#
	# It then excludes several
	# - file system types
	# - fs names
	# - fs patterns
	#
	# Available parameters:
	# WARNING_PERCENT  - disk space in percent
	# WARNING          - absolute disk space
	# CRITICAL_PERCENT - disk space in percent
	# CRITICAL         - absolute disk space
	#
	# All parameters can be also specified for a specific FS as well, e.g.:
	# WARNING_PERCENT_var="20%"
	
	eeval [ partitions ] = \
	        my $exclude_fs_type=("$EXCLUDE_FS_TYPE$") ? "$EXCLUDE_FS_TYPE$" : "hsfs|tmpfs|mvfs|nfs"; \
	        my $exclude_fs=     ("$EXCLUDE_FS$")      ? "$EXCLUDE_FS$"      : "/dev/shm"; \
	        my $exclude_pattern=("$EXCLUDE_PATTERN$") ? "$EXCLUDE_PATTERN$" : "\/cdrom"; \
	        my $disk_command="check_disk -w 2 -c 1" .  \
	                " -x " . join(" -x ", split('\|',$exclude_fs)) . \
	                " -X " . join(" -X ", split('\|',$exclude_fs_type)) . \
	                " | sed s'/.*\|\(.*\)/\1/'"; \
	        my $available_disks=`$disk_command`; \
	        my $count=0; \
	        my $WARNING_PERCENT=($WARNING_PERCENT$)?"$WARNING_PERCENT$":"10%"; \
	        my $CRITICAL_PERCENT=($CRITICAL_PERCENT$)?"$CRITICAL_PERCENT$":"5%"; \
	        my $WARNING=($WARNING$)?"$WARNING$":"500M";\
	        my $CRITICAL=($CRITICAL$)?"$CRITICAL$":"200M";\
	        foreach my $token (sort split(/\s+/,$available_disks)) { \
	                if ($token=~/^([^=]+)=([^;]+);([^;]+);([^;]+);([^;]+);(.*)$/) { \
	                        my $fsname=$1; \
	                        my $fs=$1; \
	                        next if ($fs=~/$exclude_pattern/); \
	                        $fsname=~s/\//_/g; $fsname="_root" if ($fsname eq '_'); \
	                        $count++; \
	                        parse_lines(sprintf "command [ df%-20s ] = check_disk -w %s -w %s -c %s -c %s -l -E -p %s\n", \
	                                $fsname, \
	                                ($ENV{"MULTI_WARNING${fsname}"})?$ENV{"MULTI_WARNING${fsname}"}:$WARNING, \
	                                ($ENV{"MULTI_WARNING_PERCENT${fsname}"})?$ENV{"MULTI_WARNING_PERCENT${fsname}"}:$WARNING_PERCENT, \
	                                ($ENV{"MULTI_CRITICAL${fsname}"})?$ENV{"MULTI_CRITICAL${fsname}"}:$CRITICAL, \
	                                ($ENV{"MULTI_CRITICAL_PERCENT${fsname}"})?$ENV{"MULTI_CRITICAL_PERCENT${fsname}"}:$CRITICAL_PERCENT, \
	                                $fs, \
	                        ); \
	                } \
	        } \
	        return $count;




## Extinfo Output

{{:check_multi:examples:nagiostats.png|Nagiostats extinfo output}}



