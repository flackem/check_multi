## Status Query

### host status

| field name                    | content                                      | type      | allowed values                            |
| ----------                    | -------                                      | ----      | --------------                            |
| acknowledgement_type          | 0                                            | INTEGER   | 0-none 1-normal 2-sticky                  |
| active_checks_enabled         | 1                                            | BOOLEAN   | 0-disabled 1-enabled                      |
| check_command                 | check-host-alive                             | STRING    | contains the check_command for this check |
| check_execution_time          | 1.098                                        | FLOAT     | Time in seconds                           |
| check_interval                | 60.000000                                    | FLOAT     | refers to interval_length in nagios.cfg   |
| check_latency                 | 0.316                                        | FLOAT     | time which a service is too late          |
| check_options                 | 0                                            | INTEGER   |                                           |
| check_period                  | 24x7                                         | STRING    |                                           |
| check_type                    | 0                                            | INTEGER   | 0-active 1-passive                        |
| current_attempt               | 1                                            | INTEGER   |                                           |
| current_event_id              | 109                                          | INTEGER   |                                           |
| current_notification_id       | 18                                           | INTEGER   |                                           |
| current_notification_number   | 0                                            | INTEGER   |                                           |
| current_problem_id            | 0                                            | INTEGER   |                                           |
| current_state                 | 0                                            | INTEGER   | 0-OK 1-WARNING 2-CRITICAL 3-UNKNOWN, is the RC of the plugin
| event_handler_enabled         | 1                                            | INTEGER   |                                           |
| event_handler                 | ??                                           | ??        |                                           |
| failure_prediction_enabled    | 1                                            | INTEGER   |                                           |
| flap_detection_enabled        | 1                                            | INTEGER   |                                           |
| has_been_checked              | 1                                            | INTEGER   |                                           |
| host_name                     | thinkpad                                     | STRING    |                                           |
| is_flapping                   | 0                                            | INTEGER   |                                           |
| last_check                    | 1239555469                                   | TIMESTAMP |                                           |
| last_event_id                 | 39                                           | INTEGER   |                                           |
| last_hard_state_change        | 1238513894                                   | TIMESTAMP |                                           |
| last_hard_state               | 0                                            | TIMESTAMP |                                           |
| last_notification             | 0                                            | TIMESTAMP |                                           |
| last_problem_id               | 1                                            | INTEGER   |                                           |
| last_state_change             | 1238513894                                   | TIMESTAMP |                                           |
| last_time_down                | 1237667540                                   | TIMESTAMP |                                           |
| last_time_unreachable         | 0                                            | TIMESTAMP |                                           |
| last_time_up                  | 1239555479                                   | TIMESTAMP |                                           |
| last_update                   | 1239558120                                   | TIMESTAMP |                                           |
| long_plugin_output            |                                              | STRING    |                                           |
| max_attempts                  | 10                                           | INTEGER   |                                           |
| modified_attributes           | 0                                            | INTEGER   |                                           |
| next_check                    | 1239559079                                   | TIMESTAMP |                                           |
| next_notification             | 0                                            | INTEGER   |                                           |
| no_more_notifications         | 0                                            | INTEGER   |                                           |
| notification_period           | workhours                                    | STRING    |                                           |
| notifications_enabled         | 1                                            | INTEGER   |                                           |
| obsess_over_host              | 1                                            | INTEGER   |                                           |
| passive_checks_enabled        | 1                                            | INTEGER   |                                           |
| percent_state_change          | 0.00                                         | FLOAT     |                                           |
| performance_data              | rta=0.062ms;200.000;500.000;0; pl=0%;40;80;; | STRING    |                                           |
| plugin_output                 | OK - 192.168.47.21: rta 0.062ms, lost 0%     | STRING    |                                           |
| problem_has_been_acknowledged | 0                                            | INTEGER   |                                           |
| process_performance_data      | 0                                            | INTEGER   |                                           |
| retry_interval                | 1.000000                                     | FLOAT     |                                           |
| scheduled_downtime_depth      | 0                                            | INTEGER   |                                           |
| should_be_scheduled           | 1                                            | INTEGER   |                                           |
| state_type                    | 1                                            | INTEGER   |                                           |




### service status

| field name                    | content     | type      | comment                      |
| ----------                    | -------     | ----      | -------                      |
| acknowledgement_type          | 0           | INTEGER   | 0-none 1-normal 2-sticky |
| active_checks_enabled         | 1           | BOOLEAN   | 0-disabled 1-enabled       |
| check_command                 | sys2wiki    | STRING    |                              |
| check_execution_time          | 0.149       | FLOAT     |                              |
| check_interval                | 30.000000   | FLOAT     | refers to interval_length in nagios.cfg |
| check_latency                 | 0.153       | FLOAT     |                              |
| check_options                 | 0           | INTEGER   |                              |
| check_period                  | 24x7        | STRING    |                              |
| check_type                    | 0           | INTEGER   |                              |
| current_attempt               | 4           | INTEGER   |                              |
| current_event_id              | 12          | INTEGER   |                              |
| current_notification_id       | 0           | INTEGER   |                              |
| current_notification_number   | 0           | INTEGER   |                              |
| current_problem_id            | 11          | INTEGER   |                              |
| current_state                 | 1           | INTEGER   |                              |
| event_handler_enabled         | 1           | INTEGER   |                              |
| event_handler                 |             | ??        |                              |
| failure_prediction_enabled    | 1           | INTEGER   |                              |
| flap_detection_enabled        | 1           | INTEGER   |                              |
| has_been_checked              | 1           | INTEGER   |                              |
| host_name                     | common      | STRING    |                              |
| is_flapping                   | 0           | INTEGER   |                              |
| last_check                    | 1239557533  | TIMESTAMP |                              |
| last_event_id                 | 0           | INTEGER   |                              |
| last_hard_state_change        | 1232862249  | TIMESTAMP |                              |
| last_hard_state               | 1           | TIMESTAMP |                              |
| last_notification             | 0           | TIMESTAMP |                              |
| last_problem_id               | 0           | INTEGER   |                              |
| last_state_change             | 1232862069  | TIMESTAMP |                              |
| last_time_critical            | 0           | TIMESTAMP |                              |
| last_time_ok                  | 0           | TIMESTAMP |                              |
| last_time_unknown             | 0           | TIMESTAMP |                              |
| last_time_warning             | 1239557533  | TIMESTAMP |                              |
| last_update                   | 1239558120  | TIMESTAMP |                              |
| long_plugin_output            |             | STRING    |                              |
| max_attempts                  | 4           | INTEGER   |                              |
| modified_attributes           | 0           | INTEGER   |                              |
| next_check                    | 1239559333  | TIMESTAMP |                              |
| next_notification             | 0           | ???       |                              |
| no_more_notifications         | 0           | INTEGER   |                              |
| notification_period           | 24x7        | STRING    |                              |
| notifications_enabled         | 0           | INTEGER   |                              |
| obsess_over_service           | 1           | INTEGER   |                              |
| passive_checks_enabled        | 1           | INTEGER   |                              |
| percent_state_change          | 0.00        | FLOAT     |                              |
| performance_data              |             | STRING    |                              |
| plugin_output                 | (null)      | STRING    |                              |
| problem_has_been_acknowledged | 0           | INTEGER   |                              |
| process_performance_data      | 0           | INTEGER   |                              |
| retry_interval                | 1.000000    | FLOAT     |                              |
| scheduled_downtime_depth      | 0           | INTEGER   |                              |
| service_description           | System Info | STRING    |                              |
| should_be_scheduled           | 1           | INTEGER   |                              |
| state_type                    | 1           | INTEGER   |                              |

