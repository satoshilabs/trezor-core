#include STM32_HAL_H

#include <string.h>
#include "flash.h"

// see docs/memory.md for more information

#define SECTOR_COUNT 24

static const uint32_t SECTOR_TABLE[SECTOR_COUNT + 1] = {
    [ 0] = 0x08000000, // - 0x08003FFF |  16 KiB
    [ 1] = 0x08004000, // - 0x08007FFF |  16 KiB
    [ 2] = 0x08008000, // - 0x0800BFFF |  16 KiB
    [ 3] = 0x0800C000, // - 0x0800FFFF |  16 KiB
    [ 4] = 0x08010000, // - 0x0801FFFF |  64 KiB
    [ 5] = 0x08020000, // - 0x0803FFFF | 128 KiB
    [ 6] = 0x08040000, // - 0x0805FFFF | 128 KiB
    [ 7] = 0x08060000, // - 0x0807FFFF | 128 KiB
    [ 8] = 0x08080000, // - 0x0809FFFF | 128 KiB
    [ 9] = 0x080A0000, // - 0x080BFFFF | 128 KiB
    [10] = 0x080C0000, // - 0x080DFFFF | 128 KiB
    [11] = 0x080E0000, // - 0x080FFFFF | 128 KiB
    [12] = 0x08100000, // - 0x08103FFF |  16 KiB
    [13] = 0x08104000, // - 0x08107FFF |  16 KiB
    [14] = 0x08108000, // - 0x0810BFFF |  16 KiB
    [15] = 0x0810C000, // - 0x0810FFFF |  16 KiB
    [16] = 0x08110000, // - 0x0811FFFF |  64 KiB
    [17] = 0x08120000, // - 0x0813FFFF | 128 KiB
    [18] = 0x08140000, // - 0x0815FFFF | 128 KiB
    [19] = 0x08160000, // - 0x0817FFFF | 128 KiB
    [20] = 0x08180000, // - 0x0819FFFF | 128 KiB
    [21] = 0x081A0000, // - 0x081BFFFF | 128 KiB
    [22] = 0x081C0000, // - 0x081DFFFF | 128 KiB
    [23] = 0x081E0000, // - 0x081FFFFF | 128 KiB
    [24] = 0x08200000, // last element - not a valid sector
};

bool flash_unlock(void)
{
    HAL_FLASH_Unlock();
    __HAL_FLASH_CLEAR_FLAG(FLASH_FLAG_EOP | FLASH_FLAG_OPERR | FLASH_FLAG_WRPERR | FLASH_FLAG_PGAERR | FLASH_FLAG_PGPERR | FLASH_FLAG_PGSERR);
    return true;
}

bool flash_lock(void)
{
    HAL_FLASH_Lock();
    return true;
}

bool flash_erase_sectors(const uint8_t *sectors, int len, void (*progress)(int pos, int len))
{
    if (!flash_unlock()) {
        return false;
    }
    FLASH_EraseInitTypeDef EraseInitStruct;
    EraseInitStruct.TypeErase = FLASH_TYPEERASE_SECTORS;
    EraseInitStruct.VoltageRange = FLASH_VOLTAGE_RANGE_3;
    EraseInitStruct.NbSectors = 1;
    uint32_t SectorError = 0;
    if (progress) {
        progress(0, len);
    }
    for (int i = 0; i < len; i++) {
        EraseInitStruct.Sector = sectors[i];
        if (HAL_FLASHEx_Erase(&EraseInitStruct, &SectorError) != HAL_OK) {
            flash_lock();
            return false;
        }
        // check whether the sector was really deleted (contains only 0xFF)
        uint32_t addr_start = SECTOR_TABLE[sectors[i]], addr_end = SECTOR_TABLE[sectors[i] + 1];
        for (uint32_t addr = addr_start; addr < addr_end; addr += 4) {
            if (*((const uint32_t *)addr) != 0xFFFFFFFF) {
                return false;
            }
        }
        if (progress) {
            progress(i + 1, len);
        }
    }
    flash_lock();
    return true;
}

bool flash_write_byte(uint32_t address, uint8_t data)
{
    return HAL_OK == HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, address, data);
}

bool flash_write_word(uint32_t address, uint32_t data)
{
    return HAL_OK == HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address, data);
}

#define FLASH_OTP_LOCK_BASE       0x1FFF7A00U

bool flash_otp_read(uint8_t block, uint8_t offset, uint8_t *data, uint8_t datalen)
{
    if (block >= FLASH_OTP_NUM_BLOCKS || offset + datalen > FLASH_OTP_BLOCK_SIZE) {
        return false;
    }
    for (uint8_t i = 0; i < datalen; i++) {
        data[i] = *(__IO uint8_t *)(FLASH_OTP_BASE + block * FLASH_OTP_BLOCK_SIZE + offset + i);
    }
    return true;
}

bool flash_otp_write(uint8_t block, uint8_t offset, const uint8_t *data, uint8_t datalen)
{
    if (block >= FLASH_OTP_NUM_BLOCKS || offset + datalen > FLASH_OTP_BLOCK_SIZE) {
        return false;
    }
    if (!flash_unlock()) {
        return false;
    }
    bool ret = false;
    for (uint8_t i = 0; i < datalen; i++) {
        ret = flash_write_byte(FLASH_OTP_BASE + block * FLASH_OTP_BLOCK_SIZE + offset + i, data[i]);
        if (!ret) {
            break;
        }
    }
    flash_lock();
    return ret;
}

bool flash_otp_lock(uint8_t block)
{
    if (block >= FLASH_OTP_NUM_BLOCKS) {
        return false;
    }
    if (!flash_unlock()) {
        return false;
    }
    HAL_StatusTypeDef ret = HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, FLASH_OTP_LOCK_BASE + block, 0x00);
    flash_lock();
    return ret == HAL_OK;
}

bool flash_otp_is_locked(uint8_t block)
{
    return *(__IO uint8_t *)(FLASH_OTP_LOCK_BASE + block) == 0x00;
}
