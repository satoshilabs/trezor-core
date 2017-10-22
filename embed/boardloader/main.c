#include <string.h>

#include "common.h"
#include "display.h"
#include "image.h"
#include "flash.h"
#include "rng.h"
#include "sdcard.h"

#include "lowlevel.h"
#include "version.h"

#define BOOTLOADER_IMAGE_MAGIC   0x425A5254 // TRZB
#define BOOTLOADER_IMAGE_MAXSIZE (1 * 128 * 1024)

static uint32_t check_sdcard(void)
{
    if (!sdcard_is_present()) {
        return 0;
    }

    sdcard_power_on();

    uint64_t cap = sdcard_get_capacity_in_bytes();
    if (cap < 1024 * 1024) {
        sdcard_power_off();
        return 0;
    }

    uint32_t buf[SDCARD_BLOCK_SIZE / sizeof(uint32_t)];

    sdcard_read_blocks(buf, 0, 1);

    sdcard_power_off();

    image_header hdr;

    if (image_parse_header((const uint8_t *)buf, BOOTLOADER_IMAGE_MAGIC, BOOTLOADER_IMAGE_MAXSIZE, &hdr)) {
        return hdr.codelen;
    } else {
        return 0;
    }
}

static void progress_callback(int pos, int len) {
    display_printf(".");
}

static bool copy_sdcard(void)
{
    display_backlight(255);

    display_printf("TREZOR Boardloader\n");
    display_printf("==================\n\n");

    display_printf("bootloader found on the SD card\n\n");
    display_printf("applying bootloader in 10 seconds\n\n");
    display_printf("unplug now if you want to abort\n\n");

    uint32_t codelen;

    for (int i = 10; i >= 0; i--) {
        display_printf("%d ", i);
        hal_delay(1000);
        codelen = check_sdcard();
        if (!codelen) {
            display_printf("\n\nno SD card, aborting\n");
            return false;
        }
    }

    display_printf("\n\nerasing flash:\n\n");

    // erase all flash (except boardloader)
    uint8_t sectors[] = {
        FLASH_SECTOR_STORAGE_1,
        FLASH_SECTOR_STORAGE_2,
        FLASH_SECTOR_BOOTLOADER,
        FLASH_SECTOR_FIRMWARE_START,
        7,
        8,
        9,
        10,
        FLASH_SECTOR_FIRMWARE_END,
        FLASH_SECTOR_UNUSED_START,
        13,
        14,
        FLASH_SECTOR_UNUSED_END,
        FLASH_SECTOR_FIRMWARE_EXTRA_START,
        18,
        19,
        20,
        21,
        22,
        FLASH_SECTOR_FIRMWARE_EXTRA_END,
        FLASH_SECTOR_PIN_AREA,
    };
    if (!flash_erase_sectors(sectors, 2 + 1 + 6 + 4 + 7 + 1, progress_callback)) {
        display_printf(" failed\n");
        return false;
    }
    display_printf(" done\n\n");

    if (!flash_unlock()) {
        display_printf("could not unlock flash\n");
        return false;
    }

    // copy bootloader from SD card to Flash
    display_printf("copying new bootloader from SD card\n\n");

    sdcard_power_on();

    uint32_t buf[SDCARD_BLOCK_SIZE / sizeof(uint32_t)];
    for (int i = 0; i < (HEADER_SIZE + codelen) / SDCARD_BLOCK_SIZE; i++) {
        sdcard_read_blocks((uint8_t *)buf, i, 1);
        for (int j = 0; j < SDCARD_BLOCK_SIZE / sizeof(uint32_t); j++) {
            if (!flash_write_word(BOOTLOADER_START + i * SDCARD_BLOCK_SIZE + j * sizeof(uint32_t), buf[j])) {
                display_printf("copy failed\n");
                sdcard_power_off();
                flash_lock();
                return false;
            }
        }
    }

    sdcard_power_off();
    flash_lock();

    display_printf("\ndone\n\n");
    display_printf("Unplug the device and remove the SD card\n");

    return true;
}

const uint8_t BOARDLOADER_KEY_M = 2;
const uint8_t BOARDLOADER_KEY_N = 3;
static const uint8_t * const BOARDLOADER_KEYS[] = {
#if PRODUCTION
    (const uint8_t *)"\x0e\xb9\x85\x6b\xe9\xba\x7e\x97\x2c\x7f\x34\xea\xc1\xed\x9b\x6f\xd0\xef\xd1\x72\xec\x00\xfa\xf0\xc5\x89\x75\x9d\xa4\xdd\xfb\xa0",
    (const uint8_t *)"\xac\x8a\xb4\x0b\x32\xc9\x86\x55\x79\x8f\xd5\xda\x5e\x19\x2b\xe2\x7a\x22\x30\x6e\xa0\x5c\x6d\x27\x7c\xdf\xf4\xa3\xf4\x12\x5c\xd8",
    (const uint8_t *)"\xce\x0f\xcd\x12\x54\x3e\xf5\x93\x6c\xf2\x80\x49\x82\x13\x67\x07\x86\x3d\x17\x29\x5f\xac\xed\x72\xaf\x17\x1d\x6e\x65\x13\xff\x06",
#else
    (const uint8_t *)"\xdb\x99\x5f\xe2\x51\x69\xd1\x41\xca\xb9\xbb\xba\x92\xba\xa0\x1f\x9f\x2e\x1e\xce\x7d\xf4\xcb\x2a\xc0\x51\x90\xf3\x7f\xcc\x1f\x9d",
    (const uint8_t *)"\x21\x52\xf8\xd1\x9b\x79\x1d\x24\x45\x32\x42\xe1\x5f\x2e\xab\x6c\xb7\xcf\xfa\x7b\x6a\x5e\xd3\x00\x97\x96\x0e\x06\x98\x81\xdb\x12",
    (const uint8_t *)"\x22\xfc\x29\x77\x92\xf0\xb6\xff\xc0\xbf\xcf\xdb\x7e\xdb\x0c\x0a\xa1\x4e\x02\x5a\x36\x5e\xc0\xe3\x42\xe8\x6e\x38\x29\xcb\x74\xb6",
#endif
};

int main(void)
{
    periph_init(); // need the systick timer running before the production flash (and many other HAL) operations

    if (!reset_flags_init()) {
        return 1;
    }

#if PRODUCTION
    flash_set_option_bytes();
    if (!flash_check_option_bytes()) {
        uint8_t sectors[] = {
            FLASH_SECTOR_STORAGE_1,
            FLASH_SECTOR_STORAGE_2,
        };
        flash_erase_sectors(sectors, 2, NULL);
        return 2;
    }
#endif

    clear_otg_hs_memory();

    display_init();
    sdcard_init();

    if (check_sdcard()) {
        return copy_sdcard() ? 0 : 3;
    }

    image_header hdr;

    ensure(
        image_parse_header((const uint8_t *)BOOTLOADER_START, BOOTLOADER_IMAGE_MAGIC, BOOTLOADER_IMAGE_MAXSIZE, &hdr),
        "invalid bootloader header");

    ensure(
        image_check_signature((const uint8_t *)BOOTLOADER_START, &hdr, BOARDLOADER_KEY_M, BOARDLOADER_KEY_N, BOARDLOADER_KEYS),
        "invalid bootloader signature");

    jump_to(BOOTLOADER_START + HEADER_SIZE);

    return 0;
}
