# Configuration Overloading

The feature to specify multiple [config files](configuration/options.md) for *check_multi* can be used to provide flexible configuration.
Especially in large environments this could save lots of efforts to generate a configuration.



### Parser secrets

To understand this *configuration overloading* we have to take a look into the implementation of the configuration file parser. Whenever this parser reads a 'command' line like the following

```	
	# foo.cmd
	command [ foo ] = /bin/echo is foo
```

it looks into its repository and searches for any command with name 'foo'. If there isn't any it stores the command into the repository. But if there is already a command called 'foo' the parser overloads the former command with the current command.

We now will see how we can use this behaviour to simplify our configuration.


### Overloading

If we have a second file called ''bar.cmd'' which contains the following definition

```
	# bar.cmd
	command [ foo ] = /bin/echo is bar
```

and we load this file just after the previous command file ''foo.cmd'' then the parser finds the already stored ''foo'' command (''/bin/echo is foo'') and overwrites it with the command ''/bin/echo is bar''.


### Small debug session

```  
	nagios ~> libexec/check_multi -f foo.cmd -r 0
	 OK - 1 plugins checked, 0 critical, 0 warning, 0 unknown, 1 ok
	[ 1] foo is foo
	nagios ~> libexec/check_multi -f bar.cmd -r 0
	 OK - 1 plugins checked, 0 critical, 0 warning, 0 unknown, 1 ok
	[ 1] foo is bar
	nagios ~> libexec/check_multi -f foo.cmd -f bar.cmd -r 0
	 OK - 1 plugins checked, 0 critical, 0 warning, 0 unknown, 1 ok
	[ 1] foo is bar
```

 1.  *check_multi* reads foo.cmd and executes ''echo foo''
 2.  bar.cmd is executed and shows ''bar''
 3.  foo.cmd contents are overloaded by bar.cmd: *check_multi* shows ''bar''


### Overloading benefits

Now all Linux specific checks can go into Linux.cmd and all Solaris specific checks into SunOS.cmd. No problem to split also release dependent configuration. And if some special cases for particular hosts have to be configured: do it in hostxyz.cmd.

Example: Syslog should be checked if at least once a day there is some movement in it.
A ''Linux.cmd'' for example would contain the following line:

```	
	command [ syslog ] = check_file_age -c 86400 /var/log/messages
```

and ''Solaris.cmd'' would of course search the syslog in the directory /var/adm.

```	
	command [ syslog ] = check_file_age -c 86400 /var/adm/messages
```

And last not least our ''hostxyz.cmd'' should **not** monitor any syslog:

```	
	command [ syslog ] = /bin/echo "Check disabled, Matthias Flacke, 19.11.2007"
```

See below the appropriate lines in the Nagios configuration. The most important line in this context is 

''check_command check_multi!-f $_HOSTOS$.cmd!-f $HOSTNAME.cmd''

where the OS specific part is evaluated first and maybe it gets overloaded by the host specific part.

```	
	# overload.cfg
	define host{
	   host_name linuxhost
	   _OS       Linux
	}
	define host{
	   host_name solarishost
	   _OS       SunOS
	}
	define host
	   host_name specialhost
	   _OS       SunOS
	}
	define command {
	   command_name check_multi
	   command_line $USER1$/check_multi $ARG1$ $ARG2$ $ARG3$ $ARG4$
	}
	define service
	   name          system_checks
	   check_command check_multi!-f $_HOSTOS$.cmd!-f $HOSTNAME$.cmd
	}
```
