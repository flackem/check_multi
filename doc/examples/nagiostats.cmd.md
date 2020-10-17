```
# nagiostats.cmd

command [ nagios_hosts_number ]     = /usr/local/nagios/bin/nagiostats -m -d NUMHOSTS
command [ nagios_hosts_checks ]     = /usr/local/nagios/bin/nagiostats -m -d NUMHSTACTCHK5M
command [ nagios_hosts_latency ]    = /usr/local/nagios/bin/nagiostats -m -d AVGACTHSTLAT

command [ nagios_services_number ]  = /usr/local/nagios/bin/nagiostats -m -d NUMSERVICES
command [ nagios_services_checks ]  = /usr/local/nagios/bin/nagiostats -m -d NUMACTSVCCHECKS5M
command [ nagios_services_latency ] = /usr/local/nagios/bin/nagiostats -m -d AVGACTSVCLAT

eval [ nagios_perfdata ] = "|host_number=$nagios_hosts_number$ host_checks=$nagios_hosts_checks$ host_latency=$nagios_hosts_latency$ service_number=$nagios_services_number$ service_checks=$nagios_services_checks$ service_latency=$nagios_services_latency$"

state [ WARNING ] = ( \
        $nagios_services_number$ > 1800 || \
        $nagios_services_checks$ > 1500 || \
        $nagios_services_latency$ > 30000 || \
        $nagios_hosts_number$ > 400 || \
        $nagios_hosts_checks$ > 500 || \
        $nagios_hosts_latency$ > 30000 \
)
state [ CRITICAL ] = ( \
        $nagios_services_number$ > 2000 || \
        $nagios_services_checks$ > 2000 || \
        $nagios_services_latency$ > 60000 || \
        $nagios_hosts_number$ > 500 || \
        $nagios_hosts_checks$ > 800 || \
        $nagios_hosts_latency$ > 60000 \
)
```

