## attribute - define child check's attributes

The attribute definition contains particular attributes of a previous given child check.

**Format**
```attribute [ <tag>::<attribute> ] = <content>```

**Elements**

*  **tag**: is the name of a previously defined child check.

*  **attribute**: specifies the name of the attribute to set.

*  **content**: All behind the '=' is the content of this attribute 

** Example 1**

	
```
	command   [ temperature           ] = snmpget ...
	attribute [ temperature::warning  ] = $temperature$ > 100
	attribute [ temperature::critical ] = $temperature$ > 200`</code>`
	
	In this example first the temperature is read via snmpget. Afterwards two rules specify the WARNING or CRITICAL state of this command check.
```
	
