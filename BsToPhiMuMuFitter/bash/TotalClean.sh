#!/bin/bash

SOURCE="${BASH_SOURCE[0]}" #Dir of TotalClean.sh
sm="$(dirname $0)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

GITDIR=$(git rev-parse --show-toplevel)
cd $GITDIR && find . -name "*.pyc" -type f -delete
rm -f $DIR/../data/*
rm -f $DIR/../input/selected/* 
rm -f $DIR/../input/*.root
rm -f $DIR/../Plots/*
cd $DIR/../cpp
rm -f *.pcm *.d *.so
