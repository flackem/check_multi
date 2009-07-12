# check definitions
command [ my-plugin   ] = check_multi -n "" -f /usr/local/nagios/etc/download_my-plugin.cmd -r 31
command [ sourceforge ] = check_multi -n "" -f /usr/local/nagios/etc/download_sourceforge.cmd -r 31
# state definitions
state [ warning  ]	= COUNT(CRITICAL) > 0 || COUNT(WARNING) > 0 || COUNT(UNKNOWN) > 0
state [ critical ]	= COUNT(CRITICAL) > 1
