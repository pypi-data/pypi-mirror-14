CRUSH HA
========
Proof of concept of using CRUSH maps for HA node placement

Based off of crush maps from `ceph <http://ceph.com>`_ and research paper 
behind it by (linked `here <http://ceph.com/papers/weil-crush-sc06.pdf>`_)

A Gentle Introduction
----------------------
The CRUSH Algorithm as it is used in ceph is used to determine on which nodes 
data of interest may be stored without a central controller. This is done with 
'buckets' that define the relationship between nodes (or in the case of ceph 
OSDs) and their failure/allocation domains and a set of rules which specify the 
placement of data on these nodes (and therefore their high availability 
characteristics) and is implemented as a simple VM that operates on the 
buckets.

To put it more simply, the buckets define the 'topology' of your setup (how 
things are linked and how they should fail) and rules define which nodes you 
select for data and operate on these buckets. By manipulating the rules in 
relationship to the failure domains in the buckets you can define arbitrary HA 
polices that prevent against any type of data loss in a generic fashion.

Why you may want to use it
--------------------------
This library or its concepts may be of sue for the following problems

 * cache server selection
 * locating services in a cluster without a central controller
 * making placement decisions for data/jobs
 * reference for building basic byte code interpreters

Available Commands
------------------
As this implementation uses an interpreter, there are several instructions that 
you can use. these map almost 1:1 with those from the original paper with some 
slight modification.

use
++++
The use command is used to select a bucket other than the default one provided 
to the interpreter, eg when you have to select a specific rack or geographical 
region. As the buckets form a tree this updates the root to point to the 
specified bucket. Note that you can still go back to the original root with 
another use command.

select
++++++
Select looks for nodes of the specified type and amount and places them on the 
stack. This is typically part of a 'wide' operation or 'left to right' 
operation where the intent is to cover as many possibilities before drilling 
down.

take
++++
Take is the counter part to select, unlike select this is a 'deep' or 'top to 
bottom' operation. For each item on the stack take will select count number of 
nodes

emit
++++
Emit takes the currently accumulated node choices and sends them back to the 
caller while resetting the node list and stack list. This is useful as a 
barrier if you have 2 types of criteria that need to be satisfied eg 2 nodes 
locally, then a node remotely. Selection of the first 2 nodes would be done with 
the above rules then 'emited', resetting the decision tree. The next set of 
instructions would then satisfy the remote node selection and not be 
constrained by earlier selections.

Tools
-----
The following command can be used to run a demo program:

    $ python -m crushha.interpreter

While the output is not that interesting the src code backing it may be of use 
if you intend to use this module. Setting up and enabling logging will also 
give a highly detailed and annotated look into the decisions behind each nodes 
selection for auditing purposes.

Current State
--------------
This module is currently in a very alpha state and subject to change however 
the api defined by the implementation is about 80% of the way there. This will 
be designed as a coroutine due to the requirement to be able to generate an 
arbitrary long list of nodes from a large pool and the iteration model it 
provides has proved useful to work with

The current design makes use of 'yield from' from python 3.3, python versions 
before this will not be considered as a porting target due to the complexity of 
the required trampolines to make it work correctly. The code is simple and is 
intended to stay so.

The Future
----------
 * Unit tests
 * Docs
 * Better defined op codes
 * slight optimization for shorter rules (eliminating buckets by name in 
   select)
 * Finalization of the API
 * More examples
 * hash ring bucket types

Repo: `blitz.works <http://blitz.works/crushha>`_
Docs: `docs@blitz.works <http://docs.blitz.works/crushha>`_ # comming soon
Email: code at pocketnix.org


Changelog
---------

0.2 2016-04-03
##############

* Added implicit 'emit' rule to all chains passed to the intepreter
* Basic test suite added
* Interpreter now checks there are rules to avoid infinite loops (this does not eliminate all infinite loops)

0.1 2016-04-02
##############

* Inital Release
* Working interpreter
* Example code in interpreter.py


