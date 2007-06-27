
#--- logfiles
#command[messages_ALERT]	= check_logfiles --logfile=/var/log/messages --tag=ALERT --rotation=SUSE --warningpattern=ALERT
#command[messages_critical]	= check_logfiles --logfile=/var/log/messages --tag=critical --rotation=SUSE --criticalpattern=critical

#--- some local checks on the nagios system
command[ network_ping ]		= check_ping -H localhost -w 500,5% -c 1000,10%
command[ network_interfaces ]	= check_ifstatus -H localhost
command[ network_if_eth1 ]	= check_ifoperstatus -k 4 -H localhost
command[ network_rsync ]	= check_tcp -H localhost -p 873 -e RSYNCD
command[ test_sleep ]		= check_sleep 2 2
command[ proc_acpid ]		= check_procs -c 1: -C acpid
command[ proc_automount ]	= check_procs -c 1: -C automount
command[ proc_cron ]		= check_procs -c 1: -C cron
command[ proc_httpd ]		= check_procs -c 1: -C httpd2-prefork
command[ proc_smartd ]		= check_procs -c 1: -C smartd
command[ proc_snmpd ]		= check_procs -c 1: -C snmpd
command[ proc_syslogd ]		= check_procs -c 1: -C syslog-ng
command[ proc_xinetd ]		= check_procs -c 1: -C xinetd
command[ procs_number ]		= check_procs
command[ procs_RSS ]		= check_procs -w 500000 -c 1000000 --metric=RSS
command[ procs_zombie ]		= check_procs -w 1 -c 2 -s Z
command[ system_load ]		= check_load -w 5,4,3 -c 10,8,6
command[ system_mail ]		= check_tcp -H localhost -p 25
command[ system_mailqueue ]	= check_mailq -w 2 -c 4
command[ system_mysql ]		= check_mysql -u admin
command[ system_ntp ]		= check_ntp -H ntp1.fau.de
command[ system_portmapper ]	= check_rpc -H localhost -C portmapper
command[ system_rootdisk ]	= check_disk -w 5% -c 2% -p /
command[ system_ssh ]		= check_ssh localhost
command[ system_swap ]		= check_swap -w 90 -c 80
command[ system_syslog ]	= check_file_age -f /var/log/messages -c 86400 -C 0
command[ system_users ]		= check_users -w 5 -c 10

#--- nagios check
command[ nagios_system ]	= check_nagios -F /usr/local/nagios/var/nagios.log -e 5 -C nagios
command[ nagios_tac ]		= check_http -H localhost -u "http://localhost/nagios/cgi-bin/tac.cgi" -a guest:guest

#--- some external checks
command[ nagios_ping ]		= check_ping -H www.nagios.org -w 500,5% -c 1000,10%
command[ nagios.org_dns ]	= check_dns -H www.nagios.org
command[ nagios.org_http ]	= check_http -H www.nagios.org

