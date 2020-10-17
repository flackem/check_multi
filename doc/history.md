# History

## Motivation and design

One real disadvantage of Nagios is the lack of historical data. I don't mean performance data in this context, but all kinds of numerical data, in order to do special stuff with it like comparison, calculation, averaging, weighting and last not least to build rules with it to extend the state logic.

I know that we can extract such data from the performance data RRD files, but my approach is plugin based, so I need the data accessible for the plugin, which may reside on a server apart from the Nagios server.

The base of check_multi history storing is a simple lean ASCII file. It contains pairs of timestamps and values, simply stored in one line per child check, prepended by the child check's tag.

```sensor 1359723944:10.23 1359723947:10.23 1359723948:10.23 1359723957:0.65 1359723959:0.65 1359723960:0.65 1359723972:0.47 1359723976:0.49 1359723978:0.49 1359725189:10.23 1359727304:10.23 1359727310:10.23```

Only the last values are of interest, let's pass the description of the past to the performance graphing guys.
So the values are stored into a ring buffer, where older values are cleaned up. Values will be kept per default for the last day, which are 288 values on a base of a 5 minutes check interval.

I you do not need that many values - eg. only the last hour - feel free to adopt the history_minvalues attribute.

So if we now have a database of the last numerical values of a check, what can we do with it?

*  Calculate the average of the last 3 values and get rid of Nagios SOFT / HARD state logic.

*  Raise an alarm, if the average delta over the last hour double extends the delta over the last day.

*  Notice if the load during the night is higher than the load during office hours.

*  Calculate the space trend of a disk and raise an alarm to order new storage when the time its getting full will come in the next 2 month.

*  You have a device which states codes like 23 (OK), 17 (CRIT) and sometimes it also spits out erraneous numbers, but only for short times? Then work with averaging over 3 intervals and you're clean.

*  For more use cases have a look at the examples below.

## Goodie

check_multi's history does **not** depend on regular check_intervals. If you eg. use passive checks with varying intervals, check_multi calculates the values based on the given time between the measuring points, using its stored timestamps.

This also means that you will earn perfectly valid results if you have a small check interval during office hours, but a larger interval during night.

## Cooking list

 1.  Use a check_multi release past 0.26_580
 2.  Switch on history: -s history=1
 3.  History calculations are based on child check values, so use child check states:

```
command   [ non_root           ] = ps -ef | grep -v ^root | wc -l
attribute [ non_root::critical ] = AVERAGE(10) > 50
```
 1.  Test it on command line until it works. This is pretty convenient compared to waiting on Nagios check intervals.
 2.  If you're unsure about the calculated result, ask the debugging:```check_multi ... -vvv | grep history_debug```
 3.  And if all works: pass it to Nagios config control and enjoy. ;)

## Available Macros

| Macroname              | Description                                             | 
| ---------              | -----------                                             | 
| AVERAGE                | Arithmetic average                                      | 
| WEIGHTED_AVERAGE       | Arithmetic average with higher prio on the last values  | 
| DELTA                  | Absolute difference between values                      | 
| AVERAGE_DELTA          | Computes average delta over a couple of values          | 
| WEIGHTED_AVERAGE_DELTA | Same as AVERAGE_DELTA, but with prio on the last deltas | 
| MIN                    | Minimum value of a given range                          | 
| MAX                    | Maximum value of a given range                          | 

## Macro calling and parameters

Macros may be called with one or two parameters:
 1.  One parameter: the last N intervals will be taken for consideration. 
 2.  Two parameters: both intervals are Unix timestamps, they form a timeframe, in which the macros are calculated

Note that you can use perl expressions for the timestamps, e.g. time (now), or time - 3600 (one hour past).
A macro with AVERAGE(time,time-3600) covers the last hour.






