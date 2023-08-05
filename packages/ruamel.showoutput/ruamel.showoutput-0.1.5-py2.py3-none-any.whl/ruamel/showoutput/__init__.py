# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import errno
import traceback

_package_data = dict(
    full_package_name="ruamel.showoutput",
    version_info=(0, 1, 5),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="like subprocess.check_output(), but showing progress",
    # keywords="",
    entry_points=None,
    license="MIT",
    since=2016,
    # status: "α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    install_requires=dict(
        # py27=["ruamel.ordereddict"],
    ),
)


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val

version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version

import sys               # NOQA
import time              # NOQA
import subprocess        # NOQA


def show_output(*args, **kw):
    """make sure all args parameters are strings and that the output is unicode,
    show output as it progresses.
    Don't run in parallel in subthreads etc
    """
    verbose = kw.pop('verbose', 0)
    args = list(args)
    args[0] = [str(x) for x in args[0]]
    if verbose > 0:
        print('\ncmd: ' + ' '.join([('"' + x + '"' if ' ' in x else x) for x in args[0]]))
    l = 0
    res = bytes()
    new_line = '\n'.encode('utf-8')
    kw['stdout'] = subprocess.PIPE
    inp = kw.pop('input', None)
    if inp is not None:
        kw['stdin'] = subprocess.PIPE
    p = subprocess.Popen(*args, **kw)
    if inp:
        p.stdin.write(inp)
        p.stdin.close()
    retcode = p.poll()
    line = bytes()
    try:
        while retcode is None:
            data = p.stdout.read(1)
            if data:
                line += data
                l += 1
                if data == new_line:
                    if sys.version_info >= (3,):
                        sys.stdout.write(line.decode('utf-8'))
                    else:
                        sys.tdout.write(line)
                    # no flush, use line buffering
                    res += line
                    line = bytes()
            else:
                time.sleep(0.2)   # only sleep and poll if there is nothing more to read
                retcode = p.poll()
    except KeyboardInterrupt:
        p.terminate()
        sys.exit(1)
    except IOError as e:
        if e.errno == errno.EPIPE:
            sys.exit(2)
        raise
    except BrokenPipeError:  # NOQA   PY3
        sys.exit(1)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(3)
    # might be some more written just before exit
    data = p.stdout.read()
    l += len(data)
    res += data
    if sys.version_info >= (3,):
        data = data.decode('utf-8')
    sys.stdout.write(data)
    sys.stdout.flush()
    if retcode:
        cmd = kw.get("args")
        if cmd is None:
            cmd = args[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=res)
    # print('len', l)
    return res.decode('utf-8')
