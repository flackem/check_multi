======= create_child_services.pl =======
All the passive services which are the target of the feeder event handler have to be created. You can do this manually, but its much simpler to just get a perl script do this work:
```
#!/usr/bin/perl
#

# create_child_services.pl 
# (create passive services from multi child services from status.dat)

#
# Copyright (c) 2008 Matthias Flacke (matthias.flacke at gmx.de)

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
use Data::Dumper;
use XML::Simple;
use strict;
#

#--- adopt these values to your local installation
my $STATUSDAT="/usr/local/nagios/var/status.dat";
#

#--- nothing to change from here ;-)
my $multi_service=shift(@ARGV);
my $tgtdir=shift(@ARGV);
my $success=0;
my $no_result=0;
my $overall=0;
my $starttime=time;
#

#--- check args
if ($multi_service eq "" || $tgtdir eq "") {
	print STDERR "usage: create_child_services.pl <multi_service> <target dir>\n";
	print STDERR "\t- multi_service: name of multi_service which feeds passive services (XML output)\n";
	print STDERR "\t- target dir: directory which should contain service definitions (new directory, which does not already exist!)\n";
	exit 1;
}
if (-d $tgtdir) {
	print STDERR "Error: target directory $tgtdir already exists. Please use a fresh and non existing directory name\n";
	exit 2;
} else {
	mkdir $tgtdir;
	if (! -d $tgtdir) {
		print STDERR "Cannot create target directory $tgtdir: $?\n";
		exit 3;
	}
}
#

#--- Main

my @result=get_status("service", "service_description", "=~", "$multi_service");
#print Dumper(@result);

if ($#result < 0) {
	print "Error: no services found with service description \'$multi_service\'\n";
	exit 4;
}
@result=sort { $a->{host_name} cmp $b->{host_name} } @result;
#

#--- loop over results
foreach my $service (@result) {
	my $hostname=$service->{host_name};
	my $long_plugin_output=$service->{long_plugin_output};
	$long_plugin_output=~s/.*(<PARENT>.*<\/PARENT>).*/\1/;
	$long_plugin_output=~s/\\n//g;

	#--- no result? skip service
	if ($long_plugin_output eq "") {
		print STDERR "No result for service $service->{service_description} on host $hostname - skipping\n";
		$no_result++;
		next;
	} else {
		print STDERR "Writing $tgtdir/multi_passive_${hostname}_" . ${service}->{service_description} . ".cfg for $service->{service_description} on host $hostname\n";
	}

	my $xmlref = XMLin($long_plugin_output);

	#--- loop over children and create file for command submission
	my $service_cfg="$tgtdir/multi_passive_${hostname}_" . ${service}->{service_description} . ".cfg";
	open (SERVICE, ">$service_cfg") || die "Cannot open service configuration file $service_cfg:$?";
	foreach my $child (keys %{$xmlref->{CHILD}}) {
		print SERVICE <<EOF;
define service {
	service_description     $child
	host_name               $hostname
	passive_checks_enabled  1
	active_checks_enabled   0
	check_command           check_dummy!0 "passive check"
	servicegroups           passive_feed
	use                     local-service
}
EOF
	}
	close SERVICE;

	#--- count
	$overall+=keys %{$xmlref->{CHILD}};
	$success++;
}
#--- general result

print STDERR "-" x 80, "\n";
my $elapsed=time - $starttime;
print STDERR "Written files: $success No results: $no_result All services: $overall Runtime:$elapsed seconds\n";
print STDERR "-" x 80, "\n";
exit 0;

#print Dumper(@result);

#

sub get_attr {
	my ($type)=@_;
	open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	while (<DAT>) {
		if (/^${type}status \{$/) {
			my %r=();
			while (<DAT>) {
				my $line=$_;
				last if ($line=~/^\t\}$/);
				if ($line=~/\t([^=]+)=(.*)$/) {
					my $f=$1;
					$r{"$f"}++;
				}
			}
			close DAT;
			return sort keys(%r);
		}
	}
}

sub get_status {
	my ($type,$field,$operator,$expr)=@_;
	my @result=();
	open(DAT,$STATUSDAT) || die "Cannot open $STATUSDAT:$!";
	while (<DAT>) {
		my $line=$_;
		chomp $line;
		next if ($line=~/^#/);
		next if ($line=~/^$/);
		if ($line=~/^${type}status \{$/) {
			my $found=0;
			my %r=();
			while (<DAT>) {
				my $line=$_;
				chomp $line;
				last if ($line=~/^\t\}$/);
				if ($line=~/\t([^=]+)=(.*)$/) {
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
                				print "Evaluation error in \'$expression\': $@`<p>`" if ($@);
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
					print "Invalid format: >$line<\n";
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
```
