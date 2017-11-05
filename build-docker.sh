#!/bin/bash
set -e

IMAGE=trezor-core-build
TAG=${1:-master}

docker build -t $IMAGE .
docker run -t -v $(pwd)/build-docker:/build:z $IMAGE /bin/sh -c "\
	git clone https://github.com/trezor/trezor-core && \
	cd trezor-core && \
	ln -s /build build &&
	git checkout $TAG && \
	git submodule update --init --recursive && \
	make clean vendor vendorheader build_boardloader build_bootloader build_prodtest build_firmware"
