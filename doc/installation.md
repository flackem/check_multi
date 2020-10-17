## For the impatient

 1.  [Download](download.md) your version of *check_multi*.
 2.  Untar the tarball and step into the check_multi directory.
 3.  Run the usual 3-step thing (valid for the 'default' Nagios installation in /usr/local/nagios):`# ./configure; make all; make install`
 4.  There are some examples in the sample-config directory, please have a look at them.
 5.  If you're not running a Nagios version later than 3.0a4 please setup a playground with the newest nagios version. Follow the hints  [here](installation.md).
 6.  Copy *check_multi* into your libexec directory and [integrate](configuration/nagios.md) *check_multi* into your nagios configuration.
 7.  Reload Nagios one time for *check_multi* (you will never have to do this again ;-)).
 8.  Have a look into your [Services](screenshot/services.md) or [Extended Info](screenshot/extended_info.md) screens.
 9.  Enjoy! ;-) 


## Prerequisites

**Note**: for background information concerning buffer sizes, different transports and the multiline feature, please read also [this article](blog/2009/transports_buffers_and_multiline.md).

### Extend buffer size in Nagios

Please increase your buffer limits (MAX_PLUGIN_OUTPUT_LENGTH und MAX_INPUT_BUFFER).\\
It's no problem to increase both and compile a fresh nagios version following Ethans
comment from the [Nagios 3.x documentation](http://nagios.sourceforge.net/docs/3_0/pluginapi.html):

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


### NRPE

check_multi is just a normal plugin and can be called via NRPE like all other plugins.

One remark: you might have to change the buffer sizes in common.h MAX_INPUT_BUFFER and MAX_PACKETBUFFER_LENGTH.

For the guys with old NRPE releases (before May 8th 2007) out there: for multiline output NRPE v2.8 or higher is required.

**Caveat:** the PIPE buffer handling has been changed with the linux kernel 2.6.11. Before this kernel release linux kernels were only capable to transport 4096 bytes!
 
And: have a look onto [Ton Voons blog at the opsera site](http://opsview-blog.opsera.com/dotorg/2008/08/enhancing-nrpe.html): he provides a patch which allows NRPE to read subsequent blocks one after another. The charm in this solution lies in the fact, that you don't have to upgrade all NRPE daemons in the field at once

###  check_by_ssh 

check_by_ssh from the [official Nagios Plugins 1.4.10 and above](http://sourceforge.net/project/showfiles.php?group_id=29880) is multiline capable. For older versions please use this small {{check_multi:installation:check_by_ssh.c.patch|patch}}.

### NDO
Since July 1st 2009 ndomod.c supports long plugin output - please run a decent version of ndoutils.  

`<del>`NDO is not multiline capable at the moment, since the NEB module ndomod only passes the field output but not long_output to ndo2db.
This small {{:check_multi:installation:ndomod.c.patch|patch}} solves the problem.  
  
The buffersize for ndomod is defined by NDOMOD_MAX_BUFLEN in ndomod.h and the default value is 4096. If your check_multi output is longer that 4K, please change this value and recompile NDO.
`</del>`

## Installation details

The check_multi installation is autoconf based, which means you have to use ```configure``` to define your settings and gather system information.

 1. Get your check_multi copy
 2. Step onto the [download page](download.md). There are two methods getting the SW, either per 'svn' or per tarball: Download the Tarball and unpack it where you want:`tar xpzf check_multi_[...].tar.gz`{bash}
 2.  A new directory with the version information in its name is created. Step into it.
 3.  You will see some file like this:
```
nagios@thinkpad:~/check_multi-SVN280> ls -l
total 180
-rw-r--r-- 1 nagios nagios   9374 2009-10-22 21:49 Changelog
-rw-r--r-- 1 nagios nagios  17987 2009-10-22 21:49 LICENSE
-rw-r--r-- 1 nagios nagios   2859 2009-10-22 21:49 Makefile.in
-rw-r--r-- 1 nagios nagios    993 2009-10-22 21:49 README
-rw-r--r-- 1 nagios nagios    290 2009-10-22 21:49 THANKS
-rwxr-xr-x 1 nagios nagios 102048 2009-10-22 21:49 configure
-rw-r--r-- 1 nagios nagios  13061 2009-10-22 21:49 configure.ac
drwxr-sr-x 5 nagios nagios   4096 2009-10-23 23:14 contrib
drwxr-sr-x 4 nagios nagios   4096 2009-10-23 23:14 plugins
drwxr-sr-x 9 nagios nagios   4096 2009-10-23 23:14 sample_config
-rw-r--r-- 1 nagios nagios   3081 2009-10-22 21:49 subst.in
```

check_multi itself resides in the plugins directory:
```
nagios@thinkpad:~/check_multi-SVN280> ls -l plugins
total 108
-rw-r--r-- 1 nagios nagios   478 2009-10-22 21:49 Makefile.in
-rwxr-xr-x 1 nagios nagios 95037 2009-10-22 22:07 check_multi.in
drwxr-sr-x 3 nagios nagios  4096 2009-10-23 23:14 t
```

 1.  There are some ''.in'' files. These files will be converted during the installation.
 2.  Now call the configure script. It is responsible for
    * customizing your copy of check_multi and setting defaults
    * gathering system information, e.g. the location of commands
 3.  If you want to know which options to use with configure, run ''./configure --help''.
	There are two main sections of commands:
    * directories
    * options
 4.  The most important directory setting is ''- -prefix''. It determines the 'root' directory of your *check_multi* installation.
 5.  There are numerous settings within the options section. Don't change options if you are unsure, most of the settings have reasonable defaults. For the standard installation under ''/usr/local/nagios'' you don't need any option.
 6.  Run `./configure [--option1=value1 ...]` Look for errors and correct them.
 7.  Makefiles have been created. Run `make all` to create scripts and config files.
 8.  Run tests with `make test` If these tests succeeded, you are ready for install. If not, it's most likely a configure problem. If you're sure that it's not having to do with configure issues, send me a [mail](matthias.flacke@gmx.de) with the output of the test.
 9.  Install the plugin on this host with `make install` This places the plugin under `<prefix>`/libexec''.
 10.  If you want to install check_multi on a remote host, there are multiple ways to distribute it: rcp, scp, rsync...
 11.  If you are interested in sample configuration and examples, run `make install-config` or for some contributions like a HTML aware notification script or a custom Nagios query CGI, run `make install-contrib`
 12.  That's all, enjoy ;-)



## Upgrade

An upgrade is just a new installation of your plugin with the same configure settings.


**Note**: If you want do not recall your configure settings, just run 
```
$ check_multi -V
check_multi: v$Revision: 289 $ $Date: 2009-10-31 13:56:01 +0100 (Sat, 31 Oct 2009) $ $Author: flackem $
    configure  '--prefix=/var/opt/nagios' '--with-config_dir=/etc/opt/nagios/check_multi'
```

As you see, this provides information for the version of check_multi *and* the configure command line.
No need to save config.log after installation.
