#---
#--- configure.ac
#---
#--- (c) 2008-2009 Matthias Flacke
#---
#--- $Id$
#---
#--- plenty of configuration options 
#---
#--- prerequisites, credits and Nagios defaults
AC_PREREQ(2.61)
AC_INIT(check_multi, (author: matthias.flacke@gmx.de))

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

AC_SUBST(PKG_NAME)
AC_SUBST(PKG_VERSION)
AC_SUBST(PKG_AUTHOR)
AC_SUBST(PKG_HOME_URL)
AC_SUBST(PKG_REL_DATE)
AC_SUBST(PKG_ID)

#---
#--- checks for programs
AC_PROG_MAKE_SET
#AC_PATH_PROG([STRIP],[strip],[true])
AC_PATH_PROG(CHMOD,chmod)
AC_PATH_PROG(CP,cp)
AC_PATH_PROG(INSTALL,install)
AC_SUBST(INSTALL)
AC_PATH_PROG(PERL,perl)
AC_PATH_PROG(ETHTOOL,ethtool)

#---
if test "${exec_prefix}" = "NONE"; then
	exec_prefix="${prefix}"
fi

#--- too difficult to escape this - so define it as a variable before using it ;)
ACTION_URL="style='color:#4444FF;line-height:0.1em;font-size:1.5em;cursor:crosshair'"
AC_ARG_WITH(action_url,		[  

check_multi settings:
  --with-action_url=<URL>                  action URL (default:"")],action_url=$withval,action_url="")
