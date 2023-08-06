#!/usr/bin/env python4

from collections import namedtuple
from itertools import cycle
from . import log as parent_log

# intrrucsions:
# select(type, n)
#  - Take n items of type type out of selection and put them in the accumulator
# take(type, n)
#  - Take n items of type type out of selection and select a single leaf node
#    for each selection
# emit
#  - emit all results accumulated so far and restart at top of tree

log = parent_log.getChild(__name__)

use_cmd = namedtuple('use', 'bucket')
select_cmd = namedtuple('select', 'type count')
take_cmd = namedtuple('take', 'count')
emit_cmd = namedtuple('emit', '')

class InterpreterError(Exception): pass

class ConstraintError(InterpreterError):
    def __init__(self, msg, rule_num, *args, **kwargs):
        self.msg = msg
        self.rule_num = rule_num
        self.args = (msg, rule_num) + args
        
class EmptyRulesError(InterpreterError): pass

class Bucket:
    def __init__(self, name, typ, children=[]):
        self.name = name
        self.typ = typ
        self.children = children or []
    def __repr__(self):
        child_names = [x.name for x in self.children]
        return "<{}({}, {}, {})>".format(self.__class__.__name__, self.name, self.typ, child_names)


def select(node, typ):
    if node.typ == typ:
        yield node
    else:
        for child in node.children:
            yield from select(child, typ)

def interpret(cmds, root):
    used = set()
    rule_num = 0
    
    if not cmds:
        raise EmptyRulesError()
    
    try:
        while True:
            accumulator = []
            nodes = []
            # We inject an implicit emit command here to esure that data
            # gets drained, makes simple rules shorter and makes the rules
            # slghtly more robust
            for i, cmd in enumerate(cmds + [emit_cmd()]):
                rule_num = i
                if isinstance(cmd, use_cmd):
                    log.debug("Got use command")
                    log.debug("- Using bucket " + cmd.bucket.typ)
                    root = cmd.bucket
                elif isinstance(cmd, select_cmd):
                    log.debug("Got select command")
                    log.debug("- Attempting to select {} buckets of type {}".format(cmd.count, cmd.type))
                    selector = select(root, cmd.type)
                    for i in range(cmd.count):
                        val = next(selector)
                        log.debug("- Found bucket of correct type")
                        accumulator.append(val)
                elif isinstance(cmd, take_cmd):
                    log.debug("Got take command")
                    log.debug("- {} items in accumultor".format(len(accumulator)))
                    log.debug("- Selecting {} items for each".format(cmd.count))
                    if not accumulator:
                        log.debug("- Accumulator empty, willing with current root")
                        accumulator.append(root)
                    for root in accumulator:
                        selector = select(root, 'node')
                        for i in range(cmd.count):
                            # infininte iteration here is fine. we will run out of entries
                            # and that id dictated by how wide the selector is
                            while True:
                                node = next(selector)
                                if node not in used:
                                    log.debug("- Found node")
                                    nodes.append(node)
                                    used.add(node)
                                    break
                elif isinstance(cmd, emit_cmd):
                    log.debug("Got emit command")
                    while nodes:
                        yield nodes.pop(0)
                    accumulator = []
                    log.debug("- Erased accumlator")
    except StopIteration as err:
        log.debug("Rule number {} cannot be satisfied".format(rule_num + 1))
        raise ConstraintError("Could not satisfy constraints, out of valid nodes", rule_num) from err

if __name__ == "__main__":
    buckets = {}

    node1 = Bucket('node1', 'node')
    node2 = Bucket('node2', 'node')
    node3 = Bucket('node3', 'node')
    node4 = Bucket('node4', 'node')
    node5 = Bucket('node5', 'node')
    node6 = Bucket('node6', 'node')
    dc1 = Bucket('dc1', 'datacenter', [node1, node2, node3])
    dc2 = Bucket('dc2', 'datacenter', [node4, node5])
    dc3 = Bucket('dc3', 'datacenter', [node6])
    syd_region = Bucket('sydney', 'region', [dc1, dc2])
    mlb_region = Bucket('melbourne', 'region', [dc3])
    default = Bucket('default', 'root', [syd_region, mlb_region])

    select_2_in_syd_and_one = [
        use_cmd(syd_region),
        select_cmd('datacenter', 2),
        take_cmd(1),
        emit_cmd(),
        use_cmd(default),
        take_cmd(1),
        emit_cmd(),
    ]

    rule = select_2_in_syd_and_one
    map = interpret(rule, default)
    try:
        for i in range(7):
            print(next(map))
    except ConstraintError as err:
        print("Could not satisfiy constraints of rule, erroring on rule {}".format(err.rule_num + 1))
        for i, cmd in enumerate(rule):
            if i == err.rule_num:
                print("=> {}".format(cmd))
            else:
                print(" - {}".format(cmd))
