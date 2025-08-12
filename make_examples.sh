#!/bin/bash

> examples/examples.md

for dir in examples/e[0-9]*; do
    [[ -d "$dir" ]] || continue
    echo "Processing: $dir"
    if (cd "$dir" && ./make.sh); then
        echo "Success"
    else
        echo "Failure"
    fi
done