AC_ARG_WITH(action_mouseover,           [  --with-action_mouseover=<0|1>            show PNP chart popup triggered by mouseover (default:0)],action_mouseover=$withval,action_mouseover=0)
#--- too difficult to escape this - so define it as a variable before using it ;)
client_perL=no
AC_ARG_WITH(client_perl,                        [  --with-client_perl=<perl path>           sets perl cmdline / path (e.g. #!/usr/bin/perl)],client_perl=$withval,client_perl=no)
if test client_perl=no; then
       AC_PATH_PROG(client_perl,perl)
fi
AC_ARG_WITH(cmdfile_update_interval,	[  --with-cmdfile_update_interval=<seconds> interval to update command file(s) (default:86400, one day)],cmdfile_update_interval=$withval,cmdfile_update_interval=86400)
AC_ARG_WITH(collapse,			[  --with-collapse=<0|1>                    HTML javascript tree collapse option (default:1)],collapse=$withval,collapse="1")
AC_ARG_WITH(checkresults_dir,		[  --with-checkresults_dir=<path>           directory for Nagios checkresults (default:${localstatedir}/spool/checkresults)],checkresults_dir=$withval,checkresults_dir="${localstatedir}/spool/checkresults")
AC_ARG_WITH(config_dir,			[  --with-config_dir=<path>                 directory for check_multi configuration files (default:${sysconfdir}/multi)],config_dir=$withval,config_dir="${sysconfdir}/multi")
if test ethtool=""; then
	AC_ARG_WITH(ethtool,			[  --with-ethtool=</path/to/ethtool>        define path to ethtool (default:/sbin/ethtool)],ethtool=$ethtool,ethtool="/sbin/ethtool")
fi
AC_ARG_WITH(exec_open3,			[  --with-exec_open3=<0|1>                  use new exec method with function open3],exec_open3=$withval,exec_open3=0)
AC_ARG_WITH(extinfo_in_status,		[  --with-extinfo_in_status=<0|1>           display check_multi output in status.cgi],extinfo_in_status=$withval,extinfo_in_status=0)
AC_ARG_WITH(findbin,			[  --with-findbin=<0|1>                     use Perl module FindBin for addressing plugins (default:1)],findbin=$withval,findbin=1)
AC_ARG_WITH(file_extension,		[  --with-file_extension=<ext>              default extension for check_multi command files (default:"cmd")],file_extension=$withval,file_extension="cmd")
AC_ARG_WITH(ignore_missing_cmd_file,	[  --with-ignore_missing_cmd_file=<0|1>     if missing cmd files should be ignored (default:0)],ignore_missing_cmd_file=$withval,ignore_missing_cmd_file="0")
AC_ARG_WITH(illegal_chars,		[  --with-illegal_chars=<chars>             characters to be stripped from command files (default:"\r")],illegal_chars=$withval,illegal_chars="\r")
AC_ARG_WITH(image_path,			[  --with-image_path=<URL>                  relative URL to nagios images (default:"/nagios/images")],image_path=$withval,image_path="/nagios/images")
AC_ARG_WITH(indent,			[  --with-indent=<char>                     ASCII output indent character (default:" ")],indent=$withval,indent=" ")
AC_ARG_WITH(indent_label,		[  --with-indent_label=<0|1>                indentation of child checks? (default:1)],indent_label=$withval,indent_label=1)
AC_ARG_WITH(name,			[  --with-name=<name>                       default name for check_multi label (default:"")],name=$withval,name="")
AC_ARG_WITH(no_checks_rc,		[  --with-no_checks_rc=<RC>                 RC if no checks are specified (default:3-UNKNOWN)],no_checks_rc=$withval,no_checks_rc=3)
AC_ARG_WITH(notes_url,			[  --with-notes_url=<URL>                   notes URL (default:"")],notes_url=$withval,notes_url="")
AC_ARG_WITH(persistent,			[  --with-persistent=<0|1>                  persistency: saving of state data between two calls (default:0)],persisent=$withval,persistent=0)
AC_ARG_WITH(pnp_path,			[  --with-pnp_path=<URL>                    relative URL to PNP (default:"/nagios/pnp")],pnp_path=$withval,pnp_path="/nagios/pnp")
AC_ARG_WITH(report,			[  --with-report=<NN>                       default report option (default:13)],report=$withval,report="13")
AC_ARG_WITH(style_plus_minus,		[  --with-style_plus_minus=<HTML code>      HTML style for plus/minus (default:$ACTION_URL)],style_plus_minus=$withval,style_plus_minus="$ACTION_URL")
AC_ARG_WITH(tag_notes_link,		[  --with-tag_notes_link=<URL>              documentation URL for child checks (default:"")],tag_notes_link=$withval,tag_notes_link="")
AC_ARG_WITH(target,			[  --with-target=<target_frame>             HTML target frame for URLs (default:_self)],target=$withval,target="_self")
AC_ARG_WITH(tmp_dir,			[  --with-tmp_dir=<path>                    /path/to/tmp_dir (default:/tmp/check_multi)],tmp_dir=$withval,tmp_dir="/tmp/check_multi")
AC_ARG_WITH(tmp_etc,			[  --with-tmp_etc=<path>                    /path/to/tmp_dir/etc (default:$tmp_dir/etc)],tmp_etc=$withval,tmp_etc="$tmp_dir/etc")
AC_ARG_WITH(tmp_dir_permissions,	[  --with-tmp_dir_permissions=<octal perms> permissions of tmp_dir (default:01777)],tmp_dir_permissions=$withval,tmp_dir_permissions="01777")
AC_ARG_WITH(parent_timeout,		[  --with-parent_timeut=<NN>                timeout for parent check (default:60)],parent_timeout=$withval,parent_timeout="60")
AC_ARG_WITH(child_timeout,		[  --with-child_timeout=<NN>                timeout for child checks (default:10)],child_timeout=$withval,child_timeout="10")
AC_ARG_WITH(verbose,			[  --with-verbose=<N>                       verbosity of check_multi (default:0)],verbose=$withval,verbose="0")
AC_ARG_WITH(nagios_user,		[  --with-nagios-user=<user>                user name to run plugin (default:nagios)],nagios_user=$withval,nagios_user=nagios)
AC_ARG_WITH(nagios_group,		[  --with-nagios-group=<group>              group name to run plugin (default:nagios)],nagios_group=$withval,nagios_group=nagios)
AC_ARG_WITH(nagios_name,		[  --with-nagios-name=<name>                set nagios name (there should some clones ;)) (default:nagios)],nagios_name=$withval,nagios_name=nagios)

AC_SUBST(action_mouseover)
AC_SUBST(action_url)
AC_SUBST(child_timeout)
AC_SUBST(contrib_dir)
AC_SUBST(checkresults_dir)
AC_SUBST(collapse)
AC_SUBST(cmdfile_update_interval)
AC_SUBST(config_dir)
AC_SUBST(extinfo_in_status)
AC_SUBST(ethtool)
AC_SUBST(exec_open3)
AC_SUBST(findbin)
AC_SUBST(file_extension)
AC_SUBST(ignore_missing_cmd_file)
AC_SUBST(illegal_chars)
AC_SUBST(image_path)
AC_SUBST(indent_label)
AC_SUBST(indent)
AC_SUBST(name)
AC_SUBST(no_checks_rc)
AC_SUBST(notes_url)
AC_SUBST(persistent)
AC_SUBST(pnp_path)
AC_SUBST(report)
AC_SUBST(service_definition_template)
AC_SUBST(style_plus_minus)
AC_SUBST(tag_notes_link)
AC_SUBST(target)
AC_SUBST(tmp_dir)
AC_SUBST(tmp_etc)
AC_SUBST(tmp_dir_permissions)
AC_SUBST(parent_timeout)
AC_SUBST(child_timeout)
AC_SUBST(verbose)
AC_SUBST(nagios_user)
AC_SUBST(nagios_group)
AC_SUBST(nagios_name)
AC_SUBST(LIBEXECDIR)

AC_DEFINE_UNQUOTED(DEFAULT_NAGIOS_USER,"$nagios_user")
AC_DEFINE_UNQUOTED(DEFAULT_NAGIOS_GROUP,"$nagios_group")
AC_DEFINE_UNQUOTED(DEFAULT_NAGIOS_NAME,"$nagios_name")

INSTALL_OPTS="-o $nagios_user -g $nagios_group"
AC_SUBST(INSTALL_OPTS)

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
$PERL subst plugins/check_multi
$PERL subst plugins/t/Makefile
$PERL subst plugins/t/check_multi.t

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
$PERL subst sample_config/nagiostats/nagiostats.php
$PERL subst sample_config/start_process/Makefile
$PERL subst sample_config/start_process/start_process.cmd
$PERL subst sample_config/network_interface/Makefile
$PERL subst sample_config/network_interface/network_interface.cmd

#---
#--- review options and show the user what he has broken ;)
AC_MSG_RESULT([
 -------------------------------------------------------------------
 --- $PKG_NAME configure summary (SVN ${PKG_VERSION}) 
 -------------------------------------------------------------------
])
echo " Release date ${PKG_REL_DATE}"
echo " Author       ${PKG_AUTHOR}"
echo
echo " --- Directories"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Install \${prefix}         $prefix])
AC_MSG_RESULT([ Exec \${exec_prefix}       $exec_prefix])
AC_MSG_RESULT([ Libexec directory         $libexecdir])
AC_MSG_RESULT([ CGI directory (sbin)      $sbindir])
AC_MSG_RESULT([ HTML directory (dataroot) $datarootdir])
AC_MSG_RESULT([ Contrib directory         $contrib_dir])
AC_MSG_RESULT([ Temporary directory       $tmp_dir])
AC_MSG_RESULT([ Temp dir permissions      $tmp_dir_permissions])
echo
echo " --- System options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Parent timeout (BIG T)    $parent_timeout])
AC_MSG_RESULT([ Child timeout (small t)   $child_timeout])
AC_MSG_RESULT([ Nagios user/group         $nagios_user,$nagios_group])
AC_MSG_RESULT([ Nagios name               $nagios_name])
AC_MSG_RESULT([ RC if no checks defined   $no_checks_rc])
AC_MSG_RESULT([ default file extension    $file_extension])
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
AC_MSG_RESULT([ cmdfile update interval  $cmdfile_update_interval])
AC_MSG_RESULT([ illegal chars in cmdfile $illegal_chars])
AC_MSG_RESULT([ check_multi persistent?  $persistent])
echo
echo
echo "*** Next step:  type 'make all'. ***"
echo ""
