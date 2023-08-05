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


def run(target, args=(), kwargs=None, timeout=None):
    """Run target function in a sandboxed environment and return the results.

    Everything is pickle-encoded and transmitted to the sandboxed children
    process. All arguments must be pickable and any modification the target
    function makes to the input arguments is not transmitted back from the
    function call.
    """
    
    import pickle
    import base64
    from subprocess import PIPE, Popen

    # Encode message
    kwargs = dict(kwargs or {})
    args = tuple(args)
    message = pickle.dumps((target, args, kwargs))
    message = base64.b85encode(message) + b'\n\n'
    
    # Transmit message to subprocess
    cmd = ['python_setuid', '-m', 'ejudge.sandbox']
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    response, err = proc.communicate(input=message, timeout=timeout)
    if proc.poll() != 0:
        raise RuntimeError(err.decode('utf8'))
    
    response = base64.b85decode(response[:-1])
    return pickle.loads(response)
