======= check_multi perfdata format =======
This page is more intended for developing information ;)


*  The general problem of check_multi performance data is that the child checks provide multiple performance token which have to be identified and assigned to the particular child checks. If you just queue these tokens after the '|' char, it will not be separatable any more.


*  For this purpose the check_multi perfdata header is designed. It takes profit from the fact that there is no further rule how to provide performance labels. The 'classical' performance label is just a token before the '=' like this: ''label=data''

check_multi extends this label with
    - Name of Child check
    - Separation by '::'
    - Name of plugin


*  Example: the format of an standard check_multi perfdata token is

''system_swap::check_swap::swap=1786MB;0;0;0;2048''
    - system_swap - Tag of check_multi child check
    - check_swap - plugin name
    - swap=... - classical performance data


*  The complete check_multi performance data stream is also well structured. Each check_multi stream begins with a perfdata stream for the multi parent check, containing perfdata for the number of child checks and the overall runtime of the whole check. 
    - the name of the check_multi parent check (default: check_multi)
    - the name of the plugin (always: check_multi)
    - Perfdata: plugins=`<n>` time=`<runtime elapsed>`


*  Example for check_multi perfdata header:

```
$ check_multi -x "command [ uname ] = uname -a" -n example_multi_check
example_multi_check OK - 1 plugins checked, 1 ok
[ 1] uname Linux localhost 2.6.25.9-0.2-default #1 SMP 2008-06-28 00:00:07 +0200 i686 i686 i386 GNU/Linux|example_multi_check::check_multi::plugins=1 time=0.020391
```

