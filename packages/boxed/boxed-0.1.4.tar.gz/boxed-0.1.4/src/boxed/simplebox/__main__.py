import io
import os
import pwd
import sys
import pickle
import base64
import importlib

stdout, stderr, stdin = sys.stdout, sys.stderr, sys.stdin


# Load the list of modules before setuid (the running user may not have access
# to all modules that the calling user has).
data = base64.b85decode(input())
modules = pickle.loads(data)
for mod in modules:
    importlib.import_module(mod)
if 'dill' in modules:
    import dill as pickle
elif 'cloudpickle' in modules:
    import cloudpickle as pickle

# Load the username
user = input()

# Sets the UID to nobody in order to prevent harm...
userinfo = pwd.getpwnam('nobody')
os.setuid(userinfo.pw_uid)


# Start interaction with Python master: transfer data using b85 encoded pickled
# streams. The main process reads an input string from stdin and prints back
# the result to stdout. This is done until an empty string is received.
while True:
    # Fetch data
    data = input()
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    sys.stdin = io.StringIO()

    if not data:
        break
    data = base64.b85decode(data)
    func, args, kwds = pickle.loads(data)

    # Execute
    try:
        ex = None
        result = func(*args, **kwds)
    except Exception as ex:
        result = None, ex, out.getvalue()
    finally:
        out = sys.stdout.getvalue()
        err = sys.stdout.getvalue()
        result = result, None, (out, err)
    out = base64.b85encode(pickle.dumps(result))
    print(out.decode('utf8'), file=stdout)
