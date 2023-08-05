#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
if python setup.py bdist_wheel; then
    echo
    echo
    echo -n "User module built: "
    find "$(pwd)" -name '*.whl'
    echo
fi

