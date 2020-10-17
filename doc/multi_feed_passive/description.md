# check_multi feeds passive checks (ALPHA!)

{{check_multi:multi_feeds_passive.png|}}


One of the major reasons for a *check_multi* based implementation are large environments where 

*  the number of Nagios servers should be reduced

*  the complexity of a distributed environment should be avoided

On the other hand the *check_multi* service drawback (''There can be only one'') sometimes is a vital disadvantage when 

*  heterogeneous groups are participating in the monitoring

*  one Nagios object is needed for every monitoring item (=check_multi child check).

This is the motivation for a improved implementation with

*  the standard check_multi plugin

*  an additional multi-check which feeds passive checks 

*  a small XML parsing event handler which receives the results of the multi-check

//Caveat: this implementation is alpha at the moment.

If you have comments, bug reports, suggestions, enhancements, please contact me

[Matthias Flacke](matthias.flacke@gmx.de) 2008/10/19 18:11// 



## Basic design

#### How does it work?
 1.  check_multi collects all checks from a host
 2.  An associated event_handler receives the child check data via XML
 3.  The event_handler feeds via external command interface (PROCESS_FILE) a bunch of passive checks
 4.  These passive checks have the same name like the check_multi child checks.

#### Advantages

*  The communication between Nagios server and client happens only once per machine but not once per check.

*  The multi check is active and therefore under Nagios scheduling control.

*  Since the particular services are passive they do not put load on the Nagios scheduling queue.

*  All services are nevertheless Nagios services, we have: Notification, Escalation, Reporting.

#### Disadvantages

*  More Complexity compared to a active service implementation (but less than a distributed setup ;-))

