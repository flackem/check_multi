## Prerequisite: extend buffer size in Nagios

Please increase your buffer limits and compile a new
nagios version (3.0a4 and above) following Ethans
statements from the [Nagios 3.x documentation](http://nagios.sourceforge.net/docs/3_0/pluginapi.html):

```
Plugin Output Length Restrictions
    
Nagios will only read the first 4 KB of data that a plugin returns. 
This is done in order to prevent runaway plugins from dumping megs 
or gigs of data back to Nagios. This 4 KB output limit is fairly 
easy to change if you need. Simply edit the value of the
MAX_PLUGIN_OUTPUT_LENGTH definition in the include/nagios.h.in file 
of the source code distribution and recompile Nagios. There's 
nothing else you need to change!
```
