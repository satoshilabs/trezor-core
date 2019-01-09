# initialize from the image

FROM debian:9

ARG TOOLCHAIN_FLAVOR=linux
ENV TOOLCHAIN_FLAVOR=$TOOLCHAIN_FLAVOR

# install build tools and dependencies

RUN apt-get update && apt-get install -y \
    build-essential wget git python3-pip gcc-multilib

# install dependencies from toolchain source build

RUN if [ "$TOOLCHAIN_FLAVOR" = "src" ]; then \
        apt-get install -y autoconf autogen bison dejagnu \
                           flex flip gawk git gperf gzip nsis \
                           openssh-client p7zip-full perl python-dev \
                           libisl-dev tcl tofrodos zip \
                           texinfo texlive texlive-extra-utils; \
    fi

# download toolchain

ENV TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2018q4/gcc-arm-none-eabi-8-2018-q4-major-$TOOLCHAIN_FLAVOR.tar.bz2
ENV TOOLCHAIN_SHA256SUM=fb31fbdfe08406ece43eef5df623c0b2deb8b53e405e2c878300f7a1f303ee52

# extract toolchain

RUN cd /opt && wget -O gcc.tar.bz2 $TOOLCHAIN_URL && echo "${TOOLCHAIN_SHA256SUM} gcc.tar.bz2" | sha256sum -c && tar xfj gcc.tar.bz2

# build toolchain (if required)

RUN if [ "$TOOLCHAIN_FLAVOR" = "src" ]; then \
        pushd /opt/$TOOLCHAIN_LONGVER ; \
        ./install-sources.sh --skip_steps=mingw32 ; \
        ./build-prerequisites.sh --skip_steps=mingw32 ; \
        ./build-toolchain.sh --skip_steps=mingw32,manual ; \
        popd ; \
    fi

# install additional tools

RUN apt-get install -y protobuf-compiler libprotobuf-dev

# setup toolchain

ENV PATH=/opt/$TOOLCHAIN_LONGVER/bin:$PATH

# install python dependencies

RUN pip3 install scons trezor

# workarounds for weird default install

RUN ln -s python3 /usr/bin/python
RUN ln -s dist-packages /usr/local/lib/python3.5/site-packages
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
