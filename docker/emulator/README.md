## Trezor-core Emulator in Docker

You can run Trezor-core emulator with Docker:

```bash
git clone --recursive https://github.com/trezor/trezor-core.git
cd trezor-core

./docker/emulator/build.sh  # builds docker image (needed only once)
./docker/emulator/run.sh    # runs docker image
```

This gives you simple emulator without GUI, exposing emulator UDP ports to the host so you can connect to it.
The emulator shoult be listed by:

```bash
trezorctl list
```


### GUI support

Alternativelly, you can build image with GUI support which requires X server. For OSX you can use [XQuartz](https://www.xquartz.org/).

```bash
TREZOR_GUI=1 ./docker/emulator/build.sh  # need to build GUI image
TREZOR_GUI=1 ./docker/emulator/run.sh    # run with GUI (configures display)
```


### Base image

Aforementioned images are built on top of Debian 9 image. If you rather prefer Ubuntu, change `BASE_IMAGE`:

```bash
BASE_IMAGE=ubuntu:18.04 ./docker/emulator/build.sh
```


### With toolchain

The images are built on the base image without toolchain for compiling firmware to the Trezor hardware architecture.
If you prefer to build emulator image with the toolchain:

```bash
WITH_TOOLCHAIN=1 ./docker/emulator/build.sh
```

Toolchain image is again based on Debian 9. This can be changed by setting `BASE_IMAGE` appropriately.


### PYOPT

Emulator runs by default with `PYOPT=0`, the debugging mode. This can be changed by:

```bash
PYOPT=1 ./docker/emulator/run.sh
```


### Bypassing entrypoint

Trezor images run emulator directly. In order to bypass this and get the shell of the emulator container use:

```bash
./docker/emulator/run.sh --entrypoint bash
```
