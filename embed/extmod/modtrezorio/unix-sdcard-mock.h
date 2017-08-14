/*
 * Copyright (c) Pavol Rusnak, SatoshiLabs
 *
 * Licensed under TREZOR License
 * see LICENSE file for details
 */

#include "../../trezorhal/sdcard.h"

#define SD_ERROR 41U

int sdcard_init(void) {
    return 0;
}

bool sdcard_is_present(void) {
    return false;
}

bool sdcard_power_on(void) {
    return false;
}

bool sdcard_power_off(void) {
    return true;
}

uint64_t sdcard_get_capacity_in_bytes(void) {
    return 0;
}

uint32_t sdcard_read_blocks(void *dest, uint32_t block_num, uint32_t num_blocks) {
   return SD_ERROR;
}

uint32_t sdcard_write_blocks(const void *src, uint32_t block_num, uint32_t num_blocks) {
   return SD_ERROR;
}
