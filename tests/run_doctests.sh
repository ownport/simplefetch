#!/bin/sh

python -m doctest tests/helpers.md && echo '[OK] tests/helpers.md'
python -m doctest tests/connection.md && echo '[OK] tests/connection.md'
python -m doctest tests/proxy.md && echo '[OK] tests/proxy.md'



