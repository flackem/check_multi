======= schedule downtime =======


*  general idea: take check_http to communicate with nagios server

*  Shell script? Not a good idea, because the date string has to be calculated and the date command is not very portable. Additions of delta values may overlap a date border and this is pretty ugly to calculate in shell scripts ;)

*  Conclusion: take perl! ^_^


*  TODO: test check_http for HTTPS access...

*  TODO: use multiple mechanisms for access
     - use LWP
     - use WGET
     - use check_http

# Perl script

	:::perl
	#!/usr/bin/perl
	#
	# schedule_downtime - sending downtime request to nagios server
	#
	# The idea is gracefully taken from nagios_downtime by Lars Michelsen
	#
	# improvement: this script uses nagios plugin check_http for communication 
	# with nagios server and does not need any perl modules
	#
	# Copyright (c) 2009 Matthias Flacke (matthias.flacke at gmx.de)
	#
	# This program is free software; you can redistribute it and/or
	# modify it under the terms of the GNU General Public License
	# as published by the Free Software Foundation; either version 2
	# of the License, or (at your option) any later version.
	#
	# This program is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
	#
	# You should have received a copy of the GNU General Public License
	# along with this program; if not, write to the Free Software
	# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
	#
	# whoami
	my $MYSELF="schedule_downtime";
	# where are the local nagios plugins installed?
	my $LIBEXEC_DIR="/usr/local/nagios/libexec";
	# path of check_http plugin
	my $CHECK_HTTP="$LIBEXEC_DIR/check_http";
	# logfile location
	my $LOGFILE="/var/tmp/$MYSELF.log";
	# logfile location
	my $LOGMAXSIZE=100000;
	# local hostname
	my $HOSTNAME=`uname -n`; chomp $HOSTNAME;
	
	# Nagios server settings
	
	# name or IP address of the nagios host
	my $NAGIOS_HOST="localhost";
	# name of the user to access nagios
	my $NAGIOS_USER="nagiosadmin";
	# pwd of nagios user
	my $NAGIOS_PWD="nagiosadmin";
	# URL of the cmd.cgi on the nagios server
	my $CMD_URL="http://$NAGIOS_HOST/nagios/cgi-bin/cmd.cgi";
	# date_format specified in nagios.cfg (one of euro,us,iso8601,strict-iso8601)
	my $DATE_FORMAT="us";
	
	# Downtime settings
	
	# how long should the downtime last (in seconds)
	my $DELTA_SECONDS=3600;
	# fixed downtime? (flexible downtime ends after host is coming up again)
	my $FIXED_DOWNTIME=0;
	
	#--------------------------------------------------------------------------------
	#--- Subroutines ----------------------------------------------------------------
	#--------------------------------------------------------------------------------
	sub date_string {
	        my ($date_format,$delta_seconds)=@_;
	
	        # get current time and add delta_seconds
	        my  ($sec,$min,$hour,$day,$mon,$year)=localtime(time+$delta_seconds);
	
	        # return wanted date_format
	        if ($date_format eq "us") {
	                my $date=sprintf("%02d-%02d-%04d%%20%02d:%02d:%02d",
	                        $mon+1,$day,$year+1900,$hour,$min,$sec);
	        } elsif ($date_format eq "euro") {
	                my $date=sprintf("%02d-%02d-%04d%%20%02d:%02d:%02d",
	                        $day,$mon+1,$year+1900,$hour,$min,$sec);
	        } elsif ($date_format eq "iso8601") {
	                my $date=sprintf("%02d-%02d-%04d%%20%02d:%02d:%02d",
	                        $year+1900,$mon+1,$day,$hour,$min,$sec);
	        } elsif ($date_format eq "iso8601-strict") {
	                my $date=sprintf("%02d-%02d-%04d%%20%02d:%02d:%02d",
	                        $year+1900,$mon+1,$day,$hour,$min,$sec);
	        } else {
	                my $date="Invalid date format ($date_format)";
	        }
	}
	
	#--------------------------------------------------------------------------------
	#--- Main -----------------------------------------------------------------------
	#--------------------------------------------------------------------------------
	# get command line arg
	foreach my $arg (@ARGV) {
	        if ($arg=~/([^=]+)=(.+)/) {
	                eval("\$$1=$2");
	        } else {
	                print "Usage:\t$MYSELF [var=value...]\n\tInvalid argument $arg\n";
	                exit 3;
	        }
	}
	# check variables and prerequisites
	if (! -x $CHECK_HTTP) {
	        print "Nagios plugin check_http ($CHECK_HTTP) not found or not executable. Exit."; exit 3;
	} elsif ($DELTA_SECONDS <= 0) {
	        print "Invalid delta seconds specified ($DELTA_SECONDS). Exit."; exit 3;
	}
	
	# some output
	print "Executing nagios $MYSELF script... ";
	
	# calculate start and end of downtime
	$START_TIME=&date_string($DATE_FORMAT,0);
	$END_TIME=&date_string($DATE_FORMAT,$DELTA_SECONDS);
	#print STDERR "START_TIME:$START_TIME END_TIME:$END_TIME\n";
	
	# check_http url
	my $CMD_STRING=
	        "cmd_typ=55" . 
	        "&cmd_mod=2" .
	        "&host=$HOSTNAME" . 
	        "&com_author=$NAGIOS_USER" .
	        "&com_data=Downtime%20scheduled%20from%20host%20$HOSTNAME%20via%20$MYSELF%20script" .
	        "&start_time=$START_TIME" .
	        "&end_time=$END_TIME" .
	        "&fixed=$FIXED_DOWNTIME" . 
	        "&hours=" . int($DELTA_SECONDS/3600) . 
	        "&minutes=" . int(($DELTA_SECONDS%3600)/60) . 
	        "&trigger=0" .
	        "&child_options=0" . 
	        "&btnSubmit=Commit";
	my $EXPECT_STRING="Your command request was successfully submitted to Nagios for processing";
	
	# rotate logfile if necessary
	if (-f $LOGFILE && -s $LOGFILE > $LOGMAXSIZE) {
	        unlink "$LOGFILE.old" if (-f "$LOGFILE.old");
	        rename "$LOGFILE","$LOGFILE.old";
	}
	
	# schedule downtime via check_http
	`$CHECK_HTTP -v -H $NAGIOS_HOST -u "$CMD_URL?$CMD_STRING" -a "$NAGIOS_USER:$NAGIOS_USER" -s "$EXPECT_STRING" >> $LOGFILE`;
	
	# get check_http RC and exit accordingly
	my $RC=$?>>8;
	if ($RC == 0) {
	        print "done.\n";
	        exit 0;
	} else {
	        print "error setting downtime: RC $RC - (see $LOGFILE)\n";
	        exit 1;
	}


