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
    out, err = proc.communicate(input=prefix + message, timeout=timeout)

    if proc.poll() == 0:
        decoded = base64.b85decode(out[:-1])
        response, err, msg = pickle.loads(decoded)
        if err is not None:
            print(msg, file=sys.stderr)
            raise err
        return response

    print(err.decode('utf8'), file=sys.stderr)
    raise RuntimeError('error running function %s with args=%s and '
                       'kwargs=%s' % (target, args, kwargs))
