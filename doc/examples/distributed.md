======= Distributed service checks with check_multi =======

### Description

Some day a customer complained that he could access a local intranet server. But I was sure that the server is running, nagios showed green lights everywhere.


But when I remotely connected to the customers PC, I had to notice that he is right and there is no connection from his network to the intranet server due to routing problems. Whoops... 8-o

 



The afternoon I thought about ways to cover this situation in our Nagios monitoring. Nagios has no obvious resp. generic solution for this problem except setting up multiple checks from different hosts.\\



But wait a little bit - there is a conceptional problem with this. All these checks are associated to **other** hosts as they're really belonging to. This will confuse the whole process (and the administrator as well ;-)). Notifications and escalations are based on the wrong host and the statistics / SLAs are also affected.





*check_multi* provides a simple but effective solution for this scenario: a distributed monitoring which works as a service associated to the target host.




   
{{:check_multi:examples:distributed_monitoring.png|}}





You need:  
 1.  remote access to some hosts in the wanted subnets

(i.e. normally some of your monitored servers)  
 2.  a check plugin existing on each of these hosts, which can monitor the service

(e.g. check_tcp)



You will then:
 1.  schedule a check on each of these hosts towards your target host / target service
 2.  add a flexible state evaluation of your results:



    * either all results have to be OK for the overall state being OK
    * or only some results OK will set the overall state to OK



That's it! :-)

And more: you can do this with **one** generic *check_multi* command file. Some parameters will control which hosts are to be checked and what check_command is used to examine the service.



### Call / Parameters

```
check_multi -f distributed.cmd \
-s CHECK_COMMAND="check_tcp -p 80 -H hostx -t 5" \
-s HOSTS="host1,host2,host3,host4,host5" \
-s THRESHOLDS="-w 'COUNT(WARNING)>3' -c 'COUNT(CRITICAL)>3'"
```

As you can see in the source below, you can also set other parameters from command line.

But there are already some reasonable defaults available:
    - TIMEOUT (default: 2)

this default is shorter than the normal default of 10 seconds. This is feasible here because we have multiple checks where only some have to succeed and others may fail without influencing the whole result.
    - REMOTE_CHECK (default: ''check_by_ssh -H \$host -t $timeout$ -C'' )

If you're running NRPE you can adjust this default as well.
### Child checks

Most of the child checks are designed for parameter validation and visualization:
 1.  check_command: the plugin command line to check the remote service
 2.  timeout: the timeout for the remote check

(**note**: not the timeout for the plugin, this has to be specified within the check_command itself)
 3.  hosts_to_check: comma separated list of hosts to check
 4.  remote_check: command to access a remote host, normally via NRPE or SSH.
 5.  host_checks: this dynamically creates one child check per host and returns the number of child checks.

### State evaluation


### Code: interface.cmd

	:::perl
	#
	# distributed.cmd
	#
	# Matthias Flacke, 21.11.2008
	#
	# calls different remote hosts with parametrized check and returns
	# only critical if (nearly) all hosts return errors
	#
	# Call: check_multi -f distributed.cmd
	#       -s CHECK_COMMAND="check_tcp -p 80 -H hostx -t 5" \
	#       -s HOSTS="host1,host2,host3,host4,host5" \
	#       -s THRESHOLDS="-w 'COUNT(WARNING)>3' -c 'COUNT(CRITICAL)>3'"
	#
	# caveat: take care of the different timeout thresholds!
	#
	eeval [ check_command ] = \
	        if ( "$CHECK_COMMAND$" ) { \
	                return "$CHECK_COMMAND$"; \
	        } else {\
	                print "Error: CHECK_COMMAND not defined. Exit.\n"; \
	                exit 3; \
	        }
	#
	eeval [ timeout ] = ( "$TIMEOUT$" eq "") ? "2" : "$TIMEOUT$";
	#
	eeval [ hosts_to_check ] = \
	        if ( "$HOSTS$") { \
	                return "$HOSTS$"; \
	        } else {\
	                print "Error: no HOSTS defined. Exit.\n"; \
	                exit 3; \
	        } \
	#
	eeval [ remote_check ] = \
	        if ( "$REMOTE_CHECK$") { \
	                return "$REMOTE_CHECK$"; \
	        } else { \
	                return "check_by_ssh -H \$host -t $timeout$ -C "; \
	        }
	#
	eeval [ host_checks ] = \
	        my $count=0; \
	        my $disttest=''; \
	        foreach my $host (split(/,/,'$HOSTS$')) { \
	                $disttest.="-x \'command [ $host ] = $remote_check$ \"$CHECK_COMMAND$\"\' "; \
	                $count++; \
	        } \
	        parse_lines("command [ distributed_check ] = check_multi -r 15 $disttest $THRESHOLDS$"); \ 
	        $count;


### Example output

{{:check_multi:examples:distributed_extview.png|Distributed website monitoring}}
{{tag>host network operation remote service state}}
