#!/bin/bash

source emu.config 2>/dev/null

EXE=build/unix/micropython
PYOPT="${PYOPT:-1}"
MAIN="${MAIN:-${PWD}/src/main.py}"
BROWSER="${BROWSER:-chromium}"
HEAPSIZE="${HEAPSIZE:-50M}"
SOURCE_PY_DIR="${SOURCE_PY_DIR:-src}"

ARGS="-O${PYOPT} -X heapsize=${HEAPSIZE}"

OPERATING_SYSTEM=$(uname)

LIB_OVERRIDE_PATH="${PWD}/tools/hotpatch/lib_overrides.so"
ENV_LIB_OVERRIDE="LD_PRELOAD=${LIB_OVERRIDE_PATH}"
if [ $OPERATING_SYSTEM == "Darwin" ]; then
    ENV_LIB_OVERRIDE="DYLD_INSERT_LIBRARIES=${LIB_OVERRIDE_PATH}"
fi

cd `dirname $0`/$SOURCE_PY_DIR

case "$1" in
    # persist the flash memory upon exit so you don't need to reinitalize the device every run
    "--persist")
        shift
        DYLD_FORCE_FLAT_NAMESPACE=1 DYLD_INSERT_LIBRARIES=${LIB_OVERRIDE_PATH} ../$EXE $ARGS $* $MAIN
        ;;
    "--persist-lldb")
        shift
        LLDB_SET_ENV="settings set target.env-vars ${ENV_LIB_OVERRIDE}"
        PATH=/usr/bin /usr/bin/lldb -s <(echo "${LLDB_SET_ENV}") -f ../$EXE -- $ARGS $* $MAIN
        ;;
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
