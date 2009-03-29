#!/usr/bin/perl
#
# nagios_status (query nagios services from status.dat)
#
# Copyright (c) 2007 Matthias Flacke (matthias.flacke at gmx.de)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$
#
# Copy this file into <nagiosdir>/sbin and start the CGI via
# http://<hostname>/nagios/cgi-bin/nagios_status.cgi (YMMV)
#
use strict;
use CGI qw(:standard -debug escape);
use CGI::Carp qw(fatalsToBrowser);
BEGIN { eval("use Time::HiRes qw(time)") }

#-----------------------------------------------------------------------------
#--- adopt this value to your local installation -----------------------------
#-----------------------------------------------------------------------------

my $STATUSDAT="/usr/local/nagios/var/status.dat"; # location of status.dat

#-----------------------------------------------------------------------------
#--- nothing to change from here ;-) -----------------------------------------
#-----------------------------------------------------------------------------

my $MYSELF=url(-relative=>1);
my ($CGI_BIN)=(url()=~/(.*)\/$MYSELF/);
my ($NAGIOS_URL)=(url()=~/(.*)\/cgi-bin\/$MYSELF/);
my $query="";
my @numops=(">",">=","==","!=","<","<=");
my @strops=("=~","!~","eq","ne");
my @allops=(@numops,@strops);
my @st=("OK","WARNING","CRITICAL","UNKNOWN");
my @fg=("OK","WARNING","CRITICAL","UNKNOWN");
my @bg=("Even","BGWARNING","BGCRITICAL","BGUNKNOWN");
my @fields=();
my $ftype="";
my $opref=[];

#-----------------------------------------------------------------------------
#--- Main --------------------------------------------------------------------
#-----------------------------------------------------------------------------

#--- print HTML header with nagios stylesheets
print header(-target=>'main');
print "<LINK REL='stylesheet' TYPE='text/css' HREF='$NAGIOS_URL/stylesheets/common.css'>";
print "<LINK REL='stylesheet' TYPE='text/css' HREF='$NAGIOS_URL/stylesheets/status.css'>";
print start_html('Nagios Query');
#--- determine field names from status.dat (dependent on host / service)
@fields=get_fields(param('qtype')?param('qtype'):"service");

#--- determine field type from first record
$ftype=get_field_type(param('qtype'),param('qfield'));
# print "Field type: $ftype ";
if ($ftype eq "NUMERICAL" || $ftype eq "TIMESTAMP") {
	$opref=\@numops;
} elsif ($ftype eq "STRING") {
	$opref=\@strops;
} else {
	$opref=\@allops;
}


#--- print form
print start_form(-target=>'main'),
	hr,
	"Query ",
    	popup_menu(-name=>'qtype',-values=>['service','host'],-default=>'service',onChange=>'this.form.qexpr.value="";this.form.submit();'),
	" Expression ",
    	popup_menu(-name=>'qfield',-values=>\@fields,-default=>'plugin_output',onChange=>'this.form.qexpr.value="";this.form.submit();'),
    	popup_menu(-name=>'qop',-values=>$opref,-default=>$$opref[0]),
	textfield(-name=>'qexpr',value=>''),
    	submit(-name=>'Submit'),
	hr,
    	end_form;

#--- if debug parameter set, print some values
if (param('debug')) {
	print sup;
	print "NAGIOS_URL:$NAGIOS_URL<p>";
	print "CGI_BIN:$CGI_BIN<p>";
	print "query type:",param('qtype'),"<p>";
	print "query field:",param('qfield'),"<p>";
	print "query operator:",param('qop'),"<p>";
	print "query expr:",param('qexpr'),"<p>";
	print "ftype:$ftype<p>";
}

#--- launch query
my $starttime=time;
my @result=get_status(param('qtype'),param('qfield'),param('qop'),param('qexpr'));

#--- sort results: 1. field 2. host
@result=sort {uc($a->{param('qfield')}) cmp uc($b->{param('qfield')})} @result;
@result=sort { $a->{host_name} cmp $b->{host_name} } @result;

#--- print query stats, and URL for saving query
print sup, $#result+1, " results ";
printf "in %.2fs - ", time-$starttime;
print "bookmark this URL to save the query: ";
print "<A HREF=".url(-path_info=>1,-query=>1).">Query ".param('qtype')." ".param('qfield')." ".param('qop')." ".param('qexpr');

