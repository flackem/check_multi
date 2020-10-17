	:::perl
	eval [ kvm_command ] = "/usr/bin/kvm_stat --once";
	eval [ kvm ] = 
		if ( ! open(KVM, "$kvm_command$|")) {
			$?=$UNKNOWN<<3;
			"Error calling $kvm_command$: $?";
		} else {
			while (<KVM>) {
				my ($watcher,$total,$last)=split;
				parse_lines("eeval [ ${watcher}::kvmstat ] = \"$last | ${watcher}=${total}c\"");
			}
			if (! close(KVM)) {
				$?=$UNKNOWN<<3;
				"Error reading $kvm_command$: $?"
			}
		}

