'''
Import builtin functions for easy recovery when a script or a preparation
routine messes with Python's __builtins__.
'''

# Save this for later
__name = __name__
__package = __package__

# Make source code analysis happy
print = print  # @ReservedAssignment
input = input  # @ReservedAssignment

# Import all names from builtins
D = globals()
__original = {}
try:
    D.update(__builtins__)
    __original.update(__builtins__)
except TypeError:
    for value in dir(__builtins__):
        D[value] = getattr(__builtins__, value)
        __original[value] = getattr(__builtins__, value)
        del value

# Recover real name and package
__name__ = __name  # @ReservedAssignment
__package__ = __package  # @ReservedAssignment
del D


#
# Utility functions for messing with builtins
#
def save_name(name, function):
    '''Saves a function to the __builtin__ module'''

    try:
        __builtins__[name] = function
    except TypeError:
        setattr(__builtins__, name, function)


def update(D={}, **kwds):
    '''Update the __builtin__ module with the given values'''

    D = dict(D)
    D.update(kwds)
    for k, v in D.items():
        save_name(k, v)


def restore():
    '''Restores builtins to original state'''

    try:
        D = __builtins__
        D.clear()
        D.update(__original)
    except AttributeError:
        mod = __builtins__
        for name in dir(mod):
            if name in __original:
                value = __original[name]
                setattr(mod, name, value)
            else:
                delattr(mod, name)
