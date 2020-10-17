# Monitor NFS filesystems

	:::perl
	# monitor all NFS drives (mount contains server:mountpoint)
	# call: check_multi -s WARNING_THRESHOLD=10% -s CRITICAL_THRESHOLD=5%
	
	eval [ create_disk_check  ] =
	        for (`/sbin/mount`) {
	                # extract all NFS mounts and add them as child checks
	                if ($_=~/(\S+) on \S+:\S+ /) {
	                        my $mountpoint=$1;
	                        my $tag=$mountpoint;
	                        $tag=~s/^\///;
	                        $tag=~s/\//_/g;
	                        
	                        parse_lines("command [ $tag ] = check_disk -w $WARNING_THRESHOLD$ -c $CRITICAL_THRESHOLD$ -E -p $mountpoint");
	                }
	        }


