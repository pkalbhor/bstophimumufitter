#!/bin/bash

for args in '1A' '1B' '1C' '3' '5A' '5B'
do
    python testOnly.py $args l1
done
