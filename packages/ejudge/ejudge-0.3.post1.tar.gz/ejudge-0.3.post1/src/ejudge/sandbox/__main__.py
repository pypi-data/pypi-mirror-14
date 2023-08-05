import os
import pwd
import pickle
import base64


# Sets the UID to nobody in order to prevent harm...
userinfo = pwd.getpwnam('nobody')
os.setuid(userinfo.pw_uid)

# Start interaction with Python master: transfer data using b85 encoded pickled
# streams. The main process reads an input string from stdin and prints back
# the result to stdout. This is done until an empty string is received.
while True:
    data = input()
    if not data:
        break
    data = base64.b85decode(data)
    func, args, kwds = pickle.loads(data)
    result = func(*args, **kwds)
    out = base64.b85encode(pickle.dumps(result))
    print(out.decode('utf8'))