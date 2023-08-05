#!/bin/bash -x

MY_DIR=$(readlink -f $(dirname $0))
CONFIG_DIR_SUFFIX=$1

if [[ "$CONFIG_DIR_SUFFIX" != "master" && "$CONFIG_DIR_SUFFIX" != "worker" ]]; then
   echo "Usage: launcher-wrapper <master|worker> <launcher args>"
   exit 1
fi

rm -f $MY_DIR/../etc
ln -s $MY_DIR/../etc-$CONFIG_DIR_SUFFIX $MY_DIR/../etc
shift 1
$MY_DIR/launcher $*
