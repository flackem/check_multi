## Options


### Usage

```check_multi -f <config file> | -x command  [-n name] [-t timeout] [-T TIMEOUT] [-r level] [-l libexec_path] [-s option=value] [-w <expr>] [-c <expr>] [-u <expr>] [-o <expr>] [-h][-v][-V]```

### -f, --filename

config file(s) which contain(s) commands to be executed

See the [special section](configuration/commands.md) for the format of this config file and compare the sample config file in the contrib directory.  

1.  You can specify multiple config files: ```-f `<file1>` -f `<file2>` ...```
2.  If `<file>` is a directory, all ```*.cmd``` files in this directory are included and parsed in alphabetical order.

### -n, --name

multi plugin name (shown in output)
  
default: none

This option can be used to do some descriptive tagging, e.g. SYSTEM, ORACLE, WEB etc.

### -t, --timeout

timeout for one command

default: 10

This option defines the timeout for a child plugin. 10 seconds is a often used default in Nagios plugins. Normally this value does not have to be changed.


### -T, --TIMEOUT

TIMEOUT for all commands

default: 60

This value (BIG **T** stands for the parent plugin, small *t* for the 
child plugins, please don't mix them ;-)) limits the overall plugin runtime.

Please note that Nagios itself has a timeout threshold for its
service checks (service_check_timeout=60). After this timeout 
Nagios kills the service check. 

If you specify a greater timeout
for the check_multi (BIG T), you consequently have to increase 
the nagios value for service_check_timeout accordingly. Otherwise you wouldn't see the cause for the check_multi timeout, but instead only the nagios timeout message.

The overall timeout (BIG T) provides a proper cancelling handling
for the child plugins: if the parent plugin notices that a child
plugin with its (small t) timeout extends the overall (BIG T) 
timeout, it does not execute it and reports this with the message
```plugin cancelled due to global timeout```. The child plugin then gets
the return code "UNKNOWN"

This mimic ensures the proper runtime of the parent plugin and 
a (at least UNKNOWN) result for all plugins.

### -l, --libexec

path to plugin

default: /usr/local/nagios/libexec

### -r, --report `<level>`

specify level of details in output (level is binary coded, just add 
all options)

default: 13


**Note**: you can also specify a string with combined numbers separated by '+', which should be easier to read ;-).

Example ```-r 13``` =  ```-r 1+4+8```

| Bit | Report-Option | Details / Output |
|---- |-------------- |----------------- |                                                                                                                
| 1|Service name |```24 plugins checked, 1 critical **(http)**, 1 warning **(disk_var)**, 0 unknown, 23 ok```|                                                                                                                                   
| 2|HTML output |see also [Screenshot extended info](screenshot/extended_info.md)<br/>If you use this HTML output option, be sure to set *escape_html_tags=0* in your cgi.cfg - otherwise you will see a lot of HTML tags ;-) |  
| 4|STDERR |If there is any STDERR output of the plugin it will be displayed in square brackets:<br/>```[No such file or directory]``` |                                                                                                           
 | 8|Performance data |Performance data is printed using [Multi labels](performance.md):<br/>```disk_root_warning::check_disk::/=10549MB;6047;9675;0;12094``` |                                                                                        
 | 16|Full state list |```MULTI CRITICAL - 16 plugins checked, 1 critical (disk_root_warning), 0 warning, 0 unknown, 14 ok```|                                                                                                           
 | 32|standard performance labels | Uses standard performance labels without Multi extension.<br /> This option is an alternative to option 8 |                                                                                                
 | 64| State label | OK,UNKNOWN,WARNING,CRITICAL state label is shown in front of child check output |                                                                                                                                          
 | 128|PNP action link | If there is some performance data available a PNP action URL (the star) is shown at each child check (HTML output option required) |                                                                                   
 | 256|XML data | Print the complete data of all checks in a structured XML tree. This data can be used in wrapper scripts to realize   customized output |                                                                                     
 | 512|Nagios2 compatibility | All output is displayed in 1 line<br/>```MULTI CRITICAL, disk_root_warning DISK CRITICAL - free space: / 925 MB (8% inode=82%);, top top - 13:47:31 up 4 days, 21:35,  3 users,  load average: 3.13, 3.01, 3.11```  |
 | 1024 | Notes Icon | Shows a notes icon before each child check.<br/>Use the option  ```-s notes_url=URL``` to specify the correct URL to your documentation  |                                                                                   
 | 2048 | Service definition | helper function to define passive services to be feeded by *check_multi* |                                                                                                                                     
 | 4096 | send_nsca | send all child checks as passive checks to the central Nagios server via send_nsca |                                                                                                                                     
 | 8192 | checkresults | send child checks as passive checks directly to the checkresults directory<br/>(very fast and more reliable than NSCA / command pipe) |                                                                                  
 | 16384 | encoded | print commands encoded (helper function) |                                                                                                                                                                                 
 | 32768 | condensed | hide all OK state checks and print only non OK states |                                                                                                                                                                  

### -s, --set

set several options: ```--set `<option>`=`<value>```` or ```-s `<option>`=`<value>````

If you need to set more than one option, do this by prepending **each** pair with its own ```-s``` phrase:

```$ check_multi -s opt1=val1 -s opt2=val2 ...```

All ```--set``` options are stored in environment as MULTI_`<varname>` and can be reused either as environment variable $MULTI_`<varname>` or as *check_multi* variable $`<varname>`$.

Special meaning (defaults **bold**):

