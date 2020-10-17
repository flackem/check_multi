======= Perfdata hack =======

	
```
	# perfdata_hack.cmd
	command [ eins   ] = /bin/echo "1|oins=1"
	command [ zwei   ] = /bin/echo "2|zwoa=2"
	eeval   [ gsuffa ] = \
	        my $eins=$cmds{1}{performance}; $eins=~s/.*=(.*)/$1/; \
	        my $zwei=$cmds{2}{performance}; $zwei=~s/.*=(.*)/$1/; \
	        my $gsuffa=$eins + $zwei; \
	        "$gsuffa|gsuffa=$gsuffa";
```

```
$ ../libexec/check_multi -f perfdata_hack.cmd 
OK - 3 plugins checked, 3 ok
[ 1] eins 1
[ 2] zwei 2
[ 3] gsuffa 3|check_multi::check_multi::plugins=3 time=0.011461 eins::/bin/echo::oins=1 zwei::/bin/echo::zwoa=2 gsuffa::eval::gsuffa=3
```