*  The configuration has to be set up, see [projects:check_multi:multi_feed_passive:description#generation_of_the_configuration](multi_feed_passive/description.md).

## The details

#### Prerequisites
 1.  **nagios.cfg**

remove `<'' and ''>` from illegal_macro_output_chars to allow XML output:`illegal_macro_output_chars=`~$&|'"`
 2.  **perl modules**

install XML::Simple, either from your Linux distribution or directly from [CPAN](http://search.cpan.org/perldoc?XML::Simple)
 3.  **cgi.cfg**

if not already done for check_multi - allow html output:`escape_html_tags=0`
#### check_multi feed service definition

*  Mandatory: ''is_volatile 1''

The volatile option has to be set, otherwise the event_handler will only be called when the status changes.

*  check_multi report option ''-r 263'':
    - Mandatory:      ''-r 256'' as XML output option
    - Convenient:     ''-r 2'' for pretty HTML output
    - Recommended:    ''-r 4'' for ERROR output 
    - last not least: ''-r 1'' for detailed results in the status line

*  Hint for very large setups: these feeding services could be placed in a dedicated Nagios instance to get additional performance if needed. This instance can also be used to control the distribution of the Nagios client and the multi configuration files.

*  Example:

```
define service {
        service_description     multi_feed
        host_name               host1
        check_command           check_multi!-f multi_small.cmd -r 263 -v
        event_handler           multi_feed_passive
        event_handler_enabled   1
        check_interval          5
        is_volatile             1
        use                     local-service
}
```

#### check_multi command file

Just as an example, your mileage may vary ;)
```
#--- some local checks on the nagios system
command[ disk ] = check_disk -w 5% -c 2% -p /
command[ load ] = check_load -w 5,4,3 -c 10,8,6
command[ swap ] = check_swap -w 90 -c 80
```

#### Passive service definition

*  Mandatory: ''passive_checks_enabled  1''

*  Mandatory: ''active_checks_enabled   0''

*  Example:
```
define service {
        service_description     `<child service tag>`
        host_name               `<hostname>`
        passive_checks_enabled  1
        active_checks_enabled   0
        check_command           check_dummy!0 "passive check"
        use                     local-service
}
```

#### multi_feed_passive event_handler

*  [multi_feed_passive](de/projects/check_multi/multi_feed_passive/script)

*  Code:
```
use strict;
#[...]removed GPL here ;)[...]

#--- XML module for XML extraction
use XML::Simple;
#

#--- CMD file for Nagios submission
my $cmdfile="/usr/local/nagios/var/rw/nagios.cmd";
#

#--- Command line parameters:
#--- 1. Hostname

#--- 2. Long Service Output
my $hostname=shift(@ARGV);
my $longserviceoutput=shift(@ARGV);

#--- strip long service output: take XML part and remove newlines

$longserviceoutput=~s/.*(`<PARENT>`.`<\/PARENT>`).*/\1/;
$longserviceoutput=~s/\\n//g;
#

#--- read check_multi output from XML structure
my $xmlref = XMLin($longserviceoutput);

#--- loop over children and create file for command submission

my $tmpfile="/tmp/submit_command_$$.txt";
open (TMP, ">$tmpfile") || die "cannot open tmpfile $tmpfile:$?";
foreach my $child (keys %{$xmlref->{CHILD}}) {
        printf TMP "[%d] PROCESS_SERVICE_CHECK_RESULT;%s;%s;%s;%s\n",
                time,
                $hostname,
                $child,
                $xmlref->{CHILD}->{$child}{rc},
                $xmlref->{CHILD}->{$child}{output};
}
close TMP;
#

#--- feed nagios command pipe
open(CMD,">$cmdfile") || die "cannot open cmd file $cmdfile:$?";
printf CMD "[%d] PROCESS_FILE;%s;%s",
        time,
        $tmpfile,
        1;              # delete submit_command_$$.txt afterwards
close CMD;
```

*  If you use another Nagios instance for the passive services, you have to adopt the location of the target cmd pipe file.

#### Troubleshooting

*  watch for ''PASSIVE SERVICE CHECK'' lines in your nagios.log

*  if you see the message ''Passive check result was received for service '%s' on host '%s', but the service could not be found!'', you have to double check the passive service definitions.



## Test installation

Just to get a feeling how it works, use the demo configuration:
 1.  install a fresh standard Nagios installation (from sources) under /usr/local/nagios.
 2.  unpack check_multi SVN tarfile [projects:check_multi:download](projects/check_multi/download) somewhere.
 3.  copy branches/multi_feed_passive directory to feed in nagios directory like this:`cp branches/multi_feed_passive /usr/local/nagios/feed/`
 4.  add the feed subdir as cfg_dir to nagios.cfg:`cfg_dir=/usr/local/nagios/feed`
 5.  do the necessary changes as shown in Prerequisites section of [projects:check_multi:multi_feed_passive:description#The details](projects/check_multi/multi_feed_passive/description#The details).
 6.  reload / restart Nagios: et voila :-P




If you want to put more load on your system, use the predefined hosts files and reload:

*  100 Hosts with 100 feed services and 1000 passive services:

`mv feed/etc/hosts_11-100.cfg.disabled feed/etc/hosts_11-100.cfg`

*  500 Hosts with 500 feed services and 5000 passive services:

`mv feed/etc/hosts_101-500.cfg.disabled feed/etc/hosts_101-500.cfg`




## Generation of the configuration

Generally there are two approaches for the generation of the configuration:
 1.  generate passive checks from the multi check
 2.  generate the multi check configuration from the existing passive checks
One example script which creates the passive child configs from the results of the XML check_multi plugin output, can be found [here](projects/check_multi/multi_feed_passive/create_child_services.pl)

Note: testing this script with nested check_multi checks showed some probs --- //[Matthias Flacke](matthias.flacke@gmx.de) 2008/10/26 09:19//.


## Links and Download

*  SVN repository: [http://svn.my-plugin.de/repos/check_multi/branches/multi_feed_passive](http://svn.my-plugin.de/repos/check_multi/branches/multi_feed_passive)

### TODO

*  catch possible errors:
    * no XML condition in create_child_services.pl
    * no complete output in long_plugin_output
