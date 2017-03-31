#ifndef __TREZORHAL_COMMON_H__
#define __TREZORHAL_COMMON_H__

#include <stdint.h>

#define BOOTLOADER_START  0x08000000
#define LOADER_START      0x08010000
#define FIRMWARE_START    0x08020000
#define HEADER_SIZE       0x200

void periph_init(void);

void __attribute__((noreturn)) nlr_jump_fail(void *val);

void __attribute__((noreturn)) __fatal_error(const char *msg);

void jump_to(uint32_t address);

#endif
