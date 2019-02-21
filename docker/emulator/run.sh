#!/bin/bash
cd "$(dirname "$0")"
cd ../..

PYOPT=${PYOPT:-0}
TREZOR_GUI=${TREZOR_GUI:-0}

if [[ "$TREZOR_GUI" -eq "1" ]]; then
    TAG="trezor-emu-gui"

    # Quartz start, permissions
    xhost + 127.0.0.1 >/dev/null

    # Get display number if not defined
    if [ -z "${DISPLAY_NUMBER}" ]; then
        OPERATING_SYSTEM=$(uname)
        if [ $OPERATING_SYSTEM == "Darwin" ]; then
            DISPLAY_NUMBER=`ps -ef | grep "Xquartz :\d" | grep -v xinit | awk '{ print $9; }'`
        else
            DISPLAY_NUMBER=`echo $DISPLAY | awk '{ n=split($0, a, ":"); print ":"a[n]; }'`
        fi
    fi

    DARGS=("--env=DISPLAY=host.docker.internal${DISPLAY_NUMBER}" \
          "--env=XAUTHORITY" \
          "--volume="$HOME/.Xauthority:/root/.Xauthority:rw"" \
          "-v /tmp/.X11-unix:/tmp/.X11-unix")

    echo "Starting Trezor-Emu docker with GUI, display number $DISPLAY_NUMBER"
else
    TAG="trezor-emu"
    DARGS=()
    echo "Starting Trezor-Emu docker"
fi

docker run -i  \
    -p 21324:21324/udp \
    -p 21325:21325/udp \
    -e PYOPT=$PYOPT \
    ${DARGS[@]} $@ \
    -t $TAG:latest
