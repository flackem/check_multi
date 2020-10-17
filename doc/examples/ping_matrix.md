======= Ping Matrix =======

Nice idea to create a ping matrix (some ping hosts are pinging a list of gateways) and create a matrix out of these results.

The idea behind the check_multi implementation is to 
 1.  actively ping the hosts from the ping hosts
 2.  feed these results in passive service checks

TODO: nagvis representation

(idea: War Eagle, see [this thread in the monitoring-portal.org](http://www.monitoring-portal.org/wbb/index.php?page=Thread&threadID=15950).)

## Cooking list

This demo bases on a standard Nagios installation below /usr/local/nagios
It could be a good idea to
 1.  create a directory /usr/local/nagios/etc/ping_matrix
 2.  cp ping_matrix.cfg and ping_matrix.cmd into the dir
 3.  don't forget: add cfg_dir=/usr/local/nagios/etc/ping_matrix into your nagios.cfg
 4.  reload nagios
 5.  ...
 6.  wait some minutes (and have a look into /usr/local/nagios/etc/ping_matrix for newly created passive_...cfg)
 7.  when all passive service config files are there, reload nagios again, voila ;)

## ping_matrix.cfg

```
# Ping Matrix demo (following an idea of War Eagle in monitoring-portal.de)

#
# Copyright (c) 2010 Matthias Flacke (matthias.flacke at gmx.de)

# License: GPL v2
#

# this demo bases on a standard Nagios installation below /usr/local/nagios
# it could be a good idea to

# 1. create a directory /usr/local/nagios/etc/ping_matrix
# 2. put this file into the new dir

# 3. cp ping_matrix.cmd into the dir
# 4. don't forget: add cfg_dir=/usr/local/nagios/etc/ping_matrix into your nagios.cfg

#
# 5. reload nagios

# 6. wait some minutes (and have a look into /usr/local/nagios/etc/ping_matrix for newly created passive_...cfg)
# 7. when all passive service config files are there, reload nagios again, voila.

#
#--- service for mass pinging

define service {
        service_description     ping_matrix
        hostgroup_name          ping_matrix
        servicegroups           ping_matrix
        check_interval          1
        notifications_enabled   0
        check_command           feed_passive_nrpe!check_multi!-f /usr/local/nagios/etc/ping_matrix/ping_matrix.cmd -r 256 -s HOSTS=$HOSTNAME:ping_matrix:,$!-r 8192 -s checkresults_dir=/usr/local/nagios/var/spool/checkresults
        use                     generic-service
}
#--- helper service: generation of passive services

define service {
        service_description     ping_matrix_create_passive_services
        hostgroup_name          ping_matrix
        servicegroups           ping_matrix
        #check_interval          1440   # normally its sufficient to run it once (or per script)
        check_interval          1
        notifications_enabled   0
        notification_interval   0       # only to avoid warning messages during nagios config check
        check_command           check_multi!-f /usr/local/nagios/etc/ping_matrix/ping_matrix.cmd -r 2048 -s HOSTS=$HOSTNAME:ping_matrix:,$ -s service_definition_template=/usr/local/nagios/etc/ping_matrix/service_description_template.tpl > /usr/local/nagios/etc/ping_matrix/passive_service_ping_$HOSTNAME$.cfg && echo OK
        use                     generic-service
}

#--- servicegroup for the whole ping_matrix stuff

define servicegroup{
        servicegroup_name       ping_matrix
        alias                   Ping Matrix
}

#--- command definition for NRPE feed command

define command{
        command_name            feed_passive_nrpe
        command_line            $USER1$/check_nrpe -n -H $HOSTADDRESS$ -c "$ARG1$" -a "$ARG2$" | \
                                   $USER1$/check_multi $ARG3$ $ARG4$ $ARG5$
}

##--- command definition for SSH feed command

##--- TODO: manage check_by_ssh oddities
#define command{

#       command_name            feed_passive_ssh
#       command_line            /usr/bin/ssh $HOSTADDRESS$ -o 'StrictHostKeyChecking=no' -2 '$ARG1$' | \

#                                $USER1$/check_multi $ARG2$ $ARG3$ $ARG4$
#}

#--- hostgroup for all members

define hostgroup {
        hostgroup_name          ping_matrix
        alias                   Ping Matrix
}

#--- some hosts - add more if you like to put some load on your machine ;)

define host {
        host_name               host01
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host02
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host03
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host04
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host05
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host06
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host07
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host08
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host09
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
define host {
        host_name               host10
        address                 127.0.0.1
        hostgroups              ping_matrix
        use                     linux-server
}
```

## ping_matrix.cmd

	
```
	#
	# ping_matrix.cmd
	#
	# check_multi command file for adding ping checks
	# call: check_multi -f ping_matrix.cmd -s HOSTS=host1,host2,host3...
	# 
	# Copyright (c) 2010 Matthias Flacke (matthias.flacke at gmx.de)
	# License: GPL v2
	#
	#
	eval [ add_ping_checks ] = 
	   for (split(/,/,"$HOSTS$")) {
	      parse_lines("command [ ping_${_} ] = check_icmp -H ${_} -w 0.1,10% -c 500,20%");
	   }
```

