# initialize from the image

ARG BASE_IMAGE=trezor-core:latest
FROM ${BASE_IMAGE} AS tbuilder

RUN set -ex && \
    apt-get update && \
    apt-get --no-install-recommends --yes install \
        build-essential \
        git \
        libusb-1.0-0 \
        openssh-client \
        pkg-config \
        python3-dev \
        python3-pip \
        scons \
        wget \
    && pip3 install -U setuptools wheel \
    && pip3 install scons trezor

# GUI additions
ARG TREZOR_GUI=0
ENV TREZOR_GUI=$TREZOR_GUI
RUN set -ex && \
    if [ "${TREZOR_GUI}" -eq 1 ]; then \
            apt-get --no-install-recommends --yes install \
                libsdl2-dev \
                libsdl2-image-dev; \
    fi

# Packager cleanup, best practices
RUN set -ex && rm -rf /var/lib/apt/lists/*

FROM tbuilder AS temu0
ENV PROJECT_DIR /usr/local/src/trezor-core

WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR/
RUN set -ex && make vendor;

FROM temu0 AS temu
RUN set -ex \
    && echo "Building GUI: ${TREZOR_GUI}" \
    && if [ "${TREZOR_GUI}" -eq 1 ] ; then \
        make build_unix; \
        touch "built.gui"; \
       else \
        make build_unix_noui; \
        touch "built.nogui"; \
      fi;

EXPOSE 21324/udp
EXPOSE 21325/udp

ARG PYOPT=0
ENV PYOPT=$PYOPT
ENV TREZOR_UDP_IP=0.0.0.0

# In order to bypass entrypoint pass the folowing param
# to the docker run command: --entrypoint bash
ENTRYPOINT ["make", "emu"]

