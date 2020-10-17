# check_multi commands



## 1. General format

The check_multi plugin is configured by a simple NRPE stylish ASCII config file.\\

#### Format
```<keyword> [ <tag> ] = <content>```

#### Elements

1. Supported keywords:
    * attribute
    * command
    * eval
    * eeval
    * info
    * livestatus
    * state
    * statusdat
2.  '#' comments are allowed, but only at the beginning of the lines and not in continuation lines
3.  empty lines are allowed
4.  spaces resp. white characters between all elements can provide better readability 





## 2. attribute: set variables and attributes

With the attribute command you can specify global variables and child check specific settings.

#### Format
```
attribute [ <global variable> ] = <global variable value>
attribute [ <tag>::<variable> ] = <child check value>
```

#### Elements
1.  **tag**:<br/> <tag> is the name of a particular child check. see command or eval.
2.  **global variable**:<br/> any -s variable, which you can set via command line, compare check_multi -hhh
3.  **child check / tag variable**:<br/>child check attributes, which can be seen via check_multi XML export (-r 256)

#### Examples

1.  Check /tmp/ permissions (should be writeable for everybody, but with sticky bit:
```
command   [ tmp_dir_permissions           ] = ls -ld /tmp
attribute [ tmp_dir_permissions::critical ] = "$tmp_dir_permissions$" !~ /^drwxrwxrwt/
```

2. Set global variable extinfo_in_status, this replaces nthe ewline between plugin_output and long_plugin_output by HTML `<br />` in order to present all check_multi output in the status view:

```attribute [ extinfo_in_status ] = 1```





## 3. command - Command definition

The command definition specifies the list of child plugin calls which should be executed by check_multi as parent.

### Format
```command [ <tag> ] = <plugin command line>```

### Elements

1.  **tag**:<br/>`<tag>` is a freely choosable expression and provides something like a primary key to identify the plugin call. Especially in large environments you should spent some consideration about a naming scheme.  Allowed characters: ```A–Za-z0–9_:```
2.  **plugin command line**:<br/> This is just a standard plugin command line.<br/>The directory or full path of the plugin does not have to be mentioned here, it will be either be the default ```/usr/local/nagios/libexec``` or can be specified on the check_multi [command-line](configuration/options.md) using the --libexec-switch.<br/>**New:** the standard PATH is evaluated for the execution of programs. Therefore the evaluation order is as follows: 
    - libexec-dir (default or specified with --libexec) 
    - PATH of Nagios user 
    - fully specified path of plugin or command 
3.  **Nagios Macros**<br/>are allowed here: eg. $HOSTNAME$ specifies the current name of the machine. This allows you to write flexible command files. 
4.  Note:<br/>the **order** of the command list determines the latter order of execution.
5.  **PNP**:<br/>If you want to specify a particular plugin  for [performance data](configuration/performance.md), use the label format ```command [ tag::plugin ]```. 




## 4. eval/eeval: perl code in check_multi

Eval is a powerful means to gather information from any source and create flexible plugin configurations.

*  **eval** just evaluates the given expression and stores the result in $`<tag>`$. There is no output.

*  **eeval** (speak: e(cho)eval) does the same as eval but prints the result in the output.  
  
### Format
`eval [ `<tag>` ] = `<perl expression>`
`eeval [ `<tag>` ] = `<perl expression>`

### Elements

*  **tag**:<br/>like in commands `<tag>` is a freely choosable expression and provides something like a primary key to identify the *eval* expression.

* **perl expression**:<br/> This can be an arbitrary perl expression.  
* **Return code**<br/>An eeval statement is a small perl script, and you can set the RC like in other perl scripts via the $? variable.<br/>Nevertheless it is a little bit special: you have to set the RC first and then, in the last statement, define the output of the eeval statement. Look into the following example:
  
```
eeval [ RC_CRITICAL_output_xyz ] =
   # the RC has to be shifted to the high byte of $?     
   $? = $CRITICAL << 8;
   # the output itself is the return value (well, that's not quite intuitive ;))
   return "xyz";
```

### Examples
Find more examples for eval and eeval [here](eval.md). 


## 5. info: provide information in check_multi

The info command is the door to add information to check_multi. 

If you did it with dummy command / echo or dummy eval commands, the disadvantage was that every command bears its own status. And documentation should not show any status.

### Format  
There are multiple forms of info commands:
`info [ tag::pre[_`<state>`  ] = this text comes before a plugin output`
`info [ tag::post[_`<state>` ] = and this text comes after the plugin output\nnewlines are allowed`
  
| Command                     | Position             | Only if state is  | 
| -------                     | --------             | ----------------  | 
| info [ TAG::pre           ] | before plugin output | one of all states | 
| info [ TAG::pre_ok        ] | before plugin output | OK                | 
| info [ TAG::pre_warning   ] | before plugin output | WARNING           | 
| info [ TAG::pre_critical  ] | before plugin output | CRITICAL          | 
| info [ TAG::post_unknown  ] | before plugin output | UNKNOWN           | 
| info [ TAG::post          ] | after  plugin output | one of all states | 
| info [ TAG::post_ok       ] | after  plugin output | OK                | 
| info [ TAG::post_warning  ] | after  plugin output | WARNING           | 
| info [ TAG::post_critical ] | after  plugin output | CRITICAL          | 
| info [ TAG::post_unknown  ] | after  plugin output | UNKNOWN           | 

### Details

*  **tag**:<br/>like in commands `<tag>` is a freely choosable expression and provides something like a primary key to identify the *info* expression.<br/>Note: the child check which info is related to, must exist before the info command. Otherwise info is not able to add its pre or post attributes.\\ You will get an error message otherwise.

*  **4 infos max per check**:<br/>There may be multiple info lines for each check. 'info [ tag::pre ]' and 'info [ tag::post ]' commands will be displayed in any case, so you may have two info blocks before and two info blocks after, one for the generic info and one for the specific state info.

*  **Use raw content**:<br/>you don't need to use " or ' to enclose your info blocks, just print them as they are. Newlines will be translated into "`<br />`" in HTML mode.
  
  
  
  

## 6. livestatus: read info from livestatus socket

### Format
`livestatus [ `<tag>` ] = `<host>`:`<service>`
`livestatus [ `<tag>` ] = `<host>`

### Elements

*  **tag:**<br/>like in commands `<tag>` is a freely choosable expression and provides something like a primary key to identify the *eval* expression.

*  **host:**<br/>host on which the service is running.  

*  **service:**<br/>service_description of the wanted service.<br/>**Note:** Additional variables<br/>```check_multi -s livestatus=`</path/to/livestatus-socket>```

** Multiple Hosts / Services:**<br/>If you want to specify more hosts / services, use regular expressions, which are perl like enclosed in '/'<br/>On the other hand: if you don't use slashes, the expression is taken literally.  

**/host[289]/**<br/>e.g. means host2, host8 and host9, while **host123** just means host123.
Another Example: `livestatus [ web ] = /srv.*/:httpd`

Let's assume that you have three webservers, called h1, h2 and h3, and each of them has a service ''httpd''.
*check_multi* now expands the child check ''web'' to three webservices as follows:
```
livestatus [ web_h1_httpd ] = h1:httpd
livestatus [ web_h2_httpd ] = h2:httpd
livestatus [ web_h3_httpd ] = h3:httpd
```

The new tags are built like this:```<tag>_<host>_<service>```


You can also specify services with regular expressions.

Question at the end: what will happen, if you specify the following? ```livestatus [ all ] = /.*/:/.*/```
Yes: all services in your installation will be combined within one check_multi call...

This will most likely break your [Nagios buffer sizes](installation.md) and it's not really reasonable ;-). But it shows how this expansion can work.  




##  7. state: state definition

First of all: For the default function of *check_multi* the state definition feature is *not* needed ;-).

The state definition specifies how the results of the child plugin calls should be evaluated. The standard or builtin evaluation looks for any non OK state and returns the state with the highest severity.

The evaluation order is from best to worst: 
1. OK
2. UNKNOWN
3. WARNING
4. CRITICAL

### Format
```state [ <OK|UNKNOWN|WARNING|CRITICAL> ] = <expression>```

### Elements

1.  **state**:<br/>can be one of the standard Nagios states OK, UNKNOWN, WARNING and CRITICAL.
2.  **expression**:<br/>a logical expression in Perlish style determines when the given state evaluates to true or false.

### Examples

```(disk_root == CRITICAL || disk_opt == CRITICAL)```
    * [Perl operators](http://www.perl.com/doc/manual/html/pod/perlop.html) are allowed. Since the precedence of perl operators is sometimes a little bit sophisticated please use brackets extensively - this also provides better readability ;-).
    * check tags are replaced by their return codes, e.g. disk_root -> 2 (CRITICAL)
    * COUNT(`<state>`) is replaced by the number of child check results for the mentioned state. 

```COUNT(WARNING) -> 2```
    * COUNT(ALL) will be replaced by the number of checks, e.g. for rules like this:

```state [ CRITICAL ] = COUNT(CRITICAL) == COUNT(ALL)```
    * Note: all special words (COUNT, OK, UNKNOWN, WARNING, CRITICAL) can be used case-**in**sensitive, so there's no problem to write ''count(warning)''.  
**Examples**

#### Builtin standard states  
(evaluated in this order)

```
state [ OK       ] = 1
state [ UNKNOWN  ] = COUNT(UNKNOWN)  > 0
state [ WARNING  ] = COUNT(WARNING)  > 0
state [ CRITICAL ] = COUNT(CRITICAL) > 0
```

#### Ignore WARNING and UNKNOWN and only rise CRITICAL states:

```
state [ UNKNOWN  ] = (1==0)
state [ WARNING  ] = (1==0)
state [ CRITICAL ] = COUNT(CRITICAL) > 0
```

#### Clustering: only rise critical if *more* than one CRITICAL state encountered, otherwise raise WARNING:

```
state [ WARNING  ] = COUNT(WARNING) > 0 || COUNT(CRITICAL) > 0
state [ CRITICAL ] = COUNT(CRITICAL) > 1
```

#### Config file vs. command line:
All states can also be specified on the command line with options ''-o/-u/-w/-c `<state expression>`. The precedence in the state evaluation is 
 1.  Builtin evaluation
 2.  Config file
 3.  Command line






## 8. statusdat: read info from Nagios status.dat

### Format
```statusdat [ `<tag>` ] = `<host>`:`<service>```
(and since 2010/06/04)

```statusdat [ `<tag>` ] = `<host>```

### Elements

#### tag: 
Like in commands `<tag>` is a freely choosable expression and provides something like a primary key to identify the *eval* expression.

#### host:   
host on which the service is running.  

#### service:  
service_description of the wanted service.  
*Note:* the status.dat is normally taken from `<nagiosdir>`/var/status.dat.
If you want to specify another path, do it like this:
`check_multi -s status_dat=`</path/to/status.dat>`{sh}

### Examples

#### Multiple Hosts / Services: 
If you want to specify more hosts or services, use regular expressions, which are perl like enclosed in '/'

On the other hand: if you don't use slashes, the expression is taken literally.

#### /host[289]/
e.g. means host2, host8 and host9, while *host123* just means host123.

#### statusdat [ web ] = /srv.*/:httpd

Let's assume that you have three webservers, called h1, h2 and h3, and each of them has a service ''httpd''.\\  
*check_multi* now expands the child check ''web'' to three webservices as follows:
```
statusdat [ web_h1_httpd ] = h1:httpd
statusdat [ web_h2_httpd ] = h2:httpd
statusdat [ web_h3_httpd ] = h3:httpd
```
The new tags are built like this:```<tag>_<host>_<service>```.

You can also specify services with regular expressions.


Question at the end: what will happen, if you specify the following?  
```
statusdat [ all ] = /.*/:/.*/
```

Yes, indeed: all services in your status.dat will be combined within one check_multi call...

This will most likely break your [Nagios buffer sizes](installation.md) and it's not really reasonable ;-). But it shows how this expansion can work.