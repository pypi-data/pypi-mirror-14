"""
Uses Linux kernel capabilities to make sandbox possible. It runs all scripts
as the `nobody` user. For this to work we need a python executable with the
SETUID capability enable. Do these steps::

    $ cp /usr/bin/python3.4 /usr/bin/python_setuid
    $ setcap cap_setuid+ep /usr/bin/python_setuid

Of course the first command should be adapted to the correct name/version of
your Python executable. Remember that in most distributions /usr/bin/python or
/usr/bin/python3 are simply symlinks to the correct Python executable. `setcap`
do not work in symlinks, so you should find the correct Python executable.
DO NOT enable SETUID capability in the main Python interpreter because this can
make your system vulnerable. This library would not use it anyway...
"""

import sys
import base64
import importlib
from subprocess import PIPE, Popen


def run(target, args=(), kwargs=None, *, timeout=None, pickler='pickle',
        imports=[], user='nobody'):
    """Simple sandboxing based on a python executable with setuid capabilities.

    This sandboxing relies on changing the uid to the unprivileged user nobody.
    """

    # Preload modules
    pickle = importlib.import_module(name=pickler)
    try:
        imports = list(imports)
        imports.append(target.__module__)
    except AttributeError:
        pass
    if pickler != 'pickle':
        imports.append(pickler)
    prefix = pickle.dumps(imports)
    prefix = base64.b85encode(prefix) + b'\n'

    # Adds user
    prefix += b'%s\n' % (user.encode('utf8'))

    # Encode message
    kwargs = dict(kwargs or {})
    args = tuple(args)
    message = pickle.dumps((target, args, kwargs))
    message = base64.b85encode(message) + b'\n\n'

    # Transmit message to subprocess
    cmd = ['python_setuid', '-m', 'boxed.simplebox']
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    box_out, box_err = proc.communicate(input=prefix + message, timeout=timeout)

    if box_err:
        error_code = proc.poll()
        func_name = getattr(target, '__name__', str(target))
        err_msg = box_err.decode('utf8')
        err_msg = '\n'.join('    ' + line for line in err_msg.splitlines())
        raise RuntimeError(
            'error running function %s with args=%s and kwargs=%s: '
            'return code is %s.\n'
            '%s' % (func_name, args, kwargs, error_code, err_msg)
        )

    decoded = base64.b85decode(box_out[:-1])
    response, ex, (out, err) = pickle.loads(decoded)
    print(out, end='')
    print(err, end='', file=sys.stderr)
    if ex is None:
        return response
    else:
        raise ex
