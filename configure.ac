#---
#--- configure.ac
#---
#--- (c) 2008-2011 Matthias Flacke
#---
#--- $Id$
#---
#--- plenty of configuration options 
#---
#--- prerequisites, credits and Nagios defaults
AC_PREREQ(2.59)
AC_INIT([check_multi], [0.26],[matthias.flacke@gmx.de])

AC_DEFINE([DEFAULT_NAGIOS_USER], [nagios], [Default Nagios User])
AC_DEFINE([DEFAULT_NAGIOS_GROUP], [nagios], [Default Nagios Group])

AC_PREFIX_DEFAULT(/usr/local/nagios)

#---
#--- package settings, some of them dynamic
PKG_NAME=check_multi
PKG_VERSION="$Rev$"
PKG_AUTHOR="$Author$"
PKG_HOME_URL="http://my-plugin.de/check_multi/"
PKG_REL_DATE="$Date$"
PKG_ID="$Id$"
COMMA=","

AC_SUBST(PKG_NAME)
AC_SUBST(PKG_VERSION)
AC_SUBST(PKG_AUTHOR)
AC_SUBST(PKG_HOME_URL)
AC_SUBST(PKG_REL_DATE)
AC_SUBST(PKG_ID)
AC_SUBST(COMMA)

#---
#--- checks for programs
AC_PROG_MAKE_SET
#AC_PATH_PROG([STRIP],[strip],[true])
AC_PATH_PROG(CHMOD,chmod)
AC_PATH_PROG(CP,cp)
AC_PATH_PROG(ETHTOOL,ethtool)
AC_PATH_PROG(GUNZIP,gunzip)
AC_PATH_PROG(ID,id)
AC_PROG_INSTALL
AC_PATH_PROG(MAILX,mailx)
AC_PATH_PROG(PERL,perl)

#---
if test "${exec_prefix}" = "NONE"; then
	exec_prefix="${prefix}"
fi

#--- too difficult to escape this - so define it as a variable before using it ;)
ACTION_URL="style='color:#4444FF;line-height:0.1em;font-size:1.5em;cursor:crosshair'"
AC_ARG_WITH(action_url,		[  

detail settings:
  --with-action_url=<URL>                  action URL (default:"")],action_url=$withval,action_url="")
