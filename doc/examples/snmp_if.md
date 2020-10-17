======= Multiple interfaces in a loop =======
```
#
# if.cmd

#
# call: check_multi -f if.cmd -s HOSTNAME=`<hostname>` -s snmp_community=`<community>`

#
snmp [ interfaces ] = $HOSTNAME$:1.3.6.1.2.1.2.1.0
eval [ expand_interfaces ] = 
        foreach my $interface (1 .. $interfaces$) {
                parse_lines("snmp [ if$interface ] = $HOSTNAME$:1.3.6.1.2.1.2.2.1.8.$interface");
        }
```
