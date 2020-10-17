======= Variables =======

Special meaning (defaults **bold**):
 | option | value | comment | 
 | ------ | ----- | ------- | 






 | action_url              | URL, **""**           | see [Nagios action_url](http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html#service)                                   | 
 | ----------              | -----------           | ----------------------------------------------------------------------------------------------                                   | 
 | collapse                | **1**:true, 0:false   | provide JavaScript tree collapse for recursive HTML views                                                                        | 
 | extinfo_in_status       | 1: true, **0**: false | Prints multi view also on Nagios Status view (status.cgi).

Note: this only works with HTML mode '-r 2'                         | 
 | file_extension          | **cmd**               | standard file extension for check_multi configuration files                                                                      | 
 | ignore_missing_cmd_file | 1: true, **0**: false | complain if command file not found?                                                                                              | 
 | image_path              | **/nagios/images**    | *relative* URL to Nagios images, needed e.g. for PNP link icon                                                                 | 
 | indent_label            | **1**:true 0:false    | determines if multi label length indentation should be used in recursive HTML view

0: only check number width will be indented | 
 | no_checks_rc            | **UNKNOWN **          | which RC should be provided if no checks are defined                                                                             | 
 | notes_url               | URL                   | see [Nagios notes_url](http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html#service)                                    | 
 | pnp_path                | **''/nagios/pnp''**   | *relative* URL to PNP path, needed for PNP action URL                                                                          | 
 | suppress_perfdata       | tag1,tag2,tag3...     | analogue to Nagios option process_perf_data: the performance data of all commands which are listed here will not be reported     | 
 | target                  | **_self**             | HTML target window to open HTML links                                                                                            | 

