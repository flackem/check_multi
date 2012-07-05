#!/usr/bin/perl
#
use check_multi::buffer;
eval("use Time::HiRes qw(time sleep)");

my $tb = check_multi::buffer->new(100,100);
while (1) {
	my $load = (split(/\s+/,`cat /proc/loadavg`))[0];
	$tb->push($load);

	printf "%s\nValue:%.2f Tail:%d Head:%d Queue Size:%d\n", 
		scalar(localtime), $load, $tb->{tail}, $tb->{head}, $tb->{size};
	printf "Maximum:%.2f Minimum:%.2f Average:%.2f\n", 
		$tb->get_max, $tb->get_min, $tb->get_avg;
	printf "Avg s0-10:%.2f Avg s10-20:%.2f Avg s20-30:%.2f\n\n", 
		$tb->get_avg_latest(10), 
		$tb->get_avg_interval(10,20), 
		$tb->get_avg_interval(20,30); 
	sleep 1;
}
