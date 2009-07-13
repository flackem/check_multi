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
AC_PATH_PROG(CP,cp)
AC_PATH_PROG(INSTALL,install)
AC_SUBST(INSTALL)
AC_PATH_PROG(PERL,perl)

#--- too difficult to escape this - so define it as a variable before using it ;)
ACTION_URL="style='color:#4444FF;line-height:0.1em;font-size:1.5em;cursor:crosshair'"
AC_ARG_WITH(multi_action_url,		[  

check_multi settings:
  --action_url=<URL>                  action URL (default:"")],multi_action_url=$withval,multi_action_url="")
AC_ARG_WITH(multi_cmdfile_update_interval,	[  --cmdfile_update_interval=<seconds> interval to update command file(s) (default:86400, one day)],multi_cmdfile_update_interval=$withval,multi_cmdfile_update_interval=86400)
AC_ARG_WITH(multi_collapse,			[  --collapse=<0|1>                    HTML javascript tree collapse option (default:1)],multi_collapse=$withval,multi_collapse="1")
AC_ARG_WITH(multi_config_dir,			[  --config_dir=<path>                 directory for check_multi configuration files (default:${prefix}/etc/multi)],multi_config_dir=$withval,multi_config_dir="${prefix}/etc/multi")
AC_ARG_WITH(multi_exec_open3,			[  --exec_open3=<0|1>                  use new exec method with function open3],multi_exec_open3=$withval,multi_exec_open3=0)
AC_ARG_WITH(multi_extinfo_in_status,		[  --extinfo_in_status=<0|1>           display check_multi output in status.cgi],multi_extinfo_in_status=$withval,multi_extinfo_in_status=0)
AC_ARG_WITH(multi_file_extension,		[  --file_extension=<ext>              default extension for check_multi command files (default:"cmd")],multi_file_extension=$withval,multi_file_extension="cmd")
AC_ARG_WITH(multi_ignore_missing_cmd_file,	[  --ignore_missing_cmd_file=<0|1>     if missing cmd files should be ignored (default:0)],multi_ignore_missing_cmd_file=$withval,multi_ignore_missing_cmd_file="0")
AC_ARG_WITH(multi_illegal_chars,		[  --illegal_chars=<chars>             characters to be stripped from command files (default:"\r")],multi_illegal_chars=$withval,multi_illegal_chars="\r")
AC_ARG_WITH(multi_image_path,			[  --image_path=<URL>                  relative URL to nagios images (default:"/nagios/images")],multi_image_path=$withval,multi_image_path="/nagios/images")
AC_ARG_WITH(multi_indent,			[  --indent=<char>                     ASCII output indent character (default:" ")],multi_indent=$withval,multi_indent=" ")
AC_ARG_WITH(multi_indent_label,			[  --indent_label=<0|1>                indentation of child checks? (default:1)],multi_indent_label=$withval,multi_indent_label=1)
AC_ARG_WITH(multi_name,				[  --name=<name>                       default name for check_multi label (default:"")],multi_name=$withval,multi_name="")
AC_ARG_WITH(multi_no_checks_rc,			[  --no_checks_rc=<RC>                 RC if no checks are specified (default:3-UNKNOWN)],multi_no_checks_rc=$withval,multi_no_checks_rc=3)
AC_ARG_WITH(multi_notes_url,			[  --notes_url=<URL>                   notes URL (default:"")],multi_notes_url=$withval,multi_notes_url="")
AC_ARG_WITH(multi_persistent,			[  --persistent=<0|1>                  persistency: saving of state data between two calls (default:0)],multi_persisent=$withval,multi_persistent=0)
AC_ARG_WITH(multi_pnp_path,			[  --pnp_path=<URL>                    relative URL to PNP (default:"/nagios/pnp")],multi_pnp_path=$withval,multi_pnp_path="/nagios/pnp")
AC_ARG_WITH(multi_report,			[  --report=<NN>                       default report option (default:13)],multi_report=$withval,multi_report="13")
AC_ARG_WITH(multi_style_plus_minus,		[  --style_plus_minus=<HTML code>      HTML style for plus/minus (default:$ACTION_URL)],multi_style_plus_minus=$withval,multi_style_plus_minus="$ACTION_URL")
AC_ARG_WITH(multi_tag_notes_link,		[  --tag_notes_link=<URL>              documentation URL for child checks (default:"")],multi_tag_notes_link=$withval,multi_tag_notes_link="")
AC_ARG_WITH(multi_target,			[  --target=<target_frame>             HTML target frame for URLs (default:_self)],multi_target=$withval,multi_target="_self")
AC_ARG_WITH(multi_tmp_dir,			[  --tmp_dir=<path>                    /path/to/tmp_dir (default:/tmp/check_multi)],multi_tmp_dir=$withval,multi_tmp_dir="/tmp/check_multi")
AC_ARG_WITH(multi_tmp_etc,			[  --tmp_etc=<path>                    /path/to/tmp_dir/etc (default:$multi_tmp_dir/etc)],multi_tmp_etc=$withval,multi_tmp_etc="$multi_tmp_dir/etc")
AC_ARG_WITH(multi_tmp_dir_permissions,		[  --tmp_dir_permissions=<octal perms> permissions of tmp_dir (default:01777)],multi_tmp_dir_permissions=$withval,multi_tmp_dir_permissions="01777")
AC_ARG_WITH(multi_parent_timeout,		[  --parent_timeut=<NN>                timeout for parent check (default:60)],multi_parent_timeout=$withval,multi_parent_timeout="60")
AC_ARG_WITH(multi_child_timeout,		[  --child_timeout=<NN>                timeout for child checks (default:10)],multi_child_timeout=$withval,multi_child_timeout="10")
AC_ARG_WITH(multi_verbose,			[  --verbose=<N>                       verbosity of check_multi (default:0)],multi_verbose=$withval,multi_verbose="0")
AC_ARG_WITH(nagios_user,			[  --nagios-user=<user>                user name to run plugin (default:nagios)],nagios_user=$withval,nagios_user=nagios)
AC_ARG_WITH(nagios_group,			[  --nagios-group=<group>              group name to run plugin (default:nagios)],nagios_group=$withval,nagios_group=nagios)
AC_ARG_WITH(nagios_name,			[  --nagios-name=<name>                set nagios name (there should some clones ;)) (default:nagios)],nagios_name=$withval,nagios_name=nagios)

