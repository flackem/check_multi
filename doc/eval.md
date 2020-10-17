## Expression evaluation

A powerful feature is *eval*. With this command file option you can evaluate arbitrary perl expressions and store the results either to reuse them lateron or to use the results in the final state evaluation.

There are two versions of eval:

*  eval - silent evaluation

*  eeval - *echo eval* - shows evaluation tag in extended plugin output

#### Syntax

`eval [ TAG ] = `<expression>`
`eeval [ TAG ] = `<expression>`

Continuation lines are supported with a trailing '\' at the end of the line ([Example here](eval.md)).   
  
This allows human beings to read and understand command files :-)

## Example 1: Linux network interface settings

The cmd file dynamically checks which is the default interface (i.e. the interface where the default route lies on). Then the settings (speed, duplex and auto negotiation) for this interface are collected.   

In the last step a warning is returned if the interface speed is not at least 100 MBit or if the duplex setting is not 'full'.

Additional feature: all network parameters, the interface name and its settings are displayed in the extended plugin output.   

```
# determine def_gw interface from /proc/net/route
command [ def_gw  ] = awk '$2 == "00000000" {print $1}' /proc/net/route
# get ethtool output and store it in temporary file
command [ ethtool ] = sudo /usr/sbin/ethtool $def_gw$ > /tmp/if_$def_gw$.txt \
                      && echo OK
# get interface settings using ethtool
command [ link    ] = awk '/Link detected:/    {print $3}' /tmp/if_$def_gw$.txt 
command [ speed   ] = awk '/Speed:/            {print $2}' /tmp/if_$def_gw$.txt 
command [ duplex  ] = awk '/Duplex:/           {print $2}' /tmp/if_$def_gw$.txt 
command [ autoneg ] = awk '/Auto-negotiation:/ {print $2}' /tmp/if_$def_gw$.txt 
# evaluate results
state   [ UNKNOWN ] =  "$def_gw$"  eq "" || ethtool != OK
state   [ WARNING ] = ("$speed$"   && "$speed$"  !~ /100/) || \
                      ("$duplex$"  && "$duplex$" !~ /FULL/i)
state   [ CRITICAL] =  "$link"     && "$link"    eq "no"
```

## Example 2: SUN prtdiag

SUNs hardware check program prtdiag is highly dependent on the particular kind of hardware it is running on. That makes it difficult to cover all different versions of HW in one check.
*check_multi* state evaluation provides an elegant way to cover different HW versions.

Nice side effect: the output of prtdiag is available in the extended plugin output. 

```
# prtdiag.cmd
# evaluates prtdiag output against error strings
eval [ hw_platform ] = `uname -i`
eeval [ prtdiag ] = `/usr/platform/$hw_platform$/sbin/prtdiag`
state [ CRITICAL ] = '$prtdiag$' =~/detected failure|fault: .* detected|Failed Field Replaceable Units|Detected System Faults|ERROR|FAILED|faulty|failed/
```

## Example 3: SAN data replication monitoring (HORCM)
Thanks to [Gerhard Lausser](gerhard.lausser@consol.de) for this example!

#### Environment
For the replication of SAN data in metropolitan clusters [HP provides a daemon solution](http://www.docs.hp.com/en/B7660-90014/ch05s04.html). The problem in monitoring these daemons are their changing names - it depends on the local installation which daemons have to be checked.

Fortunately the names of the horcmd daemons can be determined from the names of the daemon config files which are located under /etc: 
```
$ ls /etc/hor*
/etc/horcm.conf   /etc/horcm0.conf  /etc/horcm1.conf
```

#### Daemons

Following the config files two daemons should run:
```
$ ps -ef|grep horcmd
    root 401440      1   0   Jan 08      -  0:12 horcmd_01 
    root 467158      1   0   Jan 08      -  0:20 horcmd_00
```
Determination of the name of the calling process for the *check_multi* configuration:
```
$ /usr/bin/ps -eo 'stat uid pid ppid vsz pcpu comm args'|grep horcmd
A      0 401440      1   800   0.0 horcmgr  horcmd_01 
A      0 467158      1   804   0.0 horcmgr  horcmd_00`</code>`
The program itself is called ''horcmgr'' and its called with the parameter of the particular daemon.
```	
####  check_multi parent configuration
Parent configuration with two aims:  

* create child configuration in /tmp/horcmd_child.cmd
* add monitoring command statement

```
eval [ find_horcmd ] =                         \
	open HORCMD, ">/tmp/horcmd_child.cmd";               \
	foreach (glob "/etc/horcm*.conf") {                  \
	  /horcm(\d+)\.conf/ &&                              \
	  printf HORCMD "command [ horcmd%02d ] = check_procs -C horcmgr -a horcmd_%02d\n", $1, $1; \
	}                                                    \ 
	close HORCMD; 
	command [ horcmd ] = check_multi -f /tmp/horcmd_child.cmd
```
	
####  check_multi child configuration
The child configuration, dynamically created by the parent:
```
$ cat /tmp/horcmd_child.cmd
	command [ horcmd00 ] = check_procs -C horcmgr -a horcmd_00
	command [ horcmd01 ] = check_procs -C horcmgr -a horcmd_01
```
###  Command line test
The plugin output on the command line:

```
$ check_multi -f horcm_top.cmd
OK - 2 plugins checked, 2 ok
[ 1] find_horcmd 1
[ 2] horcmd OK - 2 plugins checked, 2 ok
[ 1] horcmd00 PROCS OK: 1 process with command name 'horcmgr', args 'horcmd_00'
[ 2] horcmd01 PROCS OK: 1 process with command name 'horcmgr', args 'horcmd_01'
|check_multi::check_multi::plugins=2 time=0.23 horcmd::check_multi::plugins=2 time=0.11
```