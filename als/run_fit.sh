#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)


     echo "-----------------------------------"
     echo "FIT"
     echo "-----------------------------------"
    python3 $SCRIPT_DIR/fit.py \
        -d $SCRIPT_DIR/sample_data/fit \
        -m $SCRIPT_DIR/model/ \
        -o $SCRIPT_DIR/output/
