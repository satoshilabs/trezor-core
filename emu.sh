#!/bin/bash

source emu.config 2>/dev/null

EXE=build/unix/micropython
OPTLEVEL="${OPTLEVEL:-1}"
MAIN="${MAIN:-main.py}"
BROWSER="${BROWSER:-chromium}"
if file $EXE | grep -q 80386 ; then
HEAPSIZE="${HEAPSIZE:-163K}"
else
HEAPSIZE="${HEAPSIZE:-400K}"
fi

ARGS="-O${OPTLEVEL} -X heapsize=${HEAPSIZE}"

cd `dirname $0`/src

case "$1" in
    "-d")
        shift
        gdb --args ../$EXE $ARGS $* $MAIN
        ;;
    "-r")
        shift
        while true; do
            ../$EXE $ARGS $* $MAIN &
            UPY_PID=$!
            find -name '*.py' | inotifywait -q -e close_write --fromfile -
            echo Restarting ...
            kill $UPY_PID
        done
        ;;
    "-p")
        shift
        ../$EXE $ARGS $* $MAIN &
        perf record -F 100 -p $! -g -- sleep 600
        perf script > perf.trace
        ../vendor/flamegraph/stackcollapse-perf.pl perf.trace | ../vendor/flamegraph/flamegraph.pl > perf.svg
        $BROWSER perf.svg
        ;;
    *)
        ../$EXE $ARGS $* $MAIN
esac
