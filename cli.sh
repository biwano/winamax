#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd 
)"
cd $DIR
venv/bin/python cli.py $@

