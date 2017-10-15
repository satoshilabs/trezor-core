.PHONY: vendor

JOBS = 4
MAKE = make -j $(JOBS)
SCONS = scons -Q -j $(JOBS)

BOARDLOADER_BUILD_DIR = build/boardloader
BOOTLOADER_BUILD_DIR  = build/bootloader
FIRMWARE_BUILD_DIR    = build/firmware

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
UNIX_PORT_OPTS ?= TREZOR_X86=0
else
UNIX_PORT_OPTS ?= TREZOR_X86=1
endif
CROSS_PORT_OPTS ?= MICROPY_FORCE_32BIT=1

ifeq ($(DISPLAY_ILI9341V), 1)
CFLAGS += -DDISPLAY_ILI9341V=1
CFLAGS += -DDISPLAY_ST7789V=0
endif

PRODUCTION ?= 0

STLINK_VER ?= v2
OPENOCD = openocd -f interface/stlink-$(STLINK_VER).cfg -c "transport select hla_swd" -f target/stm32f4x.cfg

BOARDLOADER_START   = 0x08000000
BOOTLOADER_START    = 0x08020000
FIRMWARE_START      = 0x08040000

BOARDLOADER_MAXSIZE = 49152
BOOTLOADER_MAXSIZE  = 131072
FIRMWARE_MAXSIZE    = 786432

GITREV=$(shell git describe --always --dirty)
CFLAGS += -DGITREV=$(GITREV)

## help commands:

help: ## show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m  make %-20s\033[0m %s\n", $$1, $$2} /^##(.*)/ {printf "\033[33m%s\n", substr($$0, 4)}' $(MAKEFILE_LIST)

## dependencies commands:

vendor: ## update git submodules
	git submodule update --init --recursive --force

res: ## update resources
	./tools/res_collect

## emulator commands:

run: ## run unix port
	cd src ; ../build/unix/micropython

emu: ## run emulator
	./emu.sh

## test commands:

test: ## run unit tests
	cd tests ; ./run_tests.sh

testpy: ## run selected unit tests from python-trezor
	cd tests ; ./run_tests_device.sh

pylint: ## run pylint on application sources
	pylint -E $(shell find src -name *.py)

style: ## run code style check on application sources
	flake8 $(shell find src -name *.py)

## build commands:

build: build_boardloader build_bootloader build_firmware build_unix build_cross ## build all

build_boardloader: ## build boardloader
	$(SCONS) CFLAGS="$(CFLAGS)" PRODUCTION="$(PRODUCTION)" build/boardloader/boardloader.bin

build_bootloader: ## build bootloader
	$(SCONS) CFLAGS="$(CFLAGS)" PRODUCTION="$(PRODUCTION)" build/bootloader/bootloader.bin

build_firmware: res build_cross ## build firmware with frozen modules
	$(SCONS) CFLAGS="$(CFLAGS)" build/firmware/firmware.bin

build_unix: ## build unix port
	$(SCONS) CFLAGS="$(CFLAGS)" build/unix/micropython $(UNIX_PORT_OPTS)

build_unix_noui: ## build unix port without UI support
	$(SCONS) CFLAGS="$(CFLAGS)" build/unix/micropython $(UNIX_PORT_OPTS) TREZOR_NOUI=1

build_cross: ## build mpy-cross port
	$(MAKE) -C vendor/micropython/mpy-cross $(CROSS_PORT_OPTS)

## clean commands:

clean: clean_boardloader clean_bootloader clean_firmware clean_unix clean_cross ## clean all

clean_boardloader: ## clean boardloader build
	rm -rf build/boardloader

clean_bootloader: ## clean bootloader build
	rm -rf build/bootloader

clean_firmware: ## clean firmware build
	rm -rf build/firmware

clean_unix: ## clean unix build
	rm -rf build/unix

clean_cross: ## clean mpy-cross build
	$(MAKE) -C vendor/micropython/mpy-cross clean $(CROSS_PORT_OPTS)

## flash commands:

flash: flash_boardloader flash_bootloader flash_firmware ## flash everything using OpenOCD

flash_boardloader: $(BOARDLOADER_BUILD_DIR)/boardloader.bin ## flash boardloader using OpenOCD
	$(OPENOCD) -c "init; reset halt; flash write_image erase $< $(BOARDLOADER_START); exit"

flash_bootloader: $(BOOTLOADER_BUILD_DIR)/bootloader.bin ## flash bootloader using OpenOCD
	$(OPENOCD) -c "init; reset halt; flash write_image erase $< $(BOOTLOADER_START); exit"

