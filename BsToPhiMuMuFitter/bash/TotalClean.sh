#!/bin/bash

SOURCE="${BASH_SOURCE[0]}" #Dir of TotalClean.sh
sm="$(dirname $0)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

GITDIR=$(git rev-parse --show-toplevel)
cd $GITDIR && find . -name "__pycache__" -type d -exec rm -r "{}" \;
rm -f $DIR/../data/*.root
rm -f $DIR/../input/*.root
rm -rf $DIR/../plots_*/*
cd $DIR/../cpp
rm -f *.pcm *.d *.so
