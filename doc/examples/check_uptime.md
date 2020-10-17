## Check the uptime of a server from NAGIOS_LASTHOSTSTATECHANGE

```
# check_uptime.cmd

#
# Matthias.Flacke@gmx.de, 16.03.2009

#
# to be prepended to other checks

#
# Call:  check_multi -f check_uptime.cmd -f other.cmd -s HOSTNAME=`<hostname>`

#
#

eeval [ LASTHOSTSTATECHANGE ] = \
        if ($ENV{NAGIOS_LASTHOSTSTATECHANGE}) { \
                $ENV{NAGIOS_LASTHOSTSTATECHANGE}; \
        } else { \
                print "Cannot determine NAGIOS_LASTHOSTSTATECHANGE";  \
                exit 0; \
        }

eeval [ MIN_UPTIME ] = ("$MIN_UPTIME$") ? "$MIN_UPTIME$" : 300;
eeval [ UPTIME ] = \
        my $uptime=time-$LASTHOSTSTATECHANGE$; \
        if ($uptime > $MIN_UPTIME$ ) { \
                $uptime; \
        } else { \
                print "Host is up since $uptime seconds - no service checking before $MIN_UPTIME$ seconds uptime";  \
                exit 0; \
        }
```
