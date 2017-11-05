# initialize from the image

FROM debian:9

# install build tools and dependencies

RUN apt-get update && apt-get install -y \
    build-essential wget git python3-pip \
    gcc-multilib

# download and setup toolchain

ENV TOOLCHAIN_SHORTVER=6-2017q2
ENV TOOLCHAIN_LONGVER=gcc-arm-none-eabi-6-2017-q2-update
RUN cd /opt && wget https://developer.arm.com/-/media/Files/downloads/gnu-rm/$TOOLCHAIN_SHORTVER/$TOOLCHAIN_LONGVER-linux.tar.bz2 && tar xfj $TOOLCHAIN_LONGVER-linux.tar.bz2
ENV PATH=/opt/$TOOLCHAIN_LONGVER/bin:$PATH

# install python tools

RUN pip3 install click pyblake2 scons
RUN pip3 install --no-deps git+https://github.com/trezor/python-trezor.git@master

# workarounds for weird default install

RUN ln -s python3 /usr/bin/python
ENV SCONS_LIB_DIR=/usr/local/lib/python3.5/dist-packages/scons-3.0.0
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