AC_SUBST(multi_action_url)
AC_SUBST(multi_child_timeout)
AC_SUBST(multi_contrib_dir)
AC_SUBST(multi_collapse)
AC_SUBST(multi_cmdfile_update_interval)
AC_SUBST(multi_config_dir)
AC_SUBST(multi_extinfo_in_status)
AC_SUBST(multi_exec_open3)
AC_SUBST(multi_file_extension)
AC_SUBST(multi_ignore_missing_cmd_file)
AC_SUBST(multi_illegal_chars)
AC_SUBST(multi_indent_label)
AC_SUBST(multi_indent)
AC_SUBST(multi_nagios_images)
AC_SUBST(multi_name)
AC_SUBST(multi_no_checks_rc)
AC_SUBST(multi_notes_url)
AC_SUBST(multi_persistent)
AC_SUBST(multi_pnp_path)
AC_SUBST(multi_report)
AC_SUBST(multi_service_definition_template)
AC_SUBST(multi_style_plus_minus)
AC_SUBST(multi_tag_notes_link)
AC_SUBST(multi_target)
AC_SUBST(multi_tmp_dir)
AC_SUBST(multi_tmp_etc)
AC_SUBST(multi_tmp_dir_permissions)
AC_SUBST(multi_parent_timeout)
AC_SUBST(multi_child_timeout)
AC_SUBST(multi_verbose)
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
AC_MSG_RESULT([ Contrib directory         $multi_contrib_dir])
AC_MSG_RESULT([ Temporary directory       $multi_tmp_dir])
AC_MSG_RESULT([ Temp dir permissions      $multi_tmp_dir_permissions])
echo
echo " --- Miscellaneous options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Parent timeout (BIG T)    $multi_parent_timeout])
AC_MSG_RESULT([ Child timeout (small t)   $multi_child_timeout])
AC_MSG_RESULT([ Nagios user/group         $nagios_user,$nagios_group])
AC_MSG_RESULT([ Nagios name               $nagios_name])
AC_MSG_RESULT([ RC if no checks defined   $multi_no_checks_rc])
AC_MSG_RESULT([ default file extension    $multi_file_extension])
AC_MSG_RESULT([ ignore missing cmd file?  $multi_ignore_missing_cmd_file])
echo
echo " --- Output options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ Name / Label              '$multi_name'])
AC_MSG_RESULT([ Report option default     $multi_report])
AC_MSG_RESULT([ HTML target frame         $multi_target])
AC_MSG_RESULT([ Child checks indented?    $multi_indent_label])
AC_MSG_RESULT([ Ascii indentation char    '$multi_indent'])
AC_MSG_RESULT([ Collapse tree?            $multi_collapse])
AC_MSG_RESULT([ Collapse plus style       $multi_style_plus_minus])
AC_MSG_RESULT([ Extinfo in status.cgi?    $multi_extinfo_in_status])
AC_MSG_RESULT([ Verbosity level default   $multi_verbose])
echo
echo " --- Links"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ action URL               '$multi_action_url'])
AC_MSG_RESULT([ notes URL                '$multi_notes_url'])
AC_MSG_RESULT([ documentation URL        '$multi_tag_notes_link'])
echo
echo " --- Advanced Options"
echo " -------------------------------------------------------------------"
AC_MSG_RESULT([ cmdfile update interval  $multi_cmdfile_update_interval])
AC_MSG_RESULT([ illegal chars in cmdfile $multi_illegal_chars])
AC_MSG_RESULT([ check_multi persistent?  $multi_persistent])
echo
echo
echo "*** Next step:  type 'make all'. ***"
echo ""
