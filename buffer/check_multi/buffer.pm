#!/usr/bin/perl
package check_multi::buffer;
use strict;
use warnings;
eval("use Time::HiRes qw(time sleep)");

sub new {
	my $self	= shift;
	my $maxage	= shift || 120;
	my $maxsize	= shift || 10;

	return bless({
		data	=> {},		# timestamp -> value
		head	=> 0,		# newest timestamp
		maxage	=> $maxage,	# maximum age of values
		maxsize	=> $maxsize,	# maximum number of entries
		size	=> 0,		# number of values
		tail	=> 0,		# oldest timestamp
	}, $self);
}

sub is_full {
	my $self = shift;
	return ($self->{size} >= $self->{maxsize});
}

sub is_empty {
	my $self = shift;
	return (scalar(keys %{$self->{data}}) == 0);
}

sub get_size {
	my $self = shift;
	$self->{size} = scalar(keys %{$self->{data}});
	return $self->{size};
}

sub cleanup {
	my $self = shift;
	return if ($self->is_empty);
   
	my $now = time;
	foreach my $timestamp (sort { $a <=> $b } keys %{$self->{data}}) {
		if ($timestamp < $now - $self->{maxage} || $self->{size} > $self->{maxsize}) {
			#print "Deleting value from $timestamp:$self->{data}->{$timestamp}\n";
			$self->pop($timestamp);
		} else {
			#print "Cleanup finished, oldest value is from $self->{tail}\n";
			last;
		}
	}
	return $self->{size};
}

sub push {
	my $self = shift;
	my $val = shift || return;
	my $now = shift || time;

	$self->cleanup;
	return if $self->is_full;

	$self->{data}->{$now}=$val;
	$self->set_head;
	$self->set_tail;
	$self->get_size;
	#print "Pushed at $now value $val\n";
	return $val;
}

sub pop {
	my $self = shift;
	my $timestamp = shift || $self->set_tail;

	return if $self->is_empty;

	if ($self->{data}->{$timestamp}) {
		delete $self->{data}->{$timestamp};
		$self->set_tail;
		$self->set_head;
		$self->get_size;
	}
}

sub set_tail {
	my $self = shift;
	if ($self->is_empty) {
		$self->{tail} = 0; 
	} else {
		$self->{tail} = (sort { $a <=> $b } keys %{$self->{data}})[0];
	}
}

sub set_head {
	my $self = shift;
	if ($self->is_empty) {
		$self->{head} = 0; 
	} else {
		$self->{head} = (sort { $b <=> $a } keys %{$self->{data}})[0];
	}
}

sub get_avg_latest {
	my $self = shift;
	my $seconds = shift || return;

	return if $self->is_empty;

	my $now = time;
	my $sum = 0;
	my $count = 0;
	foreach my $timestamp (keys %{$self->{data}}) {
		#--- skip all values older than seconds
		next if ($timestamp < $now - $seconds);

		$count++;
		$sum += $self->{data}->{$timestamp};
	}
	return if ($count == 0);
	return $sum / $count;
}

sub get_avg_interval {
	my $self = shift;
	my $newest = shift || return;
	my $oldest = shift || return;

	return if $self->is_empty;

	my $now = time;
	my $sum = 0;
	my $count = 0;
	foreach my $timestamp (keys %{$self->{data}}) {
		#--- skip all values not in timeframe
		next if ($timestamp < $now - $oldest || $timestamp > $now - $newest);

		$count++;
		$sum += $self->{data}->{$timestamp};
	}
	return if ($count == 0);
	return $sum / $count;
}

sub get_avg {
	my $self = shift;

	return if $self->is_empty;

	my $sum = 0;
	my $count = 0;
	foreach my $timestamp (keys %{$self->{data}}) {
		$count++;
		$sum += $self->{data}->{$timestamp};
	}
	return if ($count == 0);
	return $sum / $count;
}

sub get_max {
	my $self = shift;

	return if $self->is_empty;

	my $max = undef;
	foreach my $timestamp (keys %{$self->{data}}) {
		if (! $max or $max < $self->{data}->{$timestamp}) {
			$max = $self->{data}->{$timestamp} 
		}
	}
	return $max;
}

sub get_min {
	my $self = shift;

	return if $self->is_empty;

	my $min = undef;
	foreach my $timestamp (keys %{$self->{data}}) {
		if (! $min or $min > $self->{data}->{$timestamp}) {
			$min = $self->{data}->{$timestamp};
		}
	}
	return $min;
}

1;
