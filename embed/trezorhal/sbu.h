/*
 * This file is part of the TREZOR project, https://trezor.io/
 *
 * Copyright (c) SatoshiLabs
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __TREZORHAL_SBU_H__
#define __TREZORHAL_SBU_H__

#include <stdint.h>
#include "secbool.h"

void sbu_init(void);
void sbu_uart_on(void);
void sbu_uart_off(void);
int sbu_read(uint8_t *data, uint16_t len, uint32_t timeout);
void sbu_write(const uint8_t *data, uint16_t len, uint32_t timeout);
void sbu_set_pins(secbool sbu1, secbool sbu2);

#endif
