
import pytest
pytest.importorskip('shfshf')
from distributed.joblib import Parallel, delayed
from distributed.utils_test import cluster, loop, inc


def test_interface(loop):
    with cluster() as (s, [a, b]):
        with Executor(('127.0.0.1', s['port']), loop=loop) as e:
            L = Parallel()(delayed(inc)(i) for i in range(10))
            assert L == [inc(i) for i in range(10)]
