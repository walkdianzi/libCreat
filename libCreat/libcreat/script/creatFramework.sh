#!/bin/bash
#
# vim: sts=4 sw=4 et ai si

set -o xtrace

PROG=${BASH_SOURCE[0]:-$0}

if [ $# -lt 1 ]; then
echo "Usage: $PROG <giturl>"
exit 255
fi

cd $1

pod package $2 --force --embedded --no-mangle --exclude-deps --spec-sources=https://github.com/CocoaPods/Specs.git,http://git.souche.com/zhangting/DFC_Specs.git,http://git.souche.com/geliang/cheniu_pod.git

cd