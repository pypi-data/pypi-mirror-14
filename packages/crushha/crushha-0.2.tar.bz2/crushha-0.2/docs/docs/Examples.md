Examples
========
The interpreter module includes example code of how to use the module. The 
output of this command can be seen by invoking the module as below:

    $ python -m crushha.interpreter
    <Bucket(node1, node, [])>
    <Bucket(node4, node, [])>
    <Bucket(node2, node, [])>
    <Bucket(node3, node, [])>
    <Bucket(node5, node, [])>
    <Bucket(node6, node, [])>
    Could not satisfy constraints of rule, erroring on rule 3
     - use(bucket=<Bucket(sydney, region, ['dc1', 'dc2'])>)
     - select(type='datacenter', count=2)
    => take(count=1)
     - emit()
     - use(bucket=<Bucket(default, root, ['sydney', 'melbourne'])>)
     - take(count=1)
     - emit()

As you can see in the above, the code prints out 6 nodes and then indicates an 
issue with the rules. In this case there are only 6 nodes in the Buckets in the 
CRUSH map and hence no more are available to take when the 'take' rule is 
encountered.

A full CRUSH map is made of 2 parts, of which one is partially visible in the 
above example (The CRUSH hierarchy of failure domains) and the other is printed 
out in full (The ruleset that operates on this hierarchy).

The failure domain hierarchy is a tree structures that can have multiple roots. 
That defines the 'failure domains' and the relationship between them. `crushha` 
does not attempt to enforce specific domains however examples of classic 
failure domains are 'region', 'datacenter', 'rack', 'pdu', 'chassis' and host. 
By defining the relationship rules can be created to prevent particular types 
of scenarios. The ruleset in the example above is intended to select 2 machines 
in Sydney and another offsite datacenter to prevent against failure of a 
datacenter and subsequent data loss. 

Diving into the Ruleset above further, the ruleset operate at the level of 
datecenters as defined by the select and use rules. as no further selection of 
nodes lower in the hierarchy are used, the take command is free to select from 
any machine below those points in the CRUSH failure domain hierarchy

Select statements are generally intended to be 'wide' or provide left/right 
transversal of a tree. as failure domains are intended to be ordered, select 
statements provide this horizontal navigation inside a type of failure domain.

Use can be used to restrict the scope of this left/right movement of select and 
is useful for ensuring a specific property of your intended availability is 
enforced, eg selecting a close by data center. This is best used with multiple 
roots as tree with one 'default' root may become constraining in expressing 
these other desired properties.

Take is a 'vertical' operation intended to select destination nodes. It will 
place a node on the stack as many times as requested for each previously 
selected item. The combination of select and take has a n*m relationship where 
n is the amount of selected nodes and m is the amount of nodes take is 
requested to return

Finally Emit returns these nodes to the caller and resets the state of the VM. 
There is an implicit Emit at the end of all rulesets that gets added by the 
interpreter and as such the last Emit statement may be omitted. Emit is best 
used as a 'barrier' due to its 'reset the world' nature, it can be used to 
separate explicit requirements of your HA plan. In the above example it is used 
as a barrier to select 2 nodes locally, then once the state is reset, select a 
remaining offsite DC. 2 separate and isolated concerns that are best dealt with 
separately. This also has the effect of ordering meaning that nodes at the 
local DC are emitted first, then once a critical point is reached (3 nodes in 
the above example) off site redundancy is achieved.
