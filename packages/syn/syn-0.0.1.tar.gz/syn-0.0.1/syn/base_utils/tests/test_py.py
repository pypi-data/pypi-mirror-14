import six
from nose.tools import assert_raises
from syn.base_utils import hasmethod, mro, import_module, message

#-------------------------------------------------------------------------------
# Class utilities

def test_mro():
    import abc

    assert mro(type) == [type]
    assert mro(int) == [int, object]
    assert mro(1) == [int, object]
    assert mro(abc.ABCMeta) == [abc.ABCMeta]

def test_hasmethod():
    class Foo(object):
        a = 1
        
        def bar(self):
            pass

        @classmethod
        def cbar(cls):
            pass

        @staticmethod
        def sbar():
            pass

    f = Foo()
    f.bar()
    Foo.cbar()
    Foo.sbar()

    assert hasmethod(f, 'bar')
    assert hasmethod(Foo, 'bar')

    assert not hasmethod(f, 'a')
    assert not hasmethod(f, 'foo')

    assert hasmethod(f, 'cbar')
    assert hasmethod(Foo, 'cbar')

    assert not hasmethod(f, 'sbar')
    if six.PY2:
        assert not hasmethod(Foo, 'sbar')
    else:
        assert hasmethod(Foo, 'sbar')

#-------------------------------------------------------------------------------
# Module utilities

def test_import_module():
    import os
    import os.path

    m2 = import_module('os.path')
    assert vars(m2).keys() == vars(os.path).keys()

    m3 = import_module('os')
    assert vars(m3).keys() == vars(os).keys()

#-------------------------------------------------------------------------------
# Exception utilities

def test_message():
    e = TypeError('err')
    assert message(e) == 'err'
    assert message(TypeError()) == ''

#-------------------------------------------------------------------------------
# Unit Test Collection

def test_run_all_tests():
    # pylint: disable=W0612,W0621
    from syn.base_utils import run_all_tests
    var1 = [1]
    var2 = [2]
    var3 = [3]
    var4 = [4]

    def test():
        var1.append(5)
    def test_blah_blah():
        var2.append(6)
    def blank_test():
        var3.append(7)
    def some_other_func():
        var4.append(8) # pragma: no cover
        
    assert 'run_all_tests' in locals()
    run_all_tests(locals(), verbose=True)
    assert var1 == [1,5]
    assert var2 == [2,6]
    assert var3 == [3,7]
    assert var4 == [4]

    def test_error_func():
        raise TypeError('Testing exception trace printing')

    run_all_tests(locals(), verbose=True, print_errors=True)

#-------------------------------------------------------------------------------
# Testing utilities


class EquivObj(object):
    def __init__(self, value):
        self.value = value
    def __eq__(self, x):
        return (self.value == x.value)

class DeepcopyEquivObj(EquivObj):
    def __deepcopy__(self, memo):
        return self
    
class PickleEquivObj(EquivObj):
    def __getstate__(self):
        state = dict(value = self.value + 1)
        return state

    def __setstate__(self, state):
        self.value = state['value']
    

def test_assert_equivalent():
    from syn.base_utils import assert_equivalent

    e1 = EquivObj(1)
    e2 = EquivObj(1)
    e3 = EquivObj(2)

    assert_equivalent(e1, e2)
    assert_raises(AssertionError, assert_equivalent, e1, e3)
    assert_raises(AssertionError, assert_equivalent, e2, e3)
    assert_raises(AssertionError, assert_equivalent, e1, e1)

def test_assert_inequivalent():
    from syn.base_utils import assert_inequivalent

    e1 = EquivObj(1)
    e2 = EquivObj(1)
    e3 = EquivObj(2)

    assert_raises(AssertionError, assert_inequivalent, e1, e2)
    assert_inequivalent(e1, e3)
    assert_inequivalent(e2, e3)
    assert_raises(AssertionError, assert_inequivalent, e1, e1)

def test_assert_deepcopy_idempotent():
    from syn.base_utils import assert_deepcopy_idempotent

    e1 = EquivObj(1)
    e2 = DeepcopyEquivObj(1)

    assert_deepcopy_idempotent(e1)
    assert_raises(AssertionError, assert_deepcopy_idempotent, e2)

def test_assert_pickle_idempotent():
    from syn.base_utils import assert_pickle_idempotent

    e1 = EquivObj(1)
    e2 = PickleEquivObj(1)

    assert_pickle_idempotent(e1)
    assert_raises(AssertionError, assert_pickle_idempotent, e2)

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
