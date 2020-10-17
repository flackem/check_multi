# Macros

*check_multi* evaluates macros as Nagios does, e.g. $HOSTNAME$ or $HOSTADDRESS$. With this feature one cmd file can be used for multiple hosts:
	
```
	command[ network_ping ] = check_icmp -H $HOSTADDRESS$ -w 500,5% -c 1000,10%
```

The list of macros available in Nagios 3 can be viewed [here](http://nagios.sourceforge.net/docs/3_0/macrolist.html).

## Macros at runtime

For each command two values are stored after execution:
 1.  Returncode (RC) in the variable $STATE_`<command tag>`$
 2.  Command output in the variable $`<command tag>`$
These values can be used as macros in suksessive commands.

## Using macros from Nagios

Of course this macro substitution only works directly on the Nagios Server. If you are running checks on a remote host you can use ''-H localhost''. Or use the [--set-Option](configuration/options.md) to provide variables via command line:

```
check_multi -f `<xyz.cmd>` --set HOSTNAME=host123
```

Note: Macro names are case sensitive - e.g. ```-s HOSTNAME=host123``` is something different than ```-s hostname=host123```, in Nagios the first is to be referred as ```$HOSTNAME$``` while the latter is ```$hostname$```.
## Ondemand macros

Nagios ondemand macros (compare [here](http://nagios.sourceforge.net/docs/3_0/macros.html)) can be used by *check_multi* in order to reuse the states or any particular attributes from foreign host or service checks in the own check. Nagios needs the configuration info which data should be passed at runtime.

To illustrate this I will mention a short example. Our service is monitoring a web appliation called myapp. But additionally the state of the attached firewall mywall should be included. 
Two steps to do this:
1.  check_multi call:

```
check_multi -f myapp.cmd -s MYWALL_STATEID=$SERVICESTATEID:myhost:mywall$ -s MYWALL_OUTPUT="$SERVICEOUTPUT:myhost:mywall$"
```

2.  command file myapp.cmd:

```
# myapp.cmd
command [ myapp  ] = check_http -H myhost -u 'http://myapp'
command [ mywall ] = ( echo "$MYWALL_OUTPUT$"; exit $MYWALL_STATEID$ )
```

**Note**: Take care of the quoting here: the output string has to be included in quotes while the stateid may not (numerical RC).

The combined call of OUTPUT and STATEID provides a 1:1 presentation of the results of the mywall service without any need to reexecute the command for this service any more.
