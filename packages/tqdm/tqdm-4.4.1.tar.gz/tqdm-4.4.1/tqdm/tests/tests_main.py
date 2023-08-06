import sys
import subprocess
from tqdm import main
from docopt import DocoptExit
from copy import deepcopy

from tests_tqdm import with_setup, pretest, posttest, _range


def _sh(*cmd, **kwargs):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            **kwargs).communicate()[0].decode('utf-8')


# WARNING: this should be the last test as it messes with sys.stdin, argv
@with_setup(pretest, posttest)
def test_main():
    """ Test command line pipes """
    ls_out = _sh('ls')
    ls = subprocess.Popen(('ls'), stdout=subprocess.PIPE)
    res = _sh('python', '-c', 'from tqdm import main; main()',
              stdin=ls.stdout, stderr=subprocess.STDOUT)
    ls.wait()

    # actual test:

    assert (ls_out in res)

    # semi-fake test which gets coverage:
    try:
        _SYS = (deepcopy(sys.stdin), deepcopy(sys.argv))
    except:
        pass

    sys.stdin = map(str, _range(int(1e3)))
    sys.argv = ['', '--desc', 'Test command line pipes',
                '--ascii', 'True', '--unit_scale', 'True']
    import tqdm.__main__  # NOQA

    sys.argv = ['', '--bad', 'arg',
                '--ascii', 'True', '--unit_scale', 'True']
    try:
        main()
    except DocoptExit as e:
        if """Usage:
    tqdm [--help | options]""" not in str(e):
            raise

    try:
        sys.stdin, sys.argv = _SYS
    except:
        pass
