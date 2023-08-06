# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import pytest
from magic_constraints import *  # noqa
from magic_constraints.utils import (
    repr_return,
)


def test_validator():
    p = Parameter('a', int, validator=lambda n: n == 42)
    assert p.check_argument(42)
    assert not p.check_argument(0)
    assert not p.check_argument('test')


def test_repr():
    assert (
        repr_return("Parameter(name='a', type_=Sequence[int])") ==
        repr(Parameter(name='a', type_=Sequence[int]))
    )
    assert (
        repr_return(
            "Parameter("
            "name='a', "
            "type_=Sequence[int]"
            ")"
        ) ==
        repr(Parameter(name='a', type_=Sequence[int]))
    )
    # test keyword sorting.
    assert (
        repr_return(
            "Parameter("
            "name='a', "
            "type_=Sequence[int], "
            "default=[1, 2, 3]"
            ")"
        ) ==
        repr(Parameter(
            name='a', type_=Sequence[int], default=[1, 2, 3],
        ))
    )


def test_corner_case():

    with pytest.raises(TypeError):
        Parameter('a', int, default=None)

    with pytest.raises(SyntaxError):
        ReturnType(int, default=1)
