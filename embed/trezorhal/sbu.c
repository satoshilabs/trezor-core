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

#include STM32_HAL_H

#include "common.h"
#include "sbu.h"

static USART_HandleTypeDef usart_handle;

static inline void sbu_default_pin_state(void) {
    // SBU1/PA2 SBU2/PA3
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_RESET);

    // set above pins to OUTPUT / NOPULL
    GPIO_InitTypeDef GPIO_InitStructure;

    GPIO_InitStructure.Pin = GPIO_PIN_2 | GPIO_PIN_3;
    GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStructure);
}

static inline void sbu_active_pin_state(void) {
    // set above pins to OUTPUT / NOPULL
    GPIO_InitTypeDef GPIO_InitStructure;

    GPIO_InitStructure.Pin = GPIO_PIN_2;
    GPIO_InitStructure.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStructure.Alternate = GPIO_AF7_USART2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStructure);

    GPIO_InitStructure.Pin = GPIO_PIN_2;
    GPIO_InitStructure.Mode = GPIO_MODE_AF_OD;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStructure);
}

void sbu_init(void) {
    sbu_default_pin_state();
}

void HAL_USART_MspInit(USART_HandleTypeDef *husart) {
    // enable USART clock
    __HAL_RCC_USART2_CLK_ENABLE();
    // GPIO have already been initialised by sbu_init
}

void HAL_USART_MspDeInit(USART_HandleTypeDef *husart) {
    __HAL_RCC_USART2_CLK_DISABLE();
}

void sbu_uart_on(void) {
    if (usart_handle.Instance) {
        return;
    }

    // turn on USART
    sbu_active_pin_state();
    HAL_Delay(10);

    usart_handle.Instance = USART2;
    usart_handle.Init.BaudRate = 115200;
    usart_handle.Init.WordLength = USART_WORDLENGTH_8B;
    usart_handle.Init.StopBits = USART_STOPBITS_1;
    usart_handle.Init.Parity = USART_PARITY_NONE;
    usart_handle.Init.Mode = USART_MODE_TX_RX;
    usart_handle.Init.CLKPolarity = USART_POLARITY_LOW;
    usart_handle.Init.CLKPhase = USART_PHASE_1EDGE;
    usart_handle.Init.CLKLastBit = USART_LASTBIT_DISABLE;

    if (HAL_OK != HAL_USART_Init(&usart_handle)) {
        ensure(secfalse, NULL);
        return;
    }

    HAL_Delay(10);
}

void sbu_uart_off(void) {
    if (usart_handle.Instance) {
        HAL_USART_DeInit(&usart_handle);
        usart_handle.Instance = NULL;
    }
    // turn off USART
    HAL_Delay(10);
    sbu_default_pin_state();
    HAL_Delay(10);
}

int sbu_read(uint8_t *data, uint16_t len) {
    int res = HAL_USART_Receive(&usart_handle, data, len, 10000);
    ensure(sectrue * ((HAL_OK == res) || (HAL_TIMEOUT == res)), NULL);
    if (HAL_OK == res) {
        return len;
    } else {
        return -1;
    }
}

void sbu_write(const uint8_t *data, uint16_t len) {
    ensure(sectrue * (HAL_OK == HAL_USART_Transmit(&usart_handle, (uint8_t *)data, len, 10000)), NULL);
}

void sbu_set_pins(secbool sbu1, secbool sbu2) {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, sbu1 == sectrue ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, sbu2 == sectrue ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