#--- print result table
print "<TABLE CLASS='status'>";
print "<TR align='left'>";
print "<TH class='status'>Hostname</TH>";
print "<TH class='status'>Service</TH>" if (param('qtype') eq "service");
print "<TH class='status'>State</TH>";
print "<TH class='status'>" . param('qfield') . "</TH>" if (param('qfield') ne "plugin_output");
print "<TH class='status'>Plugin Output</TH>";
print "</TR>";
#--- loop over items
my $previous_host="";
foreach my $item (@result) {
	my $state=$st[$item->{current_state}];
	my $fg=$fg[$item->{current_state}];
	my $bg=$bg[$item->{current_state}];
	print  "<TR>";

	#--- 1. if host changes, print host link
	# http://localhost/nagios/cgi-bin/extinfo.cgi?type=1&host=localhost
	if ($item->{host_name} ne $previous_host) {
		print "<TD CLASS='statusEven'>";
		#print "<A HREF=", $CGI_BIN, "extinfo.cgi?type=1&host=", $item->{host_name}, ">", $item->{host_name};
		printf "<A HREF=%sextinfo.cgi?type=1&host=%s>%s", $CGI_BIN,$item->{host_name},$item->{host_name};
		$previous_host=$item->{host_name};
	} else {
		print "<TD>";
	}
	print "</TD>";

	#--- 2. print service description if service query
	# http://localhost/nagios/cgi-bin/extinfo.cgi?type=2&host=localhost&service=Embedded%20Perl%20Check
	if (param('qtype') eq "service") {
		print "<TD CLASS='status$bg'>";
		printf "<A HREF=%sextinfo.cgi?type=2&host=%s&service=%s>%s",$CGI_BIN,$item->{host_name},
			escape($item->{service_description}),$item->{service_description};
		print "</TD>";
	}
	
	#--- 3. print state
	print "<TD CLASS='status$fg'>", $state, "</TD>";

	#--- 4. print query field
	if (param('qfield') ne "plugin_output") {
		printf "<TD CLASS=\'status$bg\' %s>%s</TD>", 
			($ftype eq "TIMESTAMP") ? sprintf("title=\'%s\'",timestamp($item->{param('qfield')})) : "", 
			$item->{param('qfield')};
	}

	#--- 5. print plugin_output anyway
	print "<TD CLASS='status$bg'>", $item->{plugin_output}, "</TD>";

	print "</TR>";

}
print "</TABLE>";
print end_html;

#---
#--- print nagios like timestamp
#--- 03-28-2009 18:33:29
#---
sub timestamp {
	my ($timestamp)=shift;
	my @t=localtime($timestamp);
	return sprintf "%02d-%02d-%04d %02d:%02d:%02d", 
		$t[4]+1,$t[3],$t[5]+1900,$t[2],$t[1],$t[0];
}
#---
#--- get fields from status.dat
#---
sub get_fields {
	my ($type)=@_;
	open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	while (<DAT>) {
		if (/^${type}status \{$/) {
			my %r=();
			while (<DAT>) {
				last if (/^\t\}$/);
				if (/\t([^=]+)=(.*)$/) {
					my $f=$1;
					$r{"$f"}++;
				}
			}
			close DAT;
			return sort keys(%r);
		}
	}
}

#---
#--- get field_type from status.dat
#---
sub get_field_type {
	my ($type,$field)=@_;
	#print " DEBUG: looking for field:$field type:$type<br> ";
	open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	while (<DAT>) {
		if (/^${type}status \{$/) {
			while (<DAT>) {
				last if (/^\t\}$/);
				if (/\t$field=(\S+)$/ && $1 ne "0") {
					close DAT;
					#print " field:$field content:>$1< ";
					if ($1=~/^([\d\.]+)$/) {
						if ($1=~/^(\d{10})$/) {
							# print " TIMESTAMP:>", timestamp(time), "<";
							return "TIMESTAMP";
						} else {
							return "NUMERICAL";
						}
					} elsif ($1=~/\D+/) {
						return "STRING";
					} else {
						return "UNKNOWN";
					}
				}
			}
		}
	}
	return "UNKNOWN";
}

#---
#--- perform query from status.dat
#---
sub get_status {
	my ($type,$field,$operator,$expr)=@_;
	return () if ($type eq "" || $field eq "" || $operator eq "" || $expr eq "");
	my @result=();
	open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	while (<DAT>) {
		chomp;
		next if (/^#/);
		next if (/^$/);
		if (/^${type}status \{$/) {
			my $found=0;
			my %r=();
			while (<DAT>) {
				chomp;
				last if (/^\t\}$/);
				if (/\t([^=]+)=(.*)$/) {
					my $f=$1;
					my $v=$2;
					#print "f:>$f< v:>$v<\n";
					$r{"$f"}=$v;
					if ($f=~/^$field$/ && $v ne "") {
						my $expression="";
						if ($operator=~/\~/) {
							$v=~s/\'/\\'/g;
							$expression="\'${v}\'${operator}/${expr}/i";
						} elsif ($operator=~/ne|eq/) {
							$v=~s/\'/\\'/g;
							$expression="\'${v}\'${operator}\'${expr}\'";
						} else {
							$expression="${v}${operator}${expr}";
						}
						#print "expression:$expression<p>\n";
						my $e=eval "($expression)";
                				print i,"Evaluation error in \'$expression\': $@<p>" if ($@);
						if ($e) {
							$found=1;
							#print "found: $v <-> $expr<p>";
						} else {
							$found=0;
							while (<DAT>) {
			                               		last if (/\t\}$/);
                       					}
							last;
						}

					}
				} else {
					print "Invalid format: >$_<\n";
				}
			}
			if ($found) {
				push @result,\%r;
			}
		} else {
			#print "Skipping >$line< (!=$type)...\n";
			while (<DAT>) {
				last if (/^\t\}$/);
			}
		}
	}
	close DAT;
	@result;
}
