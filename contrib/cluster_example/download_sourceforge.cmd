command [ dns  ] = check_dns  -H downloads.sourceforge.net
command [ ping ] = check_icmp -H downloads.sourceforge.net -w 100,20% -c 200,40%
command [ http ] = check_http -H downloads.sourceforge.net -u "http://downloads.sourceforge.net/check-multi/check_multi-0.13.tgz"