| option                      | value                              | comment                                                                              | 
| --------------------------- | ---------------------------------- | -------------------------------------------------------------------  | 
| action_mouseover            | 1:true **0**:false                 | mouse triggers PNP popup chart                                                                                                   | 
| checkresults_dir            | `<nagiosdir>`/var/spool/checkresults | path to Nagios checkresults directory (direct insertion of checkresults)                                                         | 
| child_interval              | 0s                                 | time in seconds to sleep between child_checks, may be fraction of seconds                                                        | 
| cmdfile_update_interval     | 86400                              | update local config file copy (if config file is drawn via HTTP/FTP/...)                                                         | 
| collapse                    | **1**:true, 0:false                | provide JavaScript tree collapse for recursive HTML views                                                                        | 
| config_dir                  | `<nagiosdir>`/etc/check_multi        | path to check_multi configuration directory                                                                                      | 
| cumulate_max_rows           | 5                                  | number of rows which cumulate [ TAG ] shall display                                                                              | 
| cumulate_ignore_zero        | **1**:true 0:false                 | shall cumulate ignore zero values?                                                                                               | 
| empty_output_is_unknown     | **1**:true 0:false                 | shall empty plugin output be flagged as UNKNOWN?                                                                                 | 
| extinfo_in_status           | 1: true, **0**: false              | Prints multi view also on Nagios Status view (status.cgi). <br/>Note: this only works with HTML mode '-r 2'                         | 
| file_extension              | **cmd**                            | standard file extension for check_multi configuration files                                                                      | 
| ignore_missing_cmd_file     | 1: true, **0**: false              | complain if command file not found?                                                                                              | 
| illegal_chars               | '\r'                               | characters to be cleaned up from command files                                                                                   | 
| image_path                  | **/nagios/images**                 | *relative* URL to Nagios images, needed e.g. for PNP link icon                                                                 | 
| indent                      | ' '                                | string to indent child checks                                                                                                    | 
| indent_label                | **1**:true 0:false                 | determines if multi label length indentation should be used in recursive HTML view<br/> 0: only check number width will be indented | 
| libexec                     | `<nagiosdir>`/libexec                | directory where plugins reside, will be added to search PATH                                                                     | 
| livestatus                  | <nagiosdir/var/rw/live             | path to livestatus socket (Unix or TCP socket)                                                                                   | 
| loose_perfdata              | 1: true, **0**: false              | accept non-standard performance data, e.g. german commata                                                                        | 
| name                        | ""                                 | label to be shown in output, `<name>` OK```, ...                                                                                  | 
| no_checks_rc                | **UNKNOWN **                       | which RC should be provided if no checks are defined                                                                             | 
| notes_url                   | URL                                | see [Nagios notes_url](http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html#service)                                    | 
| persistent                  | 1: true, **0**: false              | run check_multi in persistent mode                                                                                               | 
| pnp_url                     | **```/nagios/pnp```**                | *relative* URL to PNP path, needed for PNP action URL                                                                          | 
| pnp_version                 | **0.6**, 0.4                       | PNP version (needed for mouseover paths)                                                                                         | 
| send_nsca                   | `<nagiosdir>`/bin/send_nsca          | /path/to/send_nsca binary                                                                                                        | 
| send_nsca_cfg               | `<nagiosdir>`/etc/send_nsca.cfg      | path to send_nsca.cfg configuration file                                                                                         | 
| send_nsca_srv               | `<NSCA server>`                      | name/IP address of NSCA server                                                                                                   | 
| send_nsca_port              | `<port number>`                      | port number of NSCA server                                                                                                       | 
| send_nsca_timeout           | 10s                                | timeout of NSCA transmission                                                                                                     | 
| send_nsca_delim             | ':'                                | delimiter between NSCA fields                                                                                                    | 
| service_definition_template | `<path>`                             | /path/to/template file where definition for passive feeded services is stored                                                    | 
| status_dat                  | `<nagiosdir>`/var/status.dat         | /path/to/status.dat                                                                                                              | 
| style_plus_minus            | `<HTML definition >`                 | HTML style definition for blue '+' / '-' characters                                                                              | 
| suppress_perfdata           | tag1,tag2,tag3...                  | analogue to Nagios option process_perf_data:<br/>the performance data of all commands which are listed here will not be reported     | 
| suppress_service            | tag1, tag2, tag3...                | suppress report for services tag1, tag2, tag3 ...                                                                                | 
| tag_notes_link              | URL                                | notes URL as link in the child checks TAG (caveat: quoting!)                                                                     | 
| target                      | **_self**                          | HTML target window to open HTML links                                                                                            | 
| tmp_dir                     | /tmp/check_multi                   | directory for temporary check_multi files                                                                                        | 
| tmp_dir_permissions         | octcal 1777                        | permissions for the creation of the check_multi tmp_dir                                                                          | 
| tmp_etc                     | /tmp/check_multi/etc               | directory for the local copies of remotely drawn configuration files                                                             | 
| verbose                     | 0-3, **0**                         | verbosity level, higher values than 1 are only recommended for debugging                                                         | 

### -x, --execute

specify all commands on cmdline:


``` -x 'command [ procs ] = check_procs' ```

 
``` -x 'statusdat [ webserver ] = web*:apache*' ```

 This is just a 1:1 copy of the [command definition](configuration/commands.md) or [eval definition](configuration/commands.md) or any other line of the config file.
### -w, --warning

definition of the criteria for the WARNING state


see [state definition](configuration/commands.md#7.-state:-state-definition)

### -c, --critical

definition of the criteria for the CRITICAL state


see [state definition](configuration/commands.md)

### -u, --unknown

definition of the criteria for the UNKNOWN state


see [state definition](configuration/commands.md)

### -o, --ok

definition of the criteria for the OK state


see [state definition](configuration/commands.md)

### -h, --help

print detailed help screen\\
 1.  -h   - major help options
 2.  -hh  - more detailed help options
 3.  -hhh - all help options 


### -v, --verbose

shows debug output


(multiple -v creates additional output)


### -V, --version

print version information
