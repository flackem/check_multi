FIXME
======= Temperature via SNMP =======
### Description

This example checks the Nagios performance using the ''nagiostats'' tool. This check uses the number of checks and the latency for hosts and services as basic performance values.

If you want to integrate additional or other values, have a look at ''nagiostats --help''. The standard call is ''nagiostats -m -d `<DATAVAR>`.

Note the performance value line: it allows you to provide data for one of the major performance tools (PNP or Netways Grapher V2).

### Call / Parameters

    check_multi -f nagiosperf.cmd -s NSTATS=/usr/local/nagios/bin/nagiostats


*  Parameters:
    * 
### Child checks

*  
### State evaluation

(all values are degree Celsius)

*  UNKNOWN:

temp_in or temp_out is not a valid value 

*  WARNING:

temp_in `< 15 or temp_in >` 25 or temp_out `< 0 or temp_out >` 25

*  CRITICAL:

temp_in `< 10 or temp_in >` 28 or temp_out `< -10 or temp_out >` 30
### Code: temperature.cmd

	:::sh
	# temperature.cmd
	# Matthias Flacke, 26.01.2008
	#
	# reads two temperature values from SNMP device and 
	# uses flexible state evaluation
	
	eeval [ temp_in ]       = `/usr/bin/snmpget -c public -v1 -O qv $HOSTNAME$ .1.3.6.1.4.1.2606.1.1.1.0`
	eeval [ temp_out ]      = `/usr/bin/snmpget -c public -v1 -O qv $HOSTNAME$ .1.3.6.1.4.1.2606.1.1.2.0`
	eval  [ temp_perfdata ] = `/bin/echo "|temp_in=$temp_in$ temp_out=$temp_out$"`
	
	state [ UNKNOWN    ]    = (! $temp_in || ! $temp_out)
	state [ WARNING    ]    =\
	         (temp_in  `< 15 || temp_in  >` 25) ||\
	         (temp_out `< 0  || temp_out >` 25)
	state [ CRITICAL   ]    =\
	         (temp_in  `< 10  || temp_in >` 28) ||\
	         (temp_out `< -10 || temp_out>` 30)

### Example Output

	

