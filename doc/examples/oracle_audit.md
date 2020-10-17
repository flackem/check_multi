# Oracle audit files

```
# check oracle audit files for non-zero status code

# call: check_multi -f ora_audit.cmd
#

eeval [ path_to_oracle_audit_files ] = "/path/to/oracle/audit";
eeval [ audit_files_max_age_days   ] = 7

eeval [ audit_errors               ] =
        my @files = `find $path_to_oracle_audit_files$
                -name '*.aud'
                -mtime -$audit_files_max_age_days$
                -exec grep -l "^STATUS:\[[0-9]*\] '[1-9][0-9]*'" {} \\;`;
        foreach my $path (@files) {
                if ($path=~/(.*)\/(.*)/) {
                        parse_lines("command [ $2 ] = ( /bin/echo; /usr/bin/cat $1/$2; exit $CRITICAL )");
                }
        }
        $? = ($#files+1) ? $CRITICAL<<8 : $OK<<8;
        return ($#files+1);
```
