======= check_multi concepts =======
#  Execution - locally or remotely 

Where should check_multi be executed? Locally on the Nagios server or remotely on the server to be monitored?
Either is possible - it depends on your needs.

### Remote execution on the client server

The 
#### Pros

*  Most efficient way of monitoring - saves ressources of the Nagios server by using the ressources of the monitored server

*  Only one network connection is used, only one SSH or NRPE connection is to be opened.
#### Cons

*  Plugins and check_multi configuration have to be distristributed on the remote server.

*  Authentication is needed to access the remote server.

### Local execution on the Nagios server

Sometimes its not possible to execute plugins on a remote server, e.g. because its an appliance. Then all checks have to be executed on the Nagios server itself.  

#### Pros

*  Normally no authentication is needed to access the remote server.

*  Plugins and check_multi configuration do not have to be distristributed on the remote server, they are all available on the Nagios server.
#### Cons

*  Less efficient way of monitoring - multiple ressources of the Nagios server are used to monitor a remote server. 

*  Multiple network connections are used to research the remote server, per check one.