======= check_multi version =======

### SystemV exit script

	:::bash
	#!/bin/sh
	#
	# SysV exit script for setting downtime on Nagios server
	# (idea taken from downtime script from Lars Michelsen - thanks!)
	#
	# Copyright (c) Matthias Flacke, 14.02.2009
	#
	NAGIOS_DIR="/usr/local/nagios"
	LIBEXEC_DIR="$NAGIOS_DIR/libexec"
	COMMAND_FILE="$NAGIOS_DIR/etc/downtime.cmd"
	CHECK_HTTP="$LIBEXEC_DIR/check_http"
	CHECK_MULTI="$LIBEXEC_DIR/check_multi"
	LOGFILE="/var/tmp/downtime.log"
	#
	#--- check variables and prerequisites
	if [ ! -d $NAGIOS_DIR ]; then
	        echo "Nagios directory ($NAGIOS_DIR) not found. Exit."; exit 1
	elif [ ! -x $CHECK_HTTP ]; then
	        echo "Nagios plugin check_http ($CHECK_HTTP) not found or not executable. Exit."; exit 2
	elif [ ! -x $CHECK_MULTI ]; then
	        echo "Nagios plugin check_multi ($CHECK_MULTI) not found or not executable. Exit."; exit 3
	elif [ ! -f $COMMAND_FILE ]; then
	        echo "Command file ($COMMAND_FILE) not found. Exit."; exit 4
	fi
	#
	#--- run downtime script 
	case "$1" in
	        stop)
	                echo -n "Executing nagios_downtime script... "
	                $CHECK_MULTI -f $COMMAND_FILE -v >> $LOGFILE
	                if [ $? -eq 0 ]; then
	                        echo "done."
	                        exit 0
	                else
	                        echo "error setting downtime (see $LOGFILE)"
	                        exit 1
	                fi
	                ;;

	        *)
	                echo "Usage: $0 {stop}"
	                exit 1
	                ;;
	esac


