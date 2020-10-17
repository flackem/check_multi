======= Caching =======

Not every Check needs to be executed in the classical 5 minutes time interval. There are checks to be executed once per hour or only once a day. 

check_multi respects this with caching old values. This is implemented with storing

*  a interval attribute for each child check

*  caching the old output and RC
After the interval is finished a new check is initiated and the result is stored in the temporary file.
