## FAQ - frequently answered questions


#### -H hostname missing

*  Question: Why is there no ''-H / --hostname'' option?

*  Answer: Because *check_multi* doesn't need any.

*check_multi* is a pure local plugin. It is normally called directly on the monitored server and only needs a adapted config file.\\ If you want to specify hostname options within this config file, you can use either localhost on the monitored server or - if you call the plugin on the Nagios server itself - Nagios variables like $HOSTNAME$ which will be interpreted by *check_multi*.\\ Another way is to specify variables via command line using the [--set-Option](configuration/options.md).

#### Embedded Perl (EPN)

*  Question: Is check_multi EPN capable?

*  Answer: No! The EPN implementation in Nagios is not easy to maintain in terms of debugging and quality control.

To be honest - I spent too much time into making check_multi and EPN happen :-\.

#### Examples

*  Question: Where can I find examples?

*  Answer: For the first try please have a look at the contributed [command file](http://svn.my-plugin.de/repos/check_multi/tags/current/contrib/check_multi.cmd). Another example can be found on the [process views](process_views.md) page.

####  HTML output only shows HTML tags

*  Question: I'm using the HTML output option (-r 2). But extinfo.cgi only shows a pile of HTML-Tags instead of the correct HTML output.

*  Answer: For the HTML output set the option *escape_html_tags=0* in your [cgi.cfg](http://nagios.sourceforge.net/docs/3_0/configcgi.html#escape_html_tags). See also the [report options](configuration/options.md)
Note: if cgi.cfg settings are changed, *no* Nagios restart is required. Changes will get into effect immediately after a browser reload 

#### check_multi and NSCA

*  Question: Why does check_multi not work with NSCA?

*  Answer1: NSCA is not multiline capable. It parses until it finds the first newline and then stops. Since check_multi highly depends on newlines this is a complete show stopper. We have to wait for a redesign of NSCA. :-\

*  Answer2: Actually it does ;-). When you use the HTML output option ''-r 2'' no newlines are used and NSCA will work fine.

#### PATH of plugins / commands in check_multi

*  Question: How does check_multi find its child plugins? Do I have to specify the fill path?

*  Answer: There is a clear defined order.
    - check_multi first looks into the default libexec directory, normally the same directory where check_multi is located
    - If this is not standard it can be specified via the [--libexec option](configuration/options.md). 
    - Then the nagios users PATH is searched. 
    - If anything else fails the location of a plugin can be specified with its full path.
  
#### Perfdata discarded - why that?

*  Question: Why does check_multi discard performance data?

*  Answer: Check_multi collects the performance data of multiple plugins and sources. Invalid perfdata could also invalidate other plugins perfdata, therefore it has to be sanitized.


*  Question: What does ''[perfdata discarded ...bad uom ',']'' mean?

*  Answer: Your LANG settings are incorrect - please use LANG=C or other LANG locale which provides proper '.'

#### Permissions / sudo

*  Question: How can I get need root permissions for the execution of a plugin?  

*  Answer: Basically this is the same procedure as for the execution each other plugin. The best method is to execute the command via [sudo](http://www.courtesan.com/sudo). For that you have to prepend the command line in the cmd file by ''sudo'' and adopt the sudoers configuration ''/etc/sudoers''.  


