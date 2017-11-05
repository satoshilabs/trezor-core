#include <string.h>

#include "norcow.h"

#include "../../trezorhal/flash.h"

#ifndef NORCOW_SECTORS
#define NORCOW_SECTORS {4, 16}
#endif

static uint8_t norcow_sectors[NORCOW_SECTOR_COUNT] = NORCOW_SECTORS;
static uint8_t norcow_active_sector = 0;
static uint32_t norcow_active_offset = 0;

/*
 * Erases sector
 */
static secbool norcow_erase(uint8_t sector)
{
    if (sector >= NORCOW_SECTOR_COUNT) {
        return secfalse;
    }
    return flash_erase_sectors(&norcow_sectors[sector], 1, NULL);
}

/*
 * Returns pointer to sector, starting with offset
 * Fails when there is not enough space for data of given size
 */
static const void *norcow_ptr(uint8_t sector, uint32_t offset, uint32_t size)
{
    if (sector >= NORCOW_SECTOR_COUNT) {
        return NULL;
    }
    return flash_get_address(norcow_sectors[sector], offset, size);
}

/*
 * Writes data to given sector, starting from offset
 */
static secbool norcow_write(uint8_t sector, uint32_t offset, uint32_t prefix, const uint8_t *data, uint16_t len)
{
    if (sector >= NORCOW_SECTOR_COUNT) {
        return secfalse;
    }
    if (sectrue != flash_unlock()) {
        return secfalse;
    }
    // write prefix
    if (sectrue != flash_write_word_rel(norcow_sectors[sector], offset, prefix)) {
        flash_lock();
        return secfalse;
    }
    offset += sizeof(uint32_t);
    // write data
    for (uint16_t i = 0; i < len; i++, offset++) {
        if (sectrue != flash_write_byte_rel(norcow_sectors[sector], offset, data[i])) {
            flash_lock();
            return secfalse;
        }
    }
    // pad with zeroes
    for (; offset % 4; offset++) {
        if (sectrue != flash_write_byte_rel(norcow_sectors[sector], offset, 0x00)) {
            flash_lock();
            return secfalse;
        }
    }
    flash_lock();
    return sectrue;
}

#define ALIGN4(X) (X) = ((X) + 3) & ~3

/*
 * Reads one item starting from offset
 */
static secbool read_item(uint8_t sector, uint32_t offset, uint16_t *key, const void **val, uint16_t *len, uint32_t *pos)
{
    *pos = offset;

    const void *k = norcow_ptr(sector, *pos, 2);
    if (k == NULL) return secfalse;
    *pos += 2;
    memcpy(key, k, sizeof(uint16_t));
    if (*key == 0xFFFF) {
        return secfalse;
    }

    const void *l = norcow_ptr(sector, *pos, 2);
    if (l == NULL) return secfalse;
    *pos += 2;
    memcpy(len, l, sizeof(uint16_t));

    *val = norcow_ptr(sector, *pos, *len);
    if (*val == NULL) return secfalse;
    *pos += *len;
    ALIGN4(*pos);
    return sectrue;
}

/*
 * Writes one item starting from offset
 */
static secbool write_item(uint8_t sector, uint32_t offset, uint16_t key, const void *val, uint16_t len, uint32_t *pos)
{
    uint32_t prefix = (len << 16) | key;
    *pos = offset + sizeof(uint32_t) + len;
    ALIGN4(*pos);
    return norcow_write(sector, offset, prefix, val, len);
}

/*
 * Finds item in given sector
 */
static secbool find_item(uint8_t sector, uint16_t key, const void **val, uint16_t *len)
{
    *val = 0;
    *len = 0;
    uint32_t offset = 0;
    for (;;) {
        uint16_t k, l;
        const void *v;
        uint32_t pos;
        if (sectrue != read_item(sector, offset, &k, &v, &l, &pos)) {
            break;
        }
        if (key == k) {
            *val = v;
            *len = l;
        }
        offset = pos;
    }
    return sectrue * (*val != NULL);
}

/*
 * Finds first unused offset in given sector
 */
static uint32_t find_free_offset(uint8_t sector)
{
    uint32_t offset = 0;
    for (;;) {
        uint16_t key, len;
        const void *val;
        uint32_t pos;
        if (sectrue != read_item(sector, offset, &key, &val, &len, &pos)) {
            break;
        }
        offset = pos;
    }
    return offset;
}

/*
 * Compacts active sector and sets new active sector
 */
static void compact()
{
    uint8_t norcow_next_sector = (norcow_active_sector + 1) % NORCOW_SECTOR_COUNT;

    uint32_t offset = 0, offsetw = 0;

    for (;;) {
        // read item
        uint16_t k, l;
        const void *v;
        uint32_t pos;
        secbool r = read_item(norcow_active_sector, offset, &k, &v, &l, &pos);
        if (sectrue != r) break;
        offset = pos;

        // check if not already saved
        const void *v2;
        uint16_t l2;
        r = find_item(norcow_next_sector, k, &v2, &l2);
        if (sectrue == r) continue;

        // scan for latest instance
        uint32_t offsetr = offset;
        for (;;) {
            uint16_t k2;
            uint32_t posr;
            r = read_item(norcow_active_sector, offsetr, &k2, &v2, &l2, &posr);
            if (sectrue != r) break;
            if (k == k2) {
                v = v2;
                l = l2;
            }
            offsetr = posr;
        }

        // copy the last item
        uint32_t posw;
        r = write_item(norcow_next_sector, offsetw, k, v, l, &posw);
        if (sectrue != r) { } // TODO: error
        offsetw = posw;
    }

    norcow_erase(norcow_active_sector);
    norcow_active_sector = norcow_next_sector;
    norcow_active_offset = find_free_offset(norcow_active_sector);
}

/*
 * Initializes storage
 */
secbool norcow_init(void)
{
    // detect active sector (inactive sectors are empty = start with 0xFF)
    for (uint8_t i = 0; i < NORCOW_SECTOR_COUNT; i++) {
        const uint8_t *b = norcow_ptr(i, 0, 1);
        if (b != NULL && *b != 0xFF) {
            norcow_active_sector = i;
            break;
        }
    }
    norcow_active_offset = find_free_offset(norcow_active_sector);
    return sectrue;
}

/*
 * Wipe the storage
 */
secbool norcow_wipe(void)
{
    for (uint8_t i = 0; i < NORCOW_SECTOR_COUNT; i++) {
        if (sectrue != norcow_erase(i)) {
            return secfalse;
        }
    }
    norcow_active_sector = 0;
    norcow_active_offset = 0;
    return sectrue;
}

/*
 * Looks for the given key, returns status of the operation
 */
secbool norcow_get(uint16_t key, const void **val, uint16_t *len)
{
    return find_item(norcow_active_sector, key, val, len);
}

/*
 * Sets the given key, returns status of the operation
 */
secbool norcow_set(uint16_t key, const void *val, uint16_t len)
{
    // check whether there is enough free space
    // and compact if full
    if (norcow_active_offset + sizeof(uint32_t) + len > NORCOW_SECTOR_SIZE) {
        compact();
    }
    // write item
    uint32_t pos;
    secbool r = write_item(norcow_active_sector, norcow_active_offset, key, val, len, &pos);
    if (sectrue == r) {
        norcow_active_offset = pos;
    }
    return r;
}
