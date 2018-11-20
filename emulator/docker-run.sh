#!/bin/bash
docker run -p 127.0.0.1:21324:21324/udp -p 21325:21325 -d trezor-emulator:latest