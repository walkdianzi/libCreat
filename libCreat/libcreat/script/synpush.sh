#!/bin/bash
#
# vim: sts=4 sw=4 et ai si

set -o xtrace

PROG=${BASH_SOURCE[0]:-$0}

if [ $# -lt 2 ]; then
echo "Usage: $PROG <basedir> <tag>"
exit 255
fi

echo $1

BASE_DIR=$(cd "$1"; pwd)

cd ${BASE_DIR}
git add . 
git commit -m 'no message'
git tag -d $2
git push origin :refs/tags/$2
git tag $2
git push origin master
git push origin $2
