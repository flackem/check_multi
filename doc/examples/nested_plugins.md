```
$ check_multi -x 'command [ container1 ] = check_multi -x "command [ check_swap ] = check_swap -w 20 -c 10"' -x 'command [ container2 ] = check_multi -x "command [ check_disk ] = check_disk -w 10 -x 20 -p /"'
OK - 2 plugins checked, 2 ok
[ 1] container1 OK - 1 plugins checked, 1 ok
 [ 1] check_swap SWAP OK - 87% free (7107 MB out of 8198 MB) 
[ 2] container2 OK - 1 plugins checked, 1 ok
 [ 1] check_disk DISK OK - free space: / 2472 MB (25% inode=96%);|check_multi::check_multi::plugins=3 time=1.145895 container1::check_multi::plugins=2 time=0.115744 check_swap::check_swap::swap=7107MB;0;0;0;8198 container2::check_multi::plugins=2 time=0.120307 check_disk::check_disk::/=7067MB;9927;;0;9937
```

