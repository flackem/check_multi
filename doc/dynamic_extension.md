======= Dynamic extension ========
 1.  check_multi is a perl plugin, its internal routines are visible for the eval child checks. 
 2.  And its main loop which executes the child checks is not limited.
These two prerequisites are necessary for the dynamic extension of child checks during runtime.
