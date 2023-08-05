import math
import os
import pytest
from ejudge.sandbox import run


def write_to_file(path, data):
    with open(path, 'w') as F:
        F.write(data)


def test_basic_sandbox_run():
    assert run(math.sqrt, args=(4.0,)) == 2.0


def test_forbidden_sandbox_run():
    try:
        write_to_file('trash.dat', 'foo')
        with pytest.raises(RuntimeError):
            run(os.unlink, args=('trash.dat',))
    finally:
        os.unlink('trash.dat')


if __name__ == '__main__':
    pytest.main('test_sandbox.py')
