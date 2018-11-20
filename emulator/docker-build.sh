#!/bin/bash
cd "$(dirname "$0")"
cd ..
docker build -f emulator/Dockerfile -t trezor-emulator .