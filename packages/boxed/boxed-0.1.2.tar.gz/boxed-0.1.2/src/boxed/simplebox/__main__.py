import io
import os
import pwd
import pickle
import base64
import traceback
import importlib


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
    if not data:
        break
    data = base64.b85decode(data)
    func, args, kwds = pickle.loads(data)

    # Execute
    try:
        result = func(*args, **kwds), None, None
    except Exception as ex:
        out = io.StringIO()
        traceback.print_tb(ex.__traceback__, file=out)
        result = (None, ex, out.getvalue())
    out = base64.b85encode(pickle.dumps(result))
    print(out.decode('utf8'))
