from os import listdir

import pickle

import pytest
from pytest import warns

from unittest.mock import MagicMock
from unittest.mock import patch

from discopy import rigid
from discopy.cat import Ob
from discopy.utils import *
from discopy.tensor import Box

import pytest
from pytest import warns

from os import listdir
import sys
import pkgutil
import pickle

zip_mock = MagicMock()
zip_mock.open().__enter__().read.return_value =\
    '[{"factory": "cat.Ob", "name": "a"}]'


@patch('urllib.request.urlretrieve', return_value=(None, None))
@patch('zipfile.ZipFile', return_value=zip_mock)
def test_load_corpus(a, b):
    assert load_corpus("[fake url]") == [Ob("a")]


def test_deprecated_from_tree():
    tree = {
        'factory': 'discopy.rigid.Diagram',
        'dom': {'factory': 'discopy.rigid.Ty',
                'objects': [{'factory': 'discopy.rigid.Ob', 'name': 'n'}]},
        'cod': {'factory': 'discopy.rigid.Ty',
                'objects': [{'factory': 'discopy.rigid.Ob', 'name': 'n'}]},
        'boxes': [], 'offsets': []}
    with warns(DeprecationWarning):
        assert from_tree(tree) == rigid.Id(rigid.Ty('n'))


def test_named_generic_cache():
    from discopy import tensor as dt
    box, box_int, box_float = dt.Box, dt.Box[int], dt.Box[float]
    assert box_int is dt.Box[int]
    assert box is not box_int and box_float is not box_int
    diag_int = dt.Diagram[int]
    assert diag_int is dt.Diagram[int]
    assert box_int is dt.Box[int]



@pytest.mark.parametrize('fn', listdir('test/utils/pickles/main/'))
def test_pickle_version_compatibility(fn):
    with open(f"test/utils/pickles/main/{fn}", 'rb') as f:
        new = pickle.load(f)
    with open(f"test/utils/pickles/0.6/{fn}", 'rb') as f:
        old = pickle.load(f)
    assert old == new


@pytest.mark.parametrize('pkg', [module for _, module, _ in pkgutil.iter_modules(["test/utils/pickles/src"])])
def test_pickle_unpickle(pkg):
    sys.path.append('test/utils/pickles/src')
    impmodule = __import__(pkg)
    exp = impmodule.pick
    act = pickle.loads(pickle.dumps(impmodule.pick))
    assert act == exp

def test_parameterised_box_pickle():
    box = Box("A", 2, 3)
    assert pickle.loads(pickle.dumps(box)) == box
