======= Contributions =======

All contributions are also part of the check_multi tree and included in the tarball.



##  notify_service_html

notify_service_html is part of the check_multi package.


This Script can be used as a replacement for the standard notification, it sends the HTML extended plugin output as a MIME attachment.
    - Caveat: you need a [special version of mailx](http://heirloom.sourceforge.net/mailx.html), which is capable to deal with attachments on command line.
    - Copy both files into the libexec directory.
    - Replace the corresponding notify-service-by-email setting in your commands.cfg with the following lines:

```
# 'notify-service-by-email' command definition 
define command {
    command_name         notify-service-by-email
    command_line         /bin/sh /usr/local/nagios/libexec/notify_service_html
}
```
- The script does not make use of command line variables. It instead works with Nagios environment vars which have to be enabled in the nagios.cfg:`enable_environment_macros=1`

Example mail output (it's the old template version and hopefully will be updated soon ;-)):
```
Nagios service notification
PROBLEM check_multi test WARNING
Sun Aug 5 16:33:23 CEST 2007

--- Host information ---
Name                   thinkpad
IP address             127.0.0.1

--- Service information ---
Name                   check_multi test
State                  WARNING
State type             HARD
Output                 SYSTEM WARNING - 15 plugins checked, 0 critical (), 1 warning (disk_root_warning), 0 unknown (), 14 ok

WARNING service output
[15] WARNING disk_root_warning - DISK WARNING - free space: / 4876 MB (42% inode=82%);

OK service output
[ 1] OK proc_cron - PROCS OK: 1 process with command name 'cron'
[ 2] OK proc_syslogd - PROCS OK: 1 process with command name 'syslog-ng'
[ 3] OK proc_xinetd - PROCS OK: 1 process with command name 'xinetd'
[ 4] OK procs_RSS - RSS OK: 136 processes
[ 5] OK procs_zombie - PROCS OK: 1 process with STATE = Z
[ 6] OK system_load - OK - load average: 0.53, 1.20, 1.72
[ 7] OK system_mail - TCP OK - 0.015 second response time on port 25
[ 8] OK system_mailqueue - OK: mailq is empty
[ 9] OK system_ntp - NTP OK: Offset 10.86617522 secs
[10] OK system_portmapper - OK: RPC program portmapper version 2 udp running
[11] OK system_rootdisk - DISK OK - free space: / 4876 MB (42% inode=82%);
[12] OK system_ssh - SSH OK - OpenSSH_4.4 (protocol 1.99)
[13] OK system_swap - SWAP OK - 97% free (1978 MB out of 2048 MB) 
[14] OK system_syslog - FILE_AGE OK: /var/log/messages is 1 seconds old and 6943224 bytes

Plugin                 check_multi!/usr/local/nagios/etc/check_multi.cmd
Execution time(s)      1.248

--- Contact information ---
Name                   nagiosadmin
Alias                  Nagios Admin
Mail address           Matthias.Flacke@gmx.net
Notification type      PROBLEM

--- Service URLs ---
Service details        http://localhost/nagios/cgi-bin/extinfo.cgi?type=2&host=thinkpad&service=check_multi test
Service alert history  http://localhost/nagios/cgi-bin/history.cgi?host=thinkpad&service=check_multi test
Service availability   http://localhost/nagios/cgi-bin/avail.cgi?host=thinkpad&&service=check_multi test&show_log_entries
Service comments       http://localhost/nagios

--- Host URLs ---
Host details           http://localhost/nagios/cgi-bin/extinfo.cgi?type=1&host=thinkpad
Host services          http://localhost/nagios/cgi-bin/status.cgi?host=dada
Host alert history     http://localhost/nagios/cgi-bin/history.cgi?host=thinkpad
Host availability      http://localhost/nagios/cgi-bin/avail.cgi?host=thinkpad&show_log_entries
Host comments          http://localhost/nagios
```

## status_query.cgi

At this very moment the status_query.cgi is only available in one of the   [developer versions](download.md) in ''contrib/status_query''. Create the CGI script via  ''make'' and copy it into your nagios cgi-bin directory, normally `<nagiosdir>`/sbin''.

It provides - not only for check_multi purposes - a flexible interface to query different fields in the Nagios status.dat and provide the results in a table which looks like status.cgi.


{{tag>status.dat GUI}}

