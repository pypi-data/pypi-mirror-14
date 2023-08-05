from functools import partial

#
# C/C++ support for IO problems
#
"""
# TCC
ioregister(
    'tcc', 'ANSI C (tcc compiler)',
    partial(compiled_builder, '.c', ['tcc', 'main.c', '-o', 'main.exe', '-w']),
    compiled_runner,
    ['c'],
)

# GCC
ioregister(
    'gcc', 'ANSI C (gcc compiler)',
    partial(compiled_builder, '.c', ['gcc', 'main.c', '-o', 'main.exe']),
    compiled_runner,
    ['c'],
)

# Clang
ioregister(
    'clang', 'ANSI C (clang compiler)',
    partial(compiled_builder, '.c', ['clang', 'main.c', '-o', 'main.exe']),
    compiled_runner,
    ['c'],
)
"""
