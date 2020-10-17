## Configuration

Although *check_multi* has numerous options and a configuration file the configuration is more or less simple.

For the beginning you only need the file option ```-f``` and can start with the command line:

```
	$ check_multi -f contrib/check_multi.cmd
```
That's all.

For the details have a look into the [format description of the command file](configuration/commands.md) and the [plugin call options](configuration/commands.md).

The [nagios integration](configuration/nagios.md) is plain forward and the [Macro support](configuration/macros.md) is a feature often used in large installations.
