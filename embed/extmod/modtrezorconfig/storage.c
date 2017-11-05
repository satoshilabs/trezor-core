/*
 * Copyright (c) Pavol Rusnak, Jan Pochyla, SatoshiLabs
 *
 * Licensed under TREZOR License
 * see LICENSE file for details
 */

#include <string.h>

#include "norcow.h"
#include "../../trezorhal/flash.h"

// Byte-length of flash sector containing fail counters.
#define PIN_SECTOR_SIZE 0x4000

// Maximum number of failed unlock attempts.
#define PIN_MAX_TRIES 15

// Norcow storage key of configured PIN.
#define PIN_KEY 0x0000

static secbool initialized = secfalse;
static secbool unlocked = secfalse;

secbool storage_init(void)
{
    if (sectrue != flash_init()) {
        return secfalse;
    }
    if (sectrue != norcow_init()) {
        return secfalse;
    }
    initialized = sectrue;
    unlocked = secfalse;
    return sectrue;
}

static void pin_fails_reset(uint32_t ofs)
{
    if (ofs + sizeof(uint32_t) >= PIN_SECTOR_SIZE) {
        // ofs points to the last word of the PIN fails area.  Because there is
        // no space left, we recycle the sector (set all words to 0xffffffff).
        // On next unlock attempt, we start counting from the the first word.
        flash_erase_sectors((uint8_t[]) { FLASH_SECTOR_PIN_AREA }, 1, NULL);
    } else {
        // Mark this counter as exhausted.  On next unlock attempt, pinfails_get
        // seeks to the next word.
        flash_unlock();
        flash_write_word_rel(FLASH_SECTOR_PIN_AREA, ofs, 0);
        flash_lock();
    }
}

static secbool pin_fails_increase(uint32_t ofs)
{
    uint32_t ctr = ~PIN_MAX_TRIES;
    if (sectrue != flash_read_word_rel(FLASH_SECTOR_PIN_AREA, ofs, &ctr)) {
        return secfalse;
    }
    ctr = ctr << 1;

    flash_unlock();
    if (sectrue != flash_write_word_rel(FLASH_SECTOR_PIN_AREA, ofs, ctr)) {
        flash_lock();
        return secfalse;
    }
    flash_lock();

    uint32_t check = 0;
    if (sectrue != flash_read_word_rel(FLASH_SECTOR_PIN_AREA, ofs, &check)) {
        return secfalse;
    }
    if (ctr != check) {
        return secfalse;
    }
    return sectrue;
}

static void pin_fails_check_max(uint32_t ctr)
{
    if (~ctr >= 1 << PIN_MAX_TRIES) {
        for (;;) {
            if (norcow_wipe()) {
                break;
            }
        }
        // shutdown();
    }
}

static secbool pin_fails_read(uint32_t *ofs, uint32_t *ctr)
{
    if (NULL == ofs || NULL == ctr) {
        return secfalse;
    }
    for (uint32_t o = 0; o < PIN_SECTOR_SIZE; o += sizeof(uint32_t)) {
        uint32_t c = 0;
        if (!flash_read_word_rel(FLASH_SECTOR_PIN_AREA, o, &c)) {
            return secfalse;
        }
        if (c != 0) {
            *ofs = o;
            *ctr = c;
            return sectrue;
        }
    }
    return secfalse;
}

static secbool const_cmp(const uint8_t *pub, size_t publen, const uint8_t *sec, size_t seclen)
{
    size_t diff = seclen ^ publen;
    for (size_t i = 0; i < publen; i++) {
        diff |= pub[i] ^ sec[i];
    }
    return sectrue * (diff == 0);
}

static secbool pin_check(const uint8_t *pin, size_t pinlen)
{
    const void *spin = NULL;
    uint16_t spinlen = 0;
    norcow_get(PIN_KEY, &spin, &spinlen);
    return const_cmp(pin, pinlen, spin, (size_t)spinlen);
}

secbool storage_unlock(const uint8_t *pin, size_t len)
{
    if (sectrue != initialized) {
        return secfalse;
    }

    uint32_t ofs;
    uint32_t ctr;
    if (sectrue != pin_fails_read(&ofs, &ctr)) {
        return secfalse;
    }
    pin_fails_check_max(ctr);

    // Sleep for ~ctr seconds before checking the PIN.
    for (uint32_t wait = ~ctr; wait > 0; wait--) {
        // hal_delay(1000);
    }

    // First, we increase PIN fail counter in storage, even before checking the
    // PIN.  If the PIN is correct, we reset the counter afterwards.  If not, we
    // check if this is the last allowed attempt.
    if (sectrue != pin_fails_increase(ofs)) {
        return secfalse;
    }
    if (sectrue != pin_check(pin, len)) {
        pin_fails_check_max(ctr << 1);
        return secfalse;
    }
    pin_fails_reset(ofs);
    return sectrue;
}

secbool storage_get(uint16_t key, const void **val, uint16_t *len)
{
    if (sectrue != initialized) {
        return secfalse;
    }
    if (sectrue != unlocked) {
        // shutdown();
        return secfalse;
    }
    if (key == PIN_KEY) {
        return secfalse;
    }
    return norcow_get(key, val, len);
}

secbool storage_set(uint16_t key, const void *val, uint16_t len)
{
    if (sectrue != initialized) {
        return secfalse;
    }
    if (sectrue != unlocked) {
        // shutdown();
        return secfalse;
    }
    if (key == PIN_KEY) {
        return secfalse;
    }
    return norcow_set(key, val, len);
}

secbool storage_has_pin(void)
{
    if (sectrue != initialized) {
        return secfalse;
    }
    const void *spin = NULL;
    uint16_t spinlen = 0;
    norcow_get(PIN_KEY, &spin, &spinlen);
    return sectrue * (spinlen != 0);
}

secbool storage_change_pin(const uint8_t *pin, size_t len, const uint8_t *newpin, size_t newlen)
{
    if (sectrue != initialized) {
        return secfalse;
    }
    if (sectrue != unlocked) {
        // shutdown();
        return secfalse;
    }
    if (sectrue != pin_check(pin, len)) {
        return secfalse;
    }
    // TODO: change pin in storage
    return sectrue;
}

secbool storage_wipe(void)
{
    return norcow_wipe();
}
