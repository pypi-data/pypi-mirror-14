#!/bin/bash
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${CWD}/../js/less

for i in ../bower_components/highlightjs/styles/*.css; do
    filename="$(basename \"${i}\")"
    style="${filename%.*}"
    echo "\"@import (less) \"$i\";\"" ">" "${style}.less"
    echo "@import (less) \"$i\";" > "${style}.less"
done