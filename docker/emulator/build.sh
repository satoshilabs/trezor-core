#!/bin/bash
cd "$(dirname "$0")"
cd ../..

TREZOR_GUI=${TREZOR_GUI:-0}
BASE_IMAGE=${BASE_IMAGE:-}
WITH_TOOLCHAIN=${WITH_TOOLCHAIN:-0}
[[ "$TREZOR_GUI" -eq "1" ]] && TAG="trezor-emu-gui" || TAG="trezor-emu"

echo "Trezor emulator image build, GUI support: $TREZOR_GUI, image name: $TAG"

# Root image build if toolchain is required
# Toolchain adds support for building hardware firmware
if [ "${WITH_TOOLCHAIN}" -eq 1 ]; then
    echo "Building base Trezor-core image"

    BASE_IMAGE_ARG=""
    if [ -n "$BASE_IMAGE" ]; then
        BASE_IMAGE_ARG="--build-arg BASE_IMAGE=${BASE_IMAGE}"
    fi

    docker build $BASE_IMAGE_ARG -t="trezor-core" .
    BASE_IMAGE="trezor-core:latest"

else
    BASE_IMAGE=${BASE_IMAGE:-debian:9}

fi

# emu image build
echo "Building Trezor-core emulator image"
docker build -f docker/emulator/Dockerfile --build-arg BASE_IMAGE=$BASE_IMAGE --build-arg TREZOR_GUI=$TREZOR_GUI -t="$TAG" $@ .

echo "Docker image $TAG built"
