#include STM32_HAL_H

#include <string.h>

#include "crypto.h"

#include "common.h"
#include "display.h"
#include "sdcard.h"

#define BOOTLOADER_FGCOLOR 0xFFFF
#define BOOTLOADER_BGCOLOR 0x0000

#define BOOTLOADER_PRINT(X)   do { display_print(X, -1);      display_print_out(BOOTLOADER_FGCOLOR, BOOTLOADER_BGCOLOR); } while(0)
#define BOOTLOADER_PRINTLN(X) do { display_print(X "\n", -1); display_print_out(BOOTLOADER_FGCOLOR, BOOTLOADER_BGCOLOR); } while(0)

void pendsv_isr_handler(void) {
    __fatal_error("pendsv");
}

bool check_sdcard(void)
{
    BOOTLOADER_PRINTLN("checking for SD card");

    if (!sdcard_is_present()) {
        BOOTLOADER_PRINTLN("no SD card found");
        return false;
    }

    BOOTLOADER_PRINTLN("SD card found");

    sdcard_power_on();

    uint64_t cap = sdcard_get_capacity_in_bytes();
    if (cap < 1024 * 1024) {
        BOOTLOADER_PRINTLN("SD card too small");
        sdcard_power_off();
        return false;
    }

    uint8_t buf[SDCARD_BLOCK_SIZE] __attribute__((aligned(4)));

    sdcard_read_blocks(buf, 0, 1);

    sdcard_power_off();

    if (parse_header(buf, NULL, NULL, NULL)) {
        BOOTLOADER_PRINTLN("SD card header is valid");
        return true;
    } else {
        BOOTLOADER_PRINTLN("SD card header is invalid");
        return false;
    }
}

bool copy_sdcard(void)
{

    BOOTLOADER_PRINT("erasing flash ");

    // erase flash (except bootloader)
    HAL_FLASH_Unlock();
    FLASH_EraseInitTypeDef EraseInitStruct;
    __HAL_FLASH_CLEAR_FLAG(FLASH_FLAG_EOP | FLASH_FLAG_OPERR | FLASH_FLAG_WRPERR |
                           FLASH_FLAG_PGAERR | FLASH_FLAG_PGPERR | FLASH_FLAG_PGSERR);
    EraseInitStruct.TypeErase = TYPEERASE_SECTORS;
    EraseInitStruct.VoltageRange = VOLTAGE_RANGE_3; // voltage range needs to be 2.7V to 3.6V
    EraseInitStruct.NbSectors = 1;
    uint32_t SectorError = 0;
    for (int i = 2; i < 12; i++) {
        EraseInitStruct.Sector = i;
        if (HAL_FLASHEx_Erase(&EraseInitStruct, &SectorError) != HAL_OK) {
            HAL_FLASH_Lock();
            BOOTLOADER_PRINTLN(" failed");
            return false;
        }
        BOOTLOADER_PRINT(".");
    }
    BOOTLOADER_PRINTLN(" done");

    BOOTLOADER_PRINTLN("copying new loader from SD card");

    sdcard_power_on();

    // copy loader from SD card to Flash
    uint32_t buf[SDCARD_BLOCK_SIZE / sizeof(uint32_t)];
    sdcard_read_blocks((uint8_t *)buf, 0, 1);

    uint32_t codelen;
    if (!parse_header((uint8_t *)buf, &codelen, NULL, NULL)) {
        BOOTLOADER_PRINTLN("wrong header");
        return false;
    }

    for (int i = 0; i < codelen / SDCARD_BLOCK_SIZE; i++) {
        sdcard_read_blocks((uint8_t *)buf, i, 1);
        for (int j = 0; j < SDCARD_BLOCK_SIZE / sizeof(uint32_t); j++) {
            if (HAL_FLASH_Program(TYPEPROGRAM_WORD, LOADER_START + i * SDCARD_BLOCK_SIZE + j * sizeof(uint32_t), buf[j]) != HAL_OK) {
                BOOTLOADER_PRINTLN("copy failed");
                sdcard_power_off();
                HAL_FLASH_Lock();
                return false;
            }
        }
    }

    sdcard_power_off();
    HAL_FLASH_Lock();

    BOOTLOADER_PRINTLN("done");

    return true;
}

int main(void)
{
    SCB->VTOR = BOOTLOADER_START;
    periph_init();

    sdcard_init();

    display_init();
    display_clear();
    display_backlight(255);

    BOOTLOADER_PRINTLN("TREZOR Bootloader");
    BOOTLOADER_PRINTLN("=================");
    BOOTLOADER_PRINTLN("starting bootloader");

    // TODO: remove debug
    BOOTLOADER_PRINTLN("waiting 1 second");
    HAL_Delay(1000);
    BOOTLOADER_PRINTLN("jumping to loader");
    jump_to(LOADER_START + HEADER_SIZE);
    // end

    if (check_sdcard()) {
        if (!copy_sdcard()) {
            __fatal_error("halt");
        }
    }

    BOOTLOADER_PRINTLN("checking loader");
    if (parse_header((const uint8_t *)LOADER_START, NULL, NULL, NULL)) {
        BOOTLOADER_PRINTLN("valid loader header");
        if (check_signature((const uint8_t *)LOADER_START)) {
            BOOTLOADER_PRINTLN("valid loader signature");
            BOOTLOADER_PRINTLN("JUMP!");
            jump_to(LOADER_START + HEADER_SIZE);
        } else {
            BOOTLOADER_PRINTLN("invalid loader signature");
        }
    } else {
        BOOTLOADER_PRINTLN("invalid loader header");
    }

    __fatal_error("halt");

    return 0;
}
