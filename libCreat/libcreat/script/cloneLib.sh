#!/bin/bash
#
# vim: sts=4 sw=4 et ai si

set -o xtrace

PROG=${BASH_SOURCE[0]:-$0}

if [ $# -lt 1 ]; then
echo "Usage: $PROG <giturl>"
exit 255
fi

BASE_DIR=$(cd $3; pwd)
GITURL="$1"

echo "BASE_DIR: $BASE_DIR"
echo "REPOS: $REPOS"

cd "${BASE_DIR}"

git clone ${GITURL} $2

cd $2
git pull

cd -
cd -