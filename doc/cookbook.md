======= cookbook =======

## echo value and return RC

```
command [ simple_echo_2_return_1 ] = (
        echo 2;
        exit 1;
)
eeval [ eeval_echo_2_return_test ] =
        $? = 1 << 8;
        "test";
```

## if condition with depending output and RC

```
command [ if_condition_return_0_or_3 ] = (
        if [ `date +%S` -gt 30 ]; then
                echo "`date +%S` - OK"; 
                exit 0;
        else
                echo "`date +%S` - UNKNOWN";
                exit 3;
        fi
)
```

```
command [ if_condition_return_0_or_2 ] =
        if grep 9 /proc/cpuinfo >/dev/null; then
                echo "`date +%S` - OK";
                exit 0;
        else
                echo "`date +%S` - CRITICAL";
                exit 2;
        fi
```

## self expanding command list

## dynamic command generation
## adaptive monitoring

## exit with special output and RC
## perfdata

## livestatus connection script

```
#!/usr/bin/perl
use Monitoring::Livestatus;
use Time::HiRes qw (time);
 
sub read_livestatus {
        my ($livestatus_path, $query)=@_;
 
        my $ml=Monitoring::Livestatus->new(
                peer=>$livestatus_path,
        );
        if($Monitoring::Livestatus::ErrorCode) {
                print "read_livestatus: $Monitoring::Livestatus::ErrorMessage";
                return undef;
        }
        $ml->errors_are_fatal(0);
        #$ml->errors_are_fatal(1);
        #$ml->warnings(1);
        my $livestatus=$ml->selectall_arrayref($query,{Slice => 1});
        if($Monitoring::Livestatus::ErrorCode) {
                print "read_livestatus: $Monitoring::Livestatus::ErrorMessage";
                return undef;
        }
        return $livestatus;
}
 
#--- main

my $livesocket = shift(@ARGV) || die "usage: $0 `<livestatus socket>`\n";
-S $livesocket || die "livestatus socket $livesocket is not a socket\n";
my $starttime = time;
my $aref = read_livestatus(
        $livesocket, 
        "GET services\nColumns: host_name description state last_hard_state plugin_output long_plugin_output perf_data check_command\n"
);
my $endtime = time;
printf "%d results in %f seconds\n", $#{@$aref}, $endtime - $starttime;
```
