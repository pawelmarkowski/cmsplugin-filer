#!/bin/bash

if grep docker /proc/1/cgroup -qa &>/dev/null; then
    echo "Running pip-compile commands. This may take a while..."
    pip-compile --upgrade
    pip-compile --upgrade -o requirements-dev.txt requirements-dev.in
else
    docker build -f Dockerfile.piptools -t pip-tools .
    docker run -v $(pwd):/pip-tools --rm -it pip-tools
fi