flash_firmware: $(FIRMWARE_BUILD_DIR)/firmware.bin ## flash firmware using OpenOCD
	$(OPENOCD) -c "init; reset halt; flash write_image erase $< $(FIRMWARE_START); exit"

flash_combine: $(FIRMWARE_BUILD_DIR)/combined.bin ## flash combined using OpenOCD
	$(OPENOCD) -c "init; reset halt; flash write_image erase $< $(BOARDLOADER_START); exit"

flash_erase: ## erase all sectors in flash bank 0
	$(OPENOCD) -c "init; reset halt; flash info 0; flash erase_sector 0 0 last; flash erase_check 0; exit"

## openocd debug commands:

openocd: ## start openocd which connects to the device
	$(OPENOCD)

GDB = arm-none-eabi-gdb --nx -ex 'set remotetimeout unlimited' -ex 'set confirm off' -ex 'target remote 127.0.0.1:3333' -ex 'monitor reset halt'

gdb_boardloader: $(BOARDLOADER_BUILD_DIR)/boardloader.elf ## start remote gdb session to openocd with boardloader symbols
	$(GDB) $<

gdb_bootloader: $(BOOTLOADER_BUILD_DIR)/bootloader.elf ## start remote gdb session to openocd with bootloader symbols
	$(GDB) $<

gdb_firmware: $(FIRMWARE_BUILD_DIR)/firmware.elf ## start remote gdb session to openocd with firmware symbols
	$(GDB) $<

## misc commands:

vendorheader: ## construct default vendor header
	./tools/build_vendorheader e28a8970753332bd72fef413e6b0b2ef1b4aadda7aa2c141f233712a6876b351:d4eec1869fb1b8a4e817516ad5a931557cb56805c3eb16e8f3a803d647df7869:772c8a442b7db06e166cfbc1ccbcbcde6f3eba76a4e98ef3ffc519502237d6ef 2 0.0 10 DEVELOPMENT assets/vendor_devel.toif embed/firmware/vendorheader.bin
	./tools/binctl embed/firmware/vendorheader.bin -s 1:2 4444444444444444444444444444444444444444444444444444444444444444:4545454545454545454545454545454545454545454545454545454545454545

vendorheader_sl: ## construct SatoshiLabs vendor header
	./tools/build_vendorheader 47fbdc84d8abef44fe6abde8f87b6ead821b7082ec63b9f7cc33dc53bf6c708d:03fdd9a9c3911652d5effca4540d96ed92d85850a47d256ab0a2d728c0d1a298:2218c25f8ba70c82eba8ed6a321df209c0a7643d014f33bf9317846f62923830 2 0.0 80 SatoshiLabs assets/vendor_satoshilabs.toif embed/firmware/vendorheader_sl.bin
	./tools/binctl embed/firmware/vendorheader_sl.bin -s 1:2 trezor:trezor

binctl: ## print info about binary files
	./tools/binctl $(BOOTLOADER_BUILD_DIR)/bootloader.bin
	./tools/binctl embed/firmware/vendorheader.bin
	./tools/binctl $(FIRMWARE_BUILD_DIR)/firmware.bin

bloaty: ## run bloaty size profiler
	bloaty -d symbols -n 0 -s file $(FIRMWARE_BUILD_DIR)/firmware.elf | less
	bloaty -d compileunits -n 0 -s file $(FIRMWARE_BUILD_DIR)/firmware.elf | less

sizecheck: ## check sizes of binary files
	test $(BOARDLOADER_MAXSIZE) -ge $(shell stat -c%s $(BOARDLOADER_BUILD_DIR)/boardloader.bin)
	test $(BOOTLOADER_MAXSIZE) -ge $(shell stat -c%s $(BOOTLOADER_BUILD_DIR)/bootloader.bin)
	test $(FIRMWARE_MAXSIZE) -ge $(shell stat -c%s $(FIRMWARE_BUILD_DIR)/firmware.bin)

combine: ## combine boardloader + bootloader + firmware into one combined image
	./tools/combine_firmware \
		$(BOARDLOADER_START) $(BOARDLOADER_BUILD_DIR)/boardloader.bin \
		$(BOOTLOADER_START) $(BOOTLOADER_BUILD_DIR)/bootloader.bin \
		$(FIRMWARE_START) $(FIRMWARE_BUILD_DIR)/firmware.bin \
		> $(FIRMWARE_BUILD_DIR)/combined.bin \
