#!/bin/bash
#
# vim: sts=4 sw=4 et ai si

set -o xtrace

PROG=${BASH_SOURCE[0]:-$0}

if [ $# -lt 1 ]; then
echo "Usage: $PROG <basedir>"
exit 255
fi

echo $1

BASE_DIR=$(cd "$1"; pwd)

cd ${BASE_DIR}
git add . 
git commit -m 'no message'
git push origin master
