#!/usr/bin/env py.test


from crushha.interpreter import EmptyRulesError, ConstraintError, Bucket, select
from crushha.interpreter import interpret, use_cmd, select_cmd, take_cmd, emit_cmd
from collections import Iterable
from itertools import islice
from pytest import raises

def test_contraint_error():
    with raises(TypeError):
        # ensure we need at least 2 args
        ConstraintError()

    with raises(TypeError):
        # ensure we need at least 2 args
        ConstraintError('msg')
    
    rule_num = 5    
    exc = ConstraintError('msg', rule_num)

    assert rule_num == exc.rule_num, "Rule number is not in the expected place or is diffrent"

    try:
        raise exc
    except ConstraintError:
        pass
    else:
        pytest.fail("Could not raise ConstraintError as an exception")
    
    
def test_select_basic():
    dc1 = Bucket('dc1', 'datacenter')
    dc2 = Bucket('dc2', 'datacenter')
    dc3 = Bucket('dc3', 'datacenter', [dc2])
    root = Bucket('default', 'root', [dc1, dc3])

    buckets = [x for x in select(root, 'datacenter')]
    # select should not recurse down past a bucket of the type it is
    # looking for becuase buckets should be ordered and not contain
    # buckets of the same or greater type
    assert dc2 not in buckets, "select recursed past 'found' bucket"
    # general sanity check to try and catch other issues
    assert len(buckets) == 2, "too many buckets in list"


def test_select_iterable():
    root = Bucket('default', 'root')

    assert isinstance(select(root, 'datacenter'), Iterable), "select should always return an iterable"


def test_interpreter_basic():
    vm = interpret([], Bucket('default', 'root'))
    assert isinstance(vm, Iterable), "interpreter is not an iterable"

    # Ensure that passing in empty values does not cause infinite loop
    # or return actual buckets
    with raises(EmptyRulesError):
        nodes = islice(interpret([], Bucket('default', 'root')), 1)
        nodes = list(nodes)
