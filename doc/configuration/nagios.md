## Nagios configuration example

As you will see below, this is fairly straight forward.

#### Service definition  

The example uses a command file ```check_multi.cmd``` and the following output options:

*  1 - list of services for each severity level
*  2 - HTML output
*  4 - STDERR output
*  8 - performance data

Note: you can provide the sum of the report options as a '+' separated number string


```
    define service { 
     name                 multi-service
     use                  generic-service
     check_command        check_multi!-f /usr/local/nagios/etc/check_multi.cmd -r 1+2+4+8
     service_description  check_multi_test
     host_name            localhost 
    }
```

#### Command definition
````
    define command {
    command_name         check_multi
    command_line         $USER1$/check_multi $ARG1$ $ARG2$ $ARG3$ $ARG4$
    }
````