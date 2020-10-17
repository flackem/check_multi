# Nagios performance (nagiostats)
## Description

This example checks the Nagios performance using the ''nagiostats'' tool. This check uses the number of checks and the latency for hosts and services as basic performance values.

If you want to integrate additional or other values, have a look at ''nagiostats --help''. The standard call is ''nagiostats -m -d `<DATAVAR>`.

Note the performance value line: it allows you to provide data for one of the major performance tools (PNP or Netways Grapher V2).

**Note:** It is a common experience that a Nagios installation grows and grows silently until it reaches a critical level, so there are also graphs and alarms for the number of host and service checks. 

**New:** Since the DST bug in Nagios scheduling I've added a zero service checks test. If there were no service checks during the last five minutes, a CRITICAL state is yielded.

But be careful: if you monitor Nagios within itself, it won't notify you in this case because also this check is not executed. Possible solutions: monitor Nagios from another instance or create a cronjob which sends a mail in case of trouble.


## Call / Parameters

    check_multi -f nagiostats.cmd -s NSTATS=/path/to/bin/nagiostats


*  Parameters:
    * NSTATS - path to nagiostats binary (controls also Nagios instance)

## Download

All files (nagiostats.cmd, nagiostats.php) are available in the [check_multi package](http://my-plugin.de/wiki/projects/check_multi/download).

## Child checks

 | Name                          | Code                              | Comment (see nagiostats --help)                                      | 
 | ----                          | ----                              | -------------------------------                                      | 
 | host_number                   | $NSTATS$ -m -d NUMHOSTS           | total number of hosts                                                | 
 | host_checks_5min_all          | $NSTATS$ -m -d NUMACTHSTCHECKS5M  | number of total active host checks occuring in last 5 minutes        | 
 | host_checks_5min_scheduled    | $NSTATS$ -m -d NUMSACTHSTCHECKS5M | number of scheduled active host checks occuring in last 5 minutes    | 
 | host_checks_5min_ondemand     | $NSTATS$ -m -d NUMOACTHSTCHECKS5M | number of on-demand active host checks occuring in last 5 minutes    | 
 | service_number                | $NSTATS$ -m -d NUMSERVICES        | total number of services                                             | 
 | service_checks_5min_all       | $NSTATS$ -m -d NUMACTSVCCHECKS5M  | number of total active service checks occuring in last 5 minutes     | 
 | service_checks_5min_scheduled | $NSTATS$ -m -d NUMSACTSVCCHECKS5M | number of scheduled active service checks occuring in last 5 minutes | 
 | service_checks_5min_ondemand  | $NSTATS$ -m -d NUMOACTSVCCHECKS5M | number of on-demand active service checks occuring in last 5 minutes | 
 | host_latency_ms               | $NSTATS$ -m -d AVGACTHSTLAT       | AVG active host check latency (ms)                                   | 
 | host_execution_time_ms        | $NSTATS$ -m -d AVGACTHSTEXT       | AVG active host check execution time (ms)                            | 
 | service_latency_ms            | $NSTATS$ -m -d AVGACTSVCLAT       | AVG active service check latency (ms)                                | 
 | service_execution_time_ms     | $NSTATS$ -m -d AVGACTSVCEXT       | AVG active service check execution time (ms)                         | 

## State evaluation

*  UNKNOWN:
    * no NSTATS parameter defined 
    * no executable binary nagiostats found

*  WARNING
    * > 500 hosts defined or no hosts defined
    * > 2500 services defined or no services defined
    * > 500 host checks in 5 minutes
    * > 2500 service checks in 5 minutes
    * >  5 seconds host latency
    * > 10 seconds service latency

*  CRITICAL
    * > 1000 hosts defined
    * > 5000 services defined
    * > 1000 host checks in 5 minutes
    * > 5000 service checks in 5 minutes or no service checks 
    * > 10 seconds host latency
    * > 20 seconds service latency

These thresholds may be different for your installation, the sizing is based on a large installation with active checks under Nagios 3.

## Code: nagiostats.cmd

```
# nagiostats.cmd

#
# checks Nagios performance and provides alarms and performance data

#
# Copyright (c) 2008-2009 Matthias Flacke (matthias.flacke at gmx.de)

#
# Call: check_multi -f nagiostats.cmd -s NSTATS=/path/to/nagiostats

#
#

# 1. check correct parameter passing for NSTAT binary
eeval   [ NSTATS_defined                ] = \ 
        if ("$NSTATS$" eq "") { \ 
                print "No '-s NSTATS=/path/to/nagiostats' defined\n"; \
                exit 3; \
        } else { \ 
                "OK"; \
        }   
# 2. check if passed binary is available and executable

eeval   [ nagiostats_executable         ] = \ 
        if ( ! -x "$NSTATS$") { \ 
                print "No nagiostats executable $NSTATS$ found\n"; \
                exit 3; \
        } else { \ 
                "$NSTATS$"; \
        }   
# 3. checks

command [ host_number                   ] = $NSTATS$ -m -d NUMHOSTS
command [ host_checks_5min_all          ] = $NSTATS$ -m -d NUMACTHSTCHECKS5M
command [ host_checks_5min_scheduled    ] = $NSTATS$ -m -d NUMSACTHSTCHECKS5M
command [ host_checks_5min_ondemand     ] = $NSTATS$ -m -d NUMOACTHSTCHECKS5M
 
command [ service_number                ] = $NSTATS$ -m -d NUMSERVICES
command [ service_checks_5min_all       ] = $NSTATS$ -m -d NUMACTSVCCHECKS5M
command [ service_checks_5min_scheduled ] = $NSTATS$ -m -d NUMSACTSVCCHECKS5M
command [ service_checks_5min_ondemand  ] = $NSTATS$ -m -d NUMOACTSVCCHECKS5M
 
command [ host_latency_ms               ] = $NSTATS$ -m -d AVGACTHSTLAT
command [ host_execution_time_ms        ] = $NSTATS$ -m -d AVGACTHSTEXT
 
command [ service_latency_ms            ] = $NSTATS$ -m -d AVGACTSVCLAT
command [ service_execution_time_ms     ] = $NSTATS$ -m -d AVGACTSVCEXT
 
# 4. performance data

command [ perfdata::nagiostats          ] = /bin/echo "OK|host_number=$host_number$ host_checks_5min_all=$host_checks_5min_all$ host_checks_5min_scheduled=$host_checks_5min_scheduled$ host_checks_5min_ondemand=$host_checks_5min_ondemand$ service_number=$service_number$ service_checks_5min_all=$service_checks_5min_all$ service_checks_5min_scheduled=$service_checks_5min_scheduled$ service_checks_5min_ondemand=$service_checks_5min_ondemand$ host_latency_ms=$host_latency_ms$ host_execution_time_ms=$host_execution_time_ms$ service_latency_ms=$service_latency_ms$ service_execution_time_ms=$service_execution_time_ms$"


# 5. state definitions

state [ WARNING ] =     $host_number$               >   500 || $host_number$             <= 0 \
                        $service_number$            >  2500 || $service_number$          <= 0 \
                        $host_checks_5min_all$      >   500 || \
                        $service_checks_5min_all$   >  2500 || \ 
                        $host_latency_ms$           >  5000 || \
                        $service_latency_ms$        > 10000
 
state [ CRITICAL ] =    $host_number$               >  1000 || \
                        $service_number$            >  5000 || \
                        $host_checks_5min_all$      >  1000 || \
                        $service_checks_5min_all$   >  5000 || $service_checks_5min_all$ <= 0 \
                        $host_latency_ms$           > 10000 || \
                        $service_latency_ms$        > 20000

```


## PNP performance chart

{{:check_multi:examples:nagiostats_pnp.png|PNP performance chart}}

## Extinfo Output

{{:check_multi:examples:nagiostats.png|Nagiostats extinfo output}}


## PNP template

Store this file as ''nagiostats.php'' in your NAGIOSDIR/share/pnp/templates directory.

```
	:::php
	<?php
	#
	# PNP template for nagiostats output
	# Plugin: check_multi -f nagiostats.cmd
	# Matthias Flacke, June 25th 2009
	#
	$ds_name[1] = "Host and Service Latency";
	$opt[1]  = "--vertical-label \"Time in ms\" -l0 --title \"Host and Service Latency in ms - $hostname\" ";
	$def[1]  = "DEF:var9=$rrdfile:$DS[9]:AVERAGE " ;
	$def[1] .= "DEF:var10=$rrdfile:$DS[10]:AVERAGE " ;
	$def[1] .= "DEF:var11=$rrdfile:$DS[11]:AVERAGE " ;
	$def[1] .= "DEF:var12=$rrdfile:$DS[12]:AVERAGE " ;
	
	$def[1] .= "AREA:var11#FFCC00:\"Service latency  \" " ;
	$def[1] .= "GPRINT:var11:LAST:\"%6.0lf ms last\" " ;
	$def[1] .= "GPRINT:var11:AVERAGE:\"%6.0lf ms avg\" " ;
	$def[1] .= "GPRINT:var11:MAX:\"%6.0lf ms max\" " ;
	$def[1] .= "GPRINT:var11:MIN:\"%6.0lf ms min\\n\" " ;
	
	$def[1] .= "LINE:var12#FF0000:\"Service exec time\" " ;
	$def[1] .= "GPRINT:var12:LAST:\"%6.0lf ms last\" " ;
	$def[1] .= "GPRINT:var12:AVERAGE:\"%6.0lf ms avg\" " ;
	$def[1] .= "GPRINT:var12:MAX:\"%6.0lf ms max\" " ;
	$def[1] .= "GPRINT:var12:MIN:\"%6.0lf ms min\\n\" " ;
	
	$def[1] .= "AREA:var9#5555FF:\"Host latency     \" " ;
	$def[1] .= "GPRINT:var9:LAST:\"%6.0lf ms last\" " ;
	$def[1] .= "GPRINT:var9:AVERAGE:\"%6.0lf ms avg\" " ;
	$def[1] .= "GPRINT:var9:MAX:\"%6.0lf ms max\" " ;
	$def[1] .= "GPRINT:var9:MIN:\"%6.0lf ms min\\n\" " ;
	
	$def[1] .= "LINE:var10#000000:\"Host exec time   \" " ;
	$def[1] .= "GPRINT:var10:LAST:\"%6.0lf ms last\" " ;
	$def[1] .= "GPRINT:var10:AVERAGE:\"%6.0lf ms avg\" " ;
	$def[1] .= "GPRINT:var10:MAX:\"%6.0lf ms max\" " ;
	$def[1] .= "GPRINT:var10:MIN:\"%6.0lf ms min\\n\" " ;
	
	
	$ds_name[2] = "Service Checks";
	$opt[2]  = "--vertical-label \"Checks\" -l0 --title \"Service checks during last 5 minutes - $hostname\" ";
	$def[2]  = "DEF:var5=$rrdfile:$DS[7]:AVERAGE " ;
	$def[2] .= "DEF:var6=$rrdfile:$DS[8]:AVERAGE " ;
	$def[2] .= "DEF:var7=$rrdfile:$DS[6]:AVERAGE " ;
	$def[2] .= "DEF:var8=$rrdfile:$DS[5]:AVERAGE " ;
	
	$def[2] .= "AREA:var5#FF9900:\"Scheduled checks\":STACK " ;
	$def[2] .= "GPRINT:var5:LAST:\"%6.0lf last\" " ;
	$def[2] .= "GPRINT:var5:AVERAGE:\"%6.0lf avg\" " ;
	$def[2] .= "GPRINT:var5:MAX:\"%6.0lf max\" " ;
	$def[2] .= "GPRINT:var5:MIN:\"%6.0lf min\\n\" " ;
	
	$def[2] .= "AREA:var6#FFCC00:\"Ondemand checks \":STACK " ;
	$def[2] .= "GPRINT:var6:LAST:\"%6.0lf last\" " ;
	$def[2] .= "GPRINT:var6:AVERAGE:\"%6.0lf avg\" " ;
	$def[2] .= "GPRINT:var6:MAX:\"%6.0lf max\" " ;
	$def[2] .= "GPRINT:var6:MIN:\"%6.0lf min\\n\" " ;
	
	$def[2] .= "LINE:var7#FF0000:\"All checks      \" " ;
	$def[2] .= "GPRINT:var7:LAST:\"%6.0lf last\" " ;
	$def[2] .= "GPRINT:var7:AVERAGE:\"%6.0lf avg\" " ;
	$def[2] .= "GPRINT:var7:MAX:\"%6.0lf max\" ";
	$def[2] .= "GPRINT:var7:MIN:\"%6.0lf min\\n\" " ;
	
	$def[2] .= "LINE:var8#000000:\"Services defined\" " ;
	$def[2] .= "GPRINT:var8:LAST:\"%6.0lf last\" " ;
	$def[2] .= "GPRINT:var8:AVERAGE:\"%6.0lf avg\" " ;
	$def[2] .= "GPRINT:var8:MAX:\"%6.0lf max\" ";
	$def[2] .= "GPRINT:var8:MIN:\"%6.0lf min\\n\" " ;
	
	
	$ds_name[3] = "Host Checks";
	$opt[3]  = "--vertical-label \"Checks\" -l0 --title \"Host checks during last 5 minutes - $hostname\" ";
	$def[3]  = "DEF:var1=$rrdfile:$DS[3]:AVERAGE " ;
	$def[3] .= "DEF:var2=$rrdfile:$DS[4]:AVERAGE " ;
	$def[3] .= "DEF:var3=$rrdfile:$DS[2]:AVERAGE " ;
	$def[3] .= "DEF:var4=$rrdfile:$DS[1]:AVERAGE " ;
	
	$def[3] .= "AREA:var1#7777FF:\"Scheduled checks\":STACK " ;
	$def[3] .= "GPRINT:var1:LAST:\"%6.0lf last\" " ;
	$def[3] .= "GPRINT:var1:AVERAGE:\"%6.0lf avg\" " ;
	$def[3] .= "GPRINT:var1:MAX:\"%6.0lf max\" " ;
	$def[3] .= "GPRINT:var1:MIN:\"%6.0lf min\\n\" " ;
	
	$def[3] .= "AREA:var2#BBBBFF:\"Ondemand checks \":STACK " ;
	$def[3] .= "GPRINT:var2:LAST:\"%6.0lf last\" " ;
	$def[3] .= "GPRINT:var2:AVERAGE:\"%6.0lf avg\" " ;
	$def[3] .= "GPRINT:var2:MAX:\"%6.0lf max\" " ;
	$def[3] .= "GPRINT:var4:MIN:\"%6.0lf min\\n\" " ;
	
	$def[3] .= "LINE:var3#0000FF:\"All checks      \" " ;
	$def[3] .= "GPRINT:var3:LAST:\"%6.0lf last\" " ;
	$def[3] .= "GPRINT:var3:AVERAGE:\"%6.0lf avg\" " ;
	$def[3] .= "GPRINT:var3:MAX:\"%6.0lf max\" ";
	$def[3] .= "GPRINT:var3:MIN:\"%6.0lf min\\n\" " ;
	
	$def[3] .= "LINE:var4#000000:\"Hosts defined   \" " ;
	$def[3] .= "GPRINT:var4:LAST:\"%6.0lf last\" " ;
	$def[3] .= "GPRINT:var4:AVERAGE:\"%6.0lf avg\" " ;
	$def[3] .= "GPRINT:var4:MAX:\"%6.0lf max\" ";
	$def[3] .= "GPRINT:var4:MIN:\"%6.0lf min\\n\" " ;
	
	?>
```
