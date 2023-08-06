CRUSH HA
=========
`crushha` is a python implemnetation of CRUSH maps as per the CRUSH paper at 
[ceph.com](http://ceph.com/papers/weil-crush-sc06.pdf). The implementation does 
not attempt to stick stricktly to the paper, namely the operations implementing 
the rules are slightly diffrent and enhanced to make them easier to use.

Where possible the interfaces are designed to be 'streaming' owing to the 
nature of the maps ie returning a possibly infinite ammount of nodes on 
request. Making them ideal for use in iteration or for loops.
