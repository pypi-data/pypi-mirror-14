#!/bin/bash

# Set params.
TYPE=$1

# Extend python path.
export PYTHONPATH=$PYTHONPATH:$PWD

# Activate target virtual env.
#source ~/virtualenv/venv/bin/activate

# Serialization tests.
#if [ $TYPE = "s" ]; then
#    echo :: Executing serialization tests
#    nosetests -v -s .../test_serialization.py

# Publishing tests.
#elif [ $TYPE = "p" ]; then
#    echo :: Executing publishing tests
#    nosetests -v -s .../test_publishing.py

# General tests.
#elif [ $TYPE = "g" ]; then
#    echo :: Executing general  tests
#    nosetests -v -s .../test_general.py

#fi

script_path="$(readlink -f ${BASH_SOURCE[0]})"
dir_path="$(dirname $script_path)"

nosetests $dir_path -v --exe --nocapture --nologcapture

exit 0
