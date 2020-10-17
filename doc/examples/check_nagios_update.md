======= check_nagios_update =======

## Description

Ethan Galstad has introduced a version check in Nagios since December 2008. In my opinion this check should not be part of the CORE and for sure it should not be a opt-out design. 
It is really better to add this as a plugin, where the user has to decide if he adds such a check or not. 
 
## Call / Command line

check_multi -f check_nagios_update.cmd

[-s NAGIOS_DIR=/path/to/nagios]\\ [-s NAGIOS_STATS=/path/to/nagiostats]\\ [-s NAGIOS_VERSION=`<nagios version>`]\\ [-s NAGIOS_API=`<hostname of API server>`]\\ [-s VERSION_URL=`<url to versioncheck>`]\\ [-s TINY_CHECK=0|1]\\ [-s STABLE_ONLY=0|1]\\ [-s FIRST_CHECK=0|1]
 
## Parameters 

All parameters are optional - they're equipped with reasonable defaults. IMHO they only need to be changed if there are some changes within the api web side (which can be seen in the update code in `<nagiosdir>`/base/utils.c

*  NAGIOS_DIR - prints variable / input parameter /path/to/`<nagios directory>` - default: /usr/local/nagios

*  NAGIOS_STATS - prints variable / input parameter /path/to/nagiostats - default: /usr/local/nagios/bin/nagiostats

*  NAGIOS_VERSION - prints variable / input parameter current nagios version (default: version output of nagiostats)

*  NAGIOS_API - prints variable / input parameter internet address of nagios api server  (default: api.nagios.org)

*  VERSION_URL - prints variable / input parameter version url on api.nagios.org (default: /versioncheck/)

*  TINY_CHECK - prints variable / input parameter ??? 0 - no, 1 - yes (default: 1 - yes)

*  STABLE_ONLY - prints variable / input parameter stable or devel version? 0 - no, 1 - yes (default: 1 - yes)

*  FIRST_CHECK - prints variable / input parameter ??? 0 - no, 1 - yes (default: 1 - yes)

## Child checks

** all values below can be set as check_multi variables (-s VAR=VALUE)**
The first 8 checks only present the used variables and settings. The show begins in check 9, where the complete output of the HTTP session is presented. Check 10 parses the output of check 9 and determines finally, if a new Nagios version is available.
 1.  NAGIOS_DIR
 2.  NAGIOS_STATS
 3.  NAGIOS_VERSION
 4.  NAGIOS_API
 5.  VERSION_URL
 6.  TINY_CHECK
 7.  STABLE_ONLY
 8.  FIRST_CHECK
 9.  update_check - HTML output from api.nagios.org
 10.  update_available - checks the availability of an update and prints yes - WARNING, no - OK 

## Code: check_nagios_update.cmd

	:::sh
	# nagios_update.cmd
	# 
	# Copyright (c) Matthias Flacke 2009
	#
	# Call: check_multi -f nagios_update.cmd -s STABLE_ONLY=0
	# All eeval variables can be set via command line like in this example
	
	#--- local nagios settings
	eeval [ NAGIOS_DIR     ] = ("$NAGIOS_DIR$"     eq "") ? "/usr/local/nagios" : "$NAGIOS_DIR$"
	eeval [ NAGIOS_STATS   ] = ("$NAGIOS_STATS$"   eq "") ? "$NAGIOS_DIR$/bin/nagiostats" : "$NAGIOS_STATS$"
	eeval [ NAGIOS_VERSION ] = ("$NAGIOS_VERSION$" eq "") ? `$NAGIOS_STATS$ -m -d NAGIOSVERSION` : "$NAGIOS_VERSION$"
	
	#--- settings for api.nagios.org check
	eeval [ NAGIOS_API     ] = ("$NAGIOS_API$"     eq "") ? "api.nagios.org" : "$NAGIOS_API$"
	eeval [ VERSION_URL    ] = ("$VERSION_URL$"    eq "") ? "/versioncheck/" : "$VERSION_URL$"
	eeval [ TINY_CHECK     ] = ("$TINY_URL$"       eq "") ? "1" : "$TINY_URL$"
	eeval [ STABLE_ONLY    ] = ("$STABLE_ONLY$"    eq "") ? "1" : "$STABLE_ONLY$"
	eeval [ FIRST_CHECK    ] = ("$FIRST_CHECK$"    eq "") ? "1" : "$FIRST_CHECK$"
	
	#--- get output from nagios.org
	command [ update_check ] = \
	        check_http $NAGIOS_API$ -v \
	        -u 'http://$NAGIOS_API$$VERSION_URL$' \
	        -A Nagios/$NAGIOS_VERSION$ \
	        -P 'v=1&product=nagios&tinycheck=$TINY_CHECK$&stableonly=$STABLE_ONLY$&version=$NAGIOS_VERSION$&firstcheck=$FIRST_CHECK$'
	
	eeval   [ update_available ] = if ("$update_check$"=~/UPDATE_AVAILABLE=1/){ $?=$WARNING<<8; "yes" } else { $?=$OK<<8; "no" }


## Example output

	
	nagios@thinkpad:~/etc> check_multi -f nagios_update.cmd 
	OK - 10 plugins checked, 10 ok
	[ 1] NAGIOS_DIR /usr/local/nagios
	[ 2] NAGIOS_STATS /usr/local/nagios/bin/nagiostats
	[ 3] NAGIOS_VERSION 3.0.6
	[ 4] NAGIOS_API api.nagios.org
	[ 5] VERSION_URL /versioncheck/
	[ 6] TINY_CHECK 1
	[ 7] STABLE_ONLY 1
	[ 8] FIRST_CHECK 1
	[ 9] update_check POST http://api.nagios.org/versioncheck/ HTTP/1.0
	 User-Agent: Nagios/3.0.6
	 Connection: close
	 Content-Type: application/x-www-form-urlencoded
	 Content-Length: 70
	 
	 v=1&product=nagios&tinycheck=1&stableonly=1&version=3.0.6&firstcheck=1
	 
	 http://api.nagios.org:80http://api.nagios.org/versioncheck/ is 262 characters
	 STATUS: HTTP/1.1 200 OK

	 **** HEADER ****
	 Date: Fri, 01 May 2009 20:35:22 GMT
	 Server: Apache/2.2.3 (CentOS)
	 X-Powered-By: PHP/5.1.6
	 Content-Length: 70
	 Connection: close
	 Content-Type: text/plain; charset=UTF-8

	 **** CONTENT ****
	 UPDATE_AVAILABLE=0
	 UPDATE_VERSION=3.0.6
	 UPDATE_RELEASEDATE=2008-12-01
	 
	 HTTP OK HTTP/1.1 200 OK - 262 bytes in 0.339 seconds 
	[10] update_available no|check_multi::check_multi::plugins=10 time=0.583957 update_check::check_http::time=0.339372s;;;0.000000 size=262B;;;0 