### check_multi command file

	:::perl
	#
	# downtime.cmd
	# Copyright (c) Matthias Flacke, 14.2.2009
	#
	# idea taken from downtime script from Lars Michelsen - thanks!
	# https://www.nagiosforge.org/gf/project/nagios_downtime
	#
	# to be called on a remote host which is going down
	# best practice: include call into SysV startup script
	#
	# Call: check_multi -v -f downtime.cmd -s NAGIOS_HOST=`<nagios_host>` -s HOSTNAME=`<local host>` -s NAGIOS_USER=`<username>` -s CMD_CGI_URL=`<url>` -s DATEFORMAT=`<us|euro>`
	
	#--- some vars
	eeval [ NAGIOS_HOST ] = ("$NAGIOS_HOST$" eq "") ? "localhost" : "$NAGIOS_HOST$"
	eeval [ HOSTNAME    ] = ("$HOSTNAME$" eq "") ? "localhost" : "$HOSTNAME$"
	eeval [ NAGIOS_USER ] = ("$NAGIOS_USER$" eq "") ? "nagiosadmin" : "$NAGIOS_USER$"
	eeval [ CMD_CGI_URL ] = "http://$NAGIOS_HOST$/nagios/cgi-bin/cmd.cgi"
	
	#--- date and time routines
	eeval [ DATEFORMAT  ] = ("$DATEFORMAT$" eq "") ? "us" : "$DATEFORMAT$"
	eeval [ DOWNTIME_HOURS ] = ("$DOWNTIME_HOURS$" eq "") ? "2" : "$DOWNTIME_HOURS$"
	eeval [ TODAY       ] = \
	        my  (undef,undef,undef,$dom,$mon,$year,undef,undef,undef)=localtime(time);\
	        if ("$DATEFORMAT$" eq "us") {\
	                my $date=sprintf("%02d-%02d-%04d",$mon+1,$dom,$year+1900);\
	        } elsif ("$DATEFORMAT$" eq "euro") {\
	                my $date=sprintf("%02d-%02d-%04d",$dom,$mon+1,$year+1900);\
	        } else {\
	                my $errormsg="Error: invalid date format $DATEFORMAT$ specified";\
	        }
	eeval [ STARTTIME   ] =\
	        my  ($sec,$min,$hour)=localtime(time);\
	        my $starttime=sprintf("%02d:%02d:%02d\n",$hour,$min,$sec);
	eeval [ ENDTIME     ] =\
	        my  ($sec,$min,$hour)=localtime(time);\
	        my $endtime=sprintf("%02d:%02d:%02d\n",$hour+$DOWNTIME_HOURS$,$min,$sec);
	
	#--- schedule downtime
	command [ downtime  ] = check_http -v -H $NAGIOS_HOST$ -u '$CMD_CGI_URL$?cmd_typ=55&cmd_mod=2&host=$HOSTNAME$&com_author=$NAGIOS_USER$&com_data=Downtime%20scheduled%20from%20host%20$HOSTNAME$%20via%20startup%20script&trigger=0&start_time=$TODAY$%20$STARTTIME$&end_time=$TODAY$%20$ENDTIME$&fixed=0&child_options=0&btnSubmit=Commit' -a $NAGIOS_USER$:$NAGIOS_USER$ -s 'Your command request was successfully submitted to Nagios for processing'


