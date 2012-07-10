#!/bin/sh

echo 'Specification doctests'
echo '----------------------'
python -m doctest tests/specs.md && echo 'OK\n'
echo '* Headers doctests'
echo '----------------------'
python -m doctest tests/headers.md  && echo 'OK\n'
echo '* Request doctests'
echo '----------------------'
python -m doctest tests/request.md  && echo 'OK\n'
echo '* Response doctests'
echo '----------------------'
python -m doctest tests/response.md  && echo 'OK\n'