AC_ARG_WITH(add_tag_to_list_entries,    [  --with-add_tag_to_list_entries=<0|1>     add tag as prefix to list entries (default:1)],add_tag_to_list_entries=$withval,add_tag_to_list_entries=1)
AC_ARG_WITH(action_mouseover,           [  --with-action_mouseover=<0|1>            show PNP chart popup triggered by mouseover (default:0)],action_mouseover=$withval,action_mouseover=0)
AC_ARG_WITH(cancel_before_global_timeout,			[  --with-cancel_before_global_timeout=<0|1>  cancel checks being *near* a timeout? (default:0)],cancel_before_global_timeout=$withval,cancel_before_global_timeout="0")
#--- too difficult to escape this - so define it as a variable before using it ;)
client_perl=no
AC_ARG_WITH(client_perl,                        [  --with-client_perl=<perl path>           sets perl cmdline / path (e.g. #!/usr/bin/perl)],client_perl=$withval,client_perl=no)
if test client_perl=no; then
       AC_PATH_PROG(client_perl,perl)
fi
AC_ARG_WITH(cmdfile_update_interval,	[  --with-cmdfile_update_interval=<seconds> interval to update command file(s) (default:86400, one day)],cmdfile_update_interval=$withval,cmdfile_update_interval=86400)
AC_ARG_WITH(collapse,			[  --with-collapse=<0|1>                    HTML javascript tree collapse option (default:1)],collapse=$withval,collapse="1")
AC_ARG_WITH(complain_unknown_macros,	[  --with-complain_unknown_macros=<0|1>       remove unknown macros silently, otherwise complain (default:1)],complain_unknown_macros=$withval,complain_unknown_macros=1)
AC_ARG_WITH(checkresults_dir,		[  --with-checkresults_dir=<path>           directory for Nagios checkresults (default:${localstatedir}/spool/checkresults)],checkresults_dir=$withval,checkresults_dir="${localstatedir}/spool/checkresults")
AC_ARG_WITH(child_interval,		[  --with-child_interval=<time>             time between child checks, fractions of seconds allowed (default:0.0)],child_interval=$withval,child_interval=0.0)
AC_ARG_WITH(config_dir,			[  --with-config_dir=<path>                 directory for check_multi configuration files (default:${sysconfdir}/check_multi)],config_dir=$withval,config_dir="${sysconfdir}/check_multi")
AC_ARG_WITH(cumulate_ignore_zero,	[  --with-cumulate_ignore_zero=<0|1>        cumulate ignores zero values (default:0)],cumulate_ignore_zero=$withval,cumulate_ignore_zero=0)
AC_ARG_WITH(cumulate_max_rows,	        [  --with-cumulate_max_rows=<N>             how many rows should be returned? (default:5)],cumulate_max_rows=$withval,cumulate_max_rows=5)
AC_ARG_WITH(empty_output_is_unknown,	[  --with-empty_output_is_unknown=<0|1>     should empty output be flagged as UNKNOWN (default:1)],empty_output_is_unknown=$withval,empty_output_is_unknown="1")
if test ethtool=""; then
	AC_ARG_WITH(ethtool,			[  --with-ethtool=</path/to/ethtool>        define path to ethtool (default:/sbin/ethtool)],ethtool=$ethtool,ethtool="/sbin/ethtool")
fi
AC_ARG_WITH(exec_open3,			[  --with-exec_open3=<0|1>                  use new exec method with function open3],exec_open3=$withval,exec_open3=0)
AC_ARG_WITH(extended_perfdata,		[  --with-extended_perfdata=<0|1>           provide extended check_multi perfdata],extended_perfdata=$withval,extended_perfdata=0)
AC_ARG_WITH(extinfo_in_status,		[  --with-extinfo_in_status=<0|1>           display check_multi output in status.cgi],extinfo_in_status=$withval,extinfo_in_status=0)
AC_ARG_WITH(feed_passive_autocreate,	[  --with-feed_passive_autocreate=<0|1>>    flag, if feed passive service definitions should be created automatically (default:1)],feed_passive_autocreate=$withval,feed_passive_autocreate="1")
AC_ARG_WITH(feed_passive_dir,		[  --with-feed_passive_dir=<path>           directory for automatically created feed passive service definitions (default:${sysconfdir}/check_multi/feed_passive)],feed_passive_dir=$withval,feed_passive_dir="${sysconfdir}/check_multi/feed_passive")
AC_ARG_WITH(feed_passive_dir_permissions,[  --with-feed_passive_dir_permissions=<octal perms> permissions for feed passive config dir (default:01777)],feed_passive_dir_permissions=$withval,feed_passive_dir_permissions="01777")
AC_ARG_WITH(findbin,			[  --with-findbin=<0|1>                     use Perl module FindBin for addressing plugins (default:1)],findbin=$withval,findbin=1)
AC_ARG_WITH(file_extension,		[  --with-file_extension=<ext>              default extension for check_multi command files (default:"cmd")],file_extension=$withval,file_extension="cmd")
AC_ARG_WITH(file_extension,		[  --with-file_extension=<ext>              default extension for check_multi command files (default:"cmd")],file_extension=$withval,file_extension="cmd")
AC_ARG_WITH(history,		        [  --with-history=<0|1>                     shall we store historical data for numerical checks? (default: 0)],history=$withval,history=0)
AC_ARG_WITH(history_maxsize,		[  --with-history_maxsize=<NN>              maximum number of history entries (default: 24*12 = 288)],history_maxsize=$withval,history_maxsize=288)
AC_ARG_WITH(history_maxage,		[  --with-history_maxage=<NN>               maximum age of history entries in seconds (default: 24*60*60 = 86400)],history_maxage=$withval,history_maxage=86400)
AC_ARG_WITH(history_minvalues,		[  --with-history_minvalues=<NN>            minimum of history entries, until a state rule gets valid (default: 3)],history_minvalues=$withval,history_minvalues=3)
AC_ARG_WITH(history_non_numerical_value,[  --with-history_non_numerical_value=<complain,extract> what shall be done with non numerical values? (default: complain)],history_non_numerical_value=$withval,history_non_numerical_value="complain")
AC_ARG_WITH(html_ascii_notification,	[  --with-html_ascii_notification=<0|1>     HTML output contains comment with ASCII output for notifications (default:0)],html_ascii_notification=$withval,html_ascii_notification=0)
AC_ARG_WITH(ignore_missing_cmd_file,	[  --with-ignore_missing_cmd_file=<0|1>     if missing cmd files should be ignored (default:0)],ignore_missing_cmd_file=$withval,ignore_missing_cmd_file="0")
AC_ARG_WITH(illegal_chars,		[  --with-illegal_chars=<chars>             characters to be stripped from command files (default:"\r")],illegal_chars=$withval,illegal_chars="\r")
AC_ARG_WITH(image_path,			[  --with-image_path=<URL>                  relative URL to nagios images (default:"/nagios/images")],image_path=$withval,image_path="/nagios/images")
AC_ARG_WITH(indent,			[  --with-indent=<char>                     ASCII output indent character (default:" ")],indent=$withval,indent=" ")
AC_ARG_WITH(indent_label,		[  --with-indent_label=<0|1>                indentation of child checks? (default:1)],indent_label=$withval,indent_label=1)
AC_ARG_WITH(livestatus, 		[  --with-livestatus=<path>                 /path/to/livestatus-socket (default:${localstatedir}/rw/live)],livestatus=$withval,livestatus="${localstatedir}/rw/live")
AC_ARG_WITH(loose_perfdata,		[  --with-loose_perfdata=1                  loose performance data (default:1)],loose_perfdata=$withval,loose_perfdata=1)
AC_ARG_WITH(map_host_down_state_to,	[  --with-map_host_down_state_to=1          RC to which host down state should be mapped (default:2)],map_host_down_state_to=$withval,map_host_down_state_to=2)
AC_ARG_WITH(map_host_unreachable_state_to,	[  --with-map_host_unreachable_state_to=1          RC to which host unreachable state should be mapped (default:3)],map_host_unreachable_state_to=$withval,map_host_unreachable_state_to=3)
AC_ARG_WITH(name,			[  --with-name=<name>                       default name for check_multi label (default:"")],name=$withval,name="")
AC_ARG_WITH(no_checks_rc,		[  --with-no_checks_rc=<RC>                 RC if no checks are specified (default:3-UNKNOWN)],no_checks_rc=$withval,no_checks_rc=3)
AC_ARG_WITH(notes_url,			[  --with-notes_url=<URL>                   notes URL (default:"")],notes_url=$withval,notes_url="")
AC_ARG_WITH(objects_cache,		[  --with-objects_cache=</path/to/objects.cache>    path to objects.cache (default:"${localstatedir}/objects.cache")],objects_cache=$withval,objects_cache="${localstatedir}/objects.cache")
AC_ARG_WITH(objects_cache_delimiter,	[  --with-objects_cache_delimiter=<char>    character to separate objects.cache results (default:",")],objects_cache_delimiter=$withval,objects_cache_delimiter=${COMMA})
AC_ARG_WITH(omd_environment,		[  --with-omd_environment=<0|1>             Run check_multi within OMD enviroment (default:0)],omd_environment=$withval,omd_environment=0)
AC_ARG_WITH(persistent,			[  --with-persistent=<0|1>                  persistency: saving of state data between two calls (default:0)],persistent=$withval,persistent=0)
AC_ARG_WITH(perfdata_pass_through,	[  --with-perfdata_pass_through=<0|1>       pass performance data through (default:0)],perfdata_pass_through=$withval,perfdata_pass_through=0)
AC_ARG_WITH(plugin_path,		[  --with-plugin_path=</path/to/plugins>    path to plugins (default:"/usr/local/nagios/libexec")],plugin_path=$withval,plugin_path="/usr/local/nagios/libexec")
AC_ARG_WITH(pnp_add2url,		[  --with-pnp_add2url=<URL addon>           URL addon for PNP (default:"")],pnp_add2url=$withval,pnp_add2url="")
AC_ARG_WITH(pnp_url,			[  --with-pnp_url=<URL>                     relative URL to PNP (default for PNP 0.6:"/pnp4nagios")],pnp_url=$withval,pnp_url="/pnp4nagios")
AC_ARG_WITH(pnp_version,		[  --with-pnp_version=<0.6|0.4>             PNP version (default: 0.6)],pnp_version=$withval,pnp_version="0.6")
AC_ARG_WITH(report,			[  --with-report=<NN>                       default report option (default:13)],report=$withval,report="13")
AC_ARG_WITH(report_inherit_mask,		[  --with-report_inherit_mask=<0|1>              report inherit mask (default:-1)],report_inherit_mask=$withval,report_inherit_mask="-1")
AC_ARG_WITH(signal_rc,			[  --with-signal_rc=<RC>                    RC if check_multi caught a signal default:3-UNKNOWN)],signal_rc=$withval,signal_rc=3)
AC_ARG_WITH(snmp_community,		[  --with-snmp_community=<community>        SNMP community (default:public)],snmp_community=$withval,snmp_community="public")
AC_ARG_WITH(snmp_port,			[  --with-snmp_port=<port>                  SNMP port (default:161)],snmp_port=$withval,snmp_port=161)
AC_ARG_WITH(status_dat,			[  --with-status_dat=<URL>                  path to nagios status.dat (default:"${localstatedir}/status.dat")],status_dat=$withval,status_dat="${localstatedir}/status.dat")
AC_ARG_WITH(style_plus_minus,		[  --with-style_plus_minus=<HTML code>      HTML style for plus/minus (default:$ACTION_URL)],style_plus_minus=$withval,style_plus_minus="$ACTION_URL")
AC_ARG_WITH(tag_notes_link,		[  --with-tag_notes_link=<URL>              documentation URL for child checks (default:"")],tag_notes_link=$withval,tag_notes_link="")
AC_ARG_WITH(target,			[  --with-target=<target_frame>             HTML target frame for URLs (default:_self)],target=$withval,target="_self")
AC_ARG_WITH(tmp_dir,			[  --with-tmp_dir=<path>                    /path/to/tmp_dir (default:/tmp/check_multi)],tmp_dir=$withval,tmp_dir="/tmp/check_multi")
AC_ARG_WITH(tmp_dir_permissions,	[  --with-tmp_dir_permissions=<octal perms> permissions of tmp_dir (default:01777)],tmp_dir_permissions=$withval,tmp_dir_permissions="01777")
AC_ARG_WITH(tmp_etc,			[  --with-tmp_etc=<path>                    /path/to/tmp_dir/etc (default:$tmp_dir/etc)],tmp_etc=$withval,tmp_etc="$tmp_dir/etc")
AC_ARG_WITH(use_hard_state,		[  --with-use_hard_state=<0|1>              use hard states for livestatus and statusdat checks (default:1)],use_hard_state=$withval,use_hard_state=1)
AC_ARG_WITH(parent_timeout,		[ 
major settings:
  --with-parent_timeut=<NN>                timeout for parent check (default:60)],parent_timeout=$withval,parent_timeout="60")
AC_ARG_WITH(child_timeout,		[  --with-child_timeout=<NN>                timeout for child checks (default:11)],child_timeout=$withval,child_timeout="11")
#AC_ARG_WITH(nagios_user,		[  --with-nagios-user=<user>                user name to run plugin (default:nagios)],nagios_user=$withval,nagios_user=nagios)
#AC_ARG_WITH(nagios_group,		[  --with-nagios-group=<group>              group name to run plugin (default:nagios)],nagios_group=$withval,nagios_group=nagios)
#--- taking user handling from Nagios plugins (default: install user)
INSTALL_OPTS=""
AC_ARG_WITH(nagios_user,		[  --with-nagios-user=USER                  installs executables with this user. Defaults to install user], INSTALL_OPTS="-o $withval")
AC_ARG_WITH(nagios_group,		[  --with-nagios-group=GROUP                installs executables with this group. Defaults to install user], INSTALL_OPTS="$INSTALL_OPTS -g $withval")
AC_ARG_WITH(nagios_name,		[  --with-nagios-name=<nagios|icinga>       set nagios name (there might be some clones ;)) (default:nagios)],nagios_name=$withval,nagios_name=nagios)
AC_ARG_WITH(verbose,			[  --with-verbose=<N>                       verbosity of check_multi (default:0)],verbose=$withval,verbose="0")
AC_ARG_WITH(verbose_fields,		[  --with-verbose_fields=<fieldlist>        comma separated list of attribute fields], verbose_fields=$withval, verbose_fields=[command,runtime])

#--- substitutions
AC_SUBST(INSTALL)
AC_SUBST(INSTALL_OPTS)
AC_SUBST(LIBEXECDIR)
AC_SUBST(ac_configure_args)
AC_SUBST(action_mouseover)
AC_SUBST(action_url)
AC_SUBST(add_tag_to_list_entries)
AC_SUBST(cancel_before_global_timeout)
AC_SUBST(child_interval)
AC_SUBST(checkresults_dir)
AC_SUBST(child_timeout)
AC_SUBST(cmdfile_update_interval)
AC_SUBST(collapse)
AC_SUBST(complain_unknown_macros)
AC_SUBST(contrib_dir)
AC_SUBST(config_dir)
AC_SUBST(cumulate_ignore_zero)
AC_SUBST(cumulate_max_rows)
AC_SUBST(datarootdir)
AC_SUBST(empty_output_is_unknown)
AC_SUBST(ethtool)
AC_SUBST(exec_open3)
AC_SUBST(extinfo_in_status)
AC_SUBST(extended_perfdata)
AC_SUBST(feed_passive_autocreate)
AC_SUBST(feed_passive_dir)
AC_SUBST(feed_passive_dir_permissions)
AC_SUBST(findbin)
AC_SUBST(file_extension)
AC_SUBST(gunzip)
AC_SUBST(history)
AC_SUBST(history_maxsize)
AC_SUBST(history_maxage)
AC_SUBST(history_minvalues)
AC_SUBST(history_non_numerical_value)
AC_SUBST(html_ascii_notification)
AC_SUBST(hostname)
AC_SUBST(ignore_missing_cmd_file)
AC_SUBST(illegal_chars)
AC_SUBST(image_path)
AC_SUBST(indent_label)
AC_SUBST(indent)
AC_SUBST(livestatus)
AC_SUBST(loose_perfdata)
AC_SUBST(map_host_down_state_to)
AC_SUBST(map_host_unreachable_state_to)
AC_SUBST(name)
AC_SUBST(no_checks_rc)
AC_SUBST(objects_cache)
AC_SUBST(objects_cache_delimiter)
AC_SUBST(omd_environment)
AC_SUBST(nagios_name)
AC_SUBST(notes_url)
AC_SUBST(parent_timeout)
AC_SUBST(perfdata_pass_through)
AC_SUBST(persistent)
AC_SUBST(plugin_path)
AC_SUBST(pnp_version)
AC_SUBST(pnp_add2url)
AC_SUBST(pnp_url)
AC_SUBST(report)
AC_SUBST(report_inherit_mask)
AC_SUBST(service_definition_template)
AC_SUBST(signal_rc)
AC_SUBST(snmp_community)
AC_SUBST(snmp_port)
AC_SUBST(status_dat)
AC_SUBST(style_plus_minus)
AC_SUBST(tag_notes_link)
AC_SUBST(target)
AC_SUBST(tmp_dir)
AC_SUBST(tmp_dir_permissions)
AC_SUBST(tmp_etc)
AC_SUBST(use_hard_state)
AC_SUBST(verbose)
AC_SUBST(verbose_fields)

AC_CONFIG_FILES(
	subst
	Makefile 
	contrib/Makefile
	plugins/Makefile
	plugins/t/Makefile
	sample_config/Makefile
)

AC_OUTPUT

#--- 
#--- substitution itself
$PERL subst plugins/Makefile
$CP   plugins/check_multi.in plugins/check_multi.windows.in
$PERL subst plugins/check_multi
$PERL subst plugins/check_multi.windows

$PERL subst plugins/t/Makefile
$PERL subst plugins/t/testopts.pm
$PERL subst plugins/t/10_check_multi.t
$PERL subst plugins/t/15_check_multi_history.t
$PERL subst plugins/t/20_check_multi_macros.t
$PERL subst plugins/t/30_check_multi_perfdata.t
$PERL subst plugins/t/50_check_multi_checkresults.t
$PERL subst plugins/t/60_check_multi_feeds_passive.t
$PERL subst plugins/t/70_check_multi_statusdat.t
$PERL subst plugins/t/80_check_multi_livestatus.t
$PERL subst plugins/t/90_extreme_tags.t
$PERL subst plugins/t/91_extreme_timeout.t

$PERL subst contrib/Makefile
$PERL subst contrib/status_query/Makefile
$PERL subst contrib/status_query/status_query.cgi
$PERL subst contrib/status_query/query_examples.html
$PERL subst contrib/notify_service/Makefile
$PERL subst contrib/notify_service/notify_service_html.sh

$PERL subst sample_config/Makefile
$PERL subst sample_config/multi_long/Makefile
$PERL subst sample_config/multi_long/multi_long.cmd
$PERL subst sample_config/cluster/Makefile
$PERL subst sample_config/cluster/download.cfg
$PERL subst sample_config/cluster/download.cmd
$PERL subst sample_config/cluster/download_my-plugin.cmd
$PERL subst sample_config/cluster/download_sourceforge.cmd
$PERL subst sample_config/nagiostats/Makefile
$PERL subst sample_config/nagiostats/nagiostats.cmd
$PERL subst sample_config/nagios_version/Makefile
$PERL subst sample_config/nagios_version/nagios_update.cmd
$PERL subst sample_config/nagiostats/check_multi_nagiostats.php
$PERL subst sample_config/start_process/Makefile
$PERL subst sample_config/start_process/start_process.cmd
$PERL subst sample_config/network_interface/Makefile
$PERL subst sample_config/network_interface/network_interface.cmd
$PERL subst sample_config/feed_passive/Makefile
$PERL subst sample_config/feed_passive/README
$PERL subst sample_config/feed_passive/gencfg
$PERL subst sample_config/feed_passive/feed_passive.cmd
$PERL subst sample_config/feed_passive/feed_passive.cfg
$PERL subst sample_config/feed_passive/service_definition.tpl
$PERL subst sample_config/cumulate/Makefile
$PERL subst sample_config/cumulate/flight_recorder.cmd
$PERL subst sample_config/cumulate/process_cpu.cmd
$PERL subst sample_config/cumulate/process_mem.cmd
$PERL subst sample_config/cumulate/process_rss.cmd
$PERL subst sample_config/cumulate/process_cmd.cmd
$PERL subst sample_config/cumulate/process_user.cmd

#---
#--- review options and show the user what he has broken ;)
AC_MSG_RESULT([
 -------------------------------------------------------------------
 --- $PKG_NAME configure summary (SVN ${PKG_VERSION}) 
 -------------------------------------------------------------------
])
echo " Release date   ${PKG_REL_DATE}"
echo " Author         ${PKG_AUTHOR}"
echo " Configure args :${ac_configure_args}"
echo
echo " --- Directories"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Install \${prefix}         $prefix])
AC_MSG_RESULT([ Exec \${exec_prefix}       $exec_prefix])
AC_MSG_RESULT([ Libexec directory         $libexecdir])
AC_MSG_RESULT([ CGI directory (sbin)      $sbindir])
AC_MSG_RESULT([ HTML directory (data)     $datarootdir])
AC_MSG_RESULT([ Contrib directory         $contrib_dir])
AC_MSG_RESULT([ Temporary directory       $tmp_dir])
AC_MSG_RESULT([ Temp dir permissions      $tmp_dir_permissions])
echo
echo " --- System options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Parent timeout (BIG T)    $parent_timeout])
AC_MSG_RESULT([ Child timeout (small t)   $child_timeout])
AC_MSG_RESULT([ Nagios name               $nagios_name])
AC_MSG_RESULT([ RC if no checks defined   $no_checks_rc])
AC_MSG_RESULT([ RC if caught a signal     $signal_rc])
AC_MSG_RESULT([ default cmdfile extension $file_extension])
AC_MSG_RESULT([ ignore missing cmd file?  $ignore_missing_cmd_file])
AC_MSG_RESULT([ Client perl path          $client_perl])
echo
echo " --- Output options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Name / Label              '$name'])
AC_MSG_RESULT([ Report option default     $report])
AC_MSG_RESULT([ HTML target frame         $target])
AC_MSG_RESULT([ Child checks indented?    $indent_label])
AC_MSG_RESULT([ Ascii indentation char    '$indent'])
AC_MSG_RESULT([ Collapse tree?            $collapse])
AC_MSG_RESULT([ Collapse plus style       $style_plus_minus])
AC_MSG_RESULT([ Extinfo in status.cgi?    $extinfo_in_status])
AC_MSG_RESULT([ Verbosity level default   $verbose])
AC_MSG_RESULT([ Verbosity fields          $verbose_fields])
AC_MSG_RESULT([ pnp version               $pnp_version])
AC_MSG_RESULT([ PNP URL                   $pnp_url])
AC_MSG_RESULT([ PNP chart with mouseover  $action_mouseover])
echo
echo " --- Links"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ action URL               '$action_url'])
AC_MSG_RESULT([ notes URL                '$notes_url'])
AC_MSG_RESULT([ documentation URL        '$tag_notes_link'])
echo
echo " --- Advanced Options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ illegal chars in cmdfile $illegal_chars])
AC_MSG_RESULT([ check_multi persistent?  $persistent])
AC_MSG_RESULT([ cmdfile update interval  $cmdfile_update_interval])
AC_MSG_RESULT([ Feed_passive autocreate  $feed_passive_autocreate])
AC_MSG_RESULT([ Feed_passive directory   $feed_passive_dir])
echo
echo
echo "*** Next step:  type 'make all'. ***"
echo ""
