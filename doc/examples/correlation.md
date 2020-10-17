======= Correlation of existing service check results =======

The background of the following example is the check_cluster functionality, which allows to correlate several results of service checks. Since check_cluster only allows to just count the number of checks, it can be interesting to use the flexible check_multi state rules to evaluate these results.

The following snippet just shows a simple example for a two service clustering:

*  It uses the check_multi feature of specifying child checks via command line (-x clause)

*  Both services are visualized again, the name of the child is the service description

*  Nagios Ondemand Macros are used to get the information from Nagios

*  there are two state rules
    - WARNING: show WARNING if at least one child is critical
    - CRITICAL: show CRITICAL if 2 childs are critical
 
### Nagios service definition

	:::bash
	define service {
	        service_description  check_multi_evaluates_ondemand_macros
	        use                  local-service
	        check_command        check_multi! -r 43 \
	        -x 'command [ $SERVICEDESC:host1:service1$ ] = ( \
	                echo "$SERVICEOUTPUT:host1:service1$" && \
	                exit $SERVICESTATEID:host1:service1$ )'  \
	        -x 'command [ $SERVICEDESC:host2:service2$ ] = ( \
	                echo "$SERVICEOUTPUT:host2:service2$" && \
	                exit $SERVICESTATEID:host2:service2$ )'  \
	        -w 'COUNT(CRITICAL) >= 1 || COUNT(WARNING) >= 1' \
	        -c 'COUNT(CRITICAL) >= 2'
	        host_name            host1
	}

### Nagios screenshot

{{:check_multi:examples:correlation_2services.png|}}