### Example output

	
	--------------------------------------------------------------------------------
	Plugin output
	--------------------------------------------------------------------------------
	OK - 10 plugins checked, 10 ok
	[ 1] NAGIOS_HOST localhost
	[ 2] HOSTNAME localhost
	[ 3] NAGIOS_USER nagiosadmin
	[ 4] CMD_CGI_URL http://localhost/nagios/cgi-bin/cmd.cgi
	[ 5] DATEFORMAT us
	[ 6] DOWNTIME_HOURS 2
	[ 7] TODAY 02-14-2009
	[ 8] STARTTIME 14:41:46
	[ 9] ENDTIME 16:41:46
	[10] downtime  Produced by Nagios (http://www.nagios.org).  Copyright (c) 1999-2007 Ethan Galstad. 
	
	--------------------------------------------------------------------------------
	No   Name           Runtime  RC Output
	--------------------------------------------------------------------------------
	[ 1] NAGIOS_HOST    0.0002s   0 localhost
	[ 2] HOSTNAME       0.0001s   0 localhost
	[ 3] NAGIOS_USER    0.0002s   0 nagiosadmin
	[ 4] CMD_CGI_URL    0.0001s   0 http://localhost/nagios/cgi-bin/cmd.cgi
	[ 5] DATEFORMAT     0.0002s   0 us
	[ 6] DOWNTIME_HOURS 0.0002s   0 2
	[ 7] TODAY          0.0006s   0 02-14-2009
	[ 8] STARTTIME      0.0003s   0 14:41:46
	[ 9] ENDTIME        0.0003s   0 16:41:46
	[10] downtime       0.1411s   0 GET http://localhost/nagios/cgi-bin/cmd.cgi?cmd_typ=55&cmd_mod=2&host=localhost&com_author=nagiosadmin&com_data=Downtime%20scheduled%20from%20host%20localhost%20via%20exit%20script&trigger=0&start_time=02-14-2009%2014:41:46&end_time=02-14-2009%2016:41:46&fixed=0&child_options=0&btnSubmit=Commit HTTP/1.1
	 Host: localhost
	 User-Agent: check_http/v2030 (nagios-plugins 1.4.12)
	 Connection: close
	 Authorization: Basic bmFnaW9zYWRtaW46bmFnaW9zYWRtaW4=
	 
	 
	 http://localhost:80http://localhost/nagios/cgi-bin/cmd.cgi?cmd_typ=55&cmd_mod=2&host=localhost&com_author=nagiosadmin&com_data=Downtime%20scheduled%20from%20host%20localhost%20via%20exit%20script&trigger=0&start_time=02-14-2009%2014:41:46&end_time=02-14-2009%2016:41:46&fixed=0&child_options=0&btnSubmit=Commit is 1482 characters
	 STATUS: HTTP/1.1 200 OK

	 **** HEADER ****
	 Date: Sat, 14 Feb 2009 13:41:46 GMT
	 Server: Apache/2.2.8 (Linux/SUSE)
	 Connection: close
	 Transfer-Encoding: chunked
	 Content-Type: text/html

	 **** CONTENT ****
	 51b
	 `<html>`
	 `<head>`
	 `<link rel="shortcut icon" href="/nagios/images/favicon.ico" type="image/ico">`
	 `<title>`
	 External Command Interface
	 `</title>`
	 `<LINK REL='stylesheet' TYPE='text/css' HREF='/nagios/stylesheets/common.css'>`
	 `<LINK REL='stylesheet' TYPE='text/css' HREF='/nagios/stylesheets/cmd.css'>`
	 `</head>`
	 `<body CLASS='cmd'>`
	 
	 `<!-- Produced by Nagios (http://www.nagios.org).  Copyright (c) 1999-2007 Ethan Galstad. -->`
	 `<table border=0 width=100%>`
	 `<tr>`
	 `<td align=left valign=top width=33%>`
	 `<TABLE CLASS='infoBox' BORDER=1 CELLSPACING=0 CELLPADDING=0>`
	 `<TR>``<TD CLASS='infoBox'>`
	 `<DIV CLASS='infoBoxTitle'>`External Command Interface`</DIV>`
	 Last Updated: Sat Feb 14 14:41:46 CET 2009`<BR>`
	 Nagios&reg; 3.0.6 - `<A HREF='http://www.nagios.org' TARGET='_new' CLASS='homepageURL'>`www.nagios.org`</A>``<BR>`
	 Logged in as `<i>`nagiosadmin`</i>``<BR>`
	 `</TD>``</TR>`
	 `</TABLE>`
	 `</td>`
	 `<td align=center valign=top width=33%>`
	 `</td>`
	 `<td align=right valign=bottom width=33%>`
	 `</td>`
	 `</tr>`
	 `</table>`
	 `<P>``<DIV CLASS='infoMessage'>`Your command request was successfully submitted to Nagios for processing.`<BR>``<BR>`
	 Note: It may take a while before the command is actually processed.`<BR>``<BR>`
	 `<A HREF='javascript:window.history.go(-2)'>`Done`</A>``</DIV>``</P>`
	 `<!-- Produced by Nagios (http://www.nagios.org).  Copyright (c) 1999-2007 Ethan Galstad. -->`
	 `</body>`
	 `</html>`
	 
	 0
	 
	 
	 HTTP OK HTTP/1.1 200 OK - 0.119 second response time 
	
	
	--------------------------------------------------------------------------------
	State    Expression                                              Evaluates to
	--------------------------------------------------------------------------------
	OK       1                                                       TRUE
	UNKNOWN  COUNT(UNKNOWN)>0                                        FALSE
	WARNING  COUNT(WARNING)>0                                        FALSE
	CRITICAL COUNT(CRITICAL)>0                                       FALSE
	--------------------------------------------------------------------------------
	                                                Overall state => OK
	--------------------------------------------------------------------------------
	|check_multi::check_multi::plugins=11 time=0.199984 downtime::check_http:: time=0.118853s;;;0.000000 size=1482B;;;0 



### Sample for wget

	:::bash
	Thanks for the input - the following seems to work:
	
	Turn off service notification:
	
	 wget --quiet -O - --http-user=myuser --http-password=mypassword --post-data 
	'cmd_typ=23&cmd_mod=2&host=myhost&service=myservice&btnSubmit=Commit' 
	http://webserver/nagios/cgi-bin/cmd.cgi > /dev/null
	
	Turn on service notification:
	
	 wget --quiet -O - --http-user=myuser --http-password=mypassword --post-data 
	'cmd_typ=22&cmd_mod=2&host=myhost&service=myservice&btnSubmit=Commit' 
	http://webserver/nagios/cgi-bin/cmd.cgi > /dev/null
	
	I'd probably put the username and password in a ~nagios/.wgetrc file, so a 
	resulting Solaris crontab entry might look like:
	
	# turn on notfications
	/usr/bin/su - nagios -c "/usr/local/bin/wget --quiet -O - --post-data 
	'cmd_typ=23&cmd_mod=2&host=myhost&service=myservice&btnSubmit=Commit' 
	http://webserver/nagios/cgi-bin/cmd.cgi" > /dev/null 2>&1
	
	I was also able to do this on Windows using GnuWin wget:
	
	C:\PROGRA~1\GnuWin32\bin>wget --quiet -O - --post-data 
	"cmd_typ=23&cmd_mod=2&host=myhost&service=myservice&btnSubmit=Commit" 
	http://webserver/nagios/cgi-bin/cmd.cgi
	
	(.wgetrc becomes c:/progra~1/wget/etc/wgetrc)
	
	-e

