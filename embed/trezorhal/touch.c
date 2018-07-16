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

#include <string.h>

#include "common.h"
#include "secbool.h"
#include "touch.h"

#define TOUCH_ADDRESS       (0x38U << 1) // the HAL requires the 7-bit address to be shifted by one bit
#define TOUCH_PACKET_SIZE   7U
#define EVENT_PRESS_DOWN    0x00U
#define EVENT_CONTACT       0x80U
#define EVENT_LIFT_UP       0x40U
#define EVENT_NO_EVENT      0xC0U
#define GESTURE_NO_GESTURE  0x00U
#define X_POS_MSB (touch_data[3] & 0x0FU)
#define X_POS_LSB (touch_data[4])
#define Y_POS_MSB (touch_data[5] & 0x0FU)
#define Y_POS_LSB (touch_data[6])

static I2C_HandleTypeDef i2c_handle;

static void touch_power_on(void)
{
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_10, GPIO_PIN_RESET); // CTP_ON/PB10
    HAL_Delay(50);
}

/*
static void touch_power_off(void)
{
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_10, GPIO_PIN_SET); // CTP_ON/PB10
    HAL_Delay(50);
}
*/

void touch_init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;

    // configure the CTP circuitry on/off pin
    GPIO_InitStructure.Mode  = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStructure.Pull  = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStructure.Pin   = GPIO_PIN_10;
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_10, GPIO_PIN_SET);
    HAL_GPIO_Init(GPIOB, &GPIO_InitStructure);

    touch_power_on();

    // Enable I2C clock
    __HAL_RCC_I2C1_CLK_ENABLE();

    // Init SCL and SDA GPIO lines (PB6 & PB7)
    GPIO_InitStructure.Pin = GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStructure.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_LOW; // I2C is a KHz bus and low speed is still good into the low MHz
    GPIO_InitStructure.Alternate = GPIO_AF4_I2C1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStructure);

    i2c_handle.Instance = I2C1;
    i2c_handle.Init.ClockSpeed = 400000;
    i2c_handle.Init.DutyCycle = I2C_DUTYCYCLE_16_9;
    i2c_handle.Init.OwnAddress1 = 0xFE; // master
    i2c_handle.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    i2c_handle.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    i2c_handle.Init.OwnAddress2 = 0;
    i2c_handle.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    i2c_handle.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;

    ensure(sectrue * (HAL_OK == HAL_I2C_Init(&i2c_handle)), NULL);

    // PC4 capacitive touch panel module (CTPM) interrupt (INT) input
    //GPIO_InitStructure.Pin = GPIO_PIN_4;
    //GPIO_InitStructure.Mode = GPIO_MODE_INPUT;
    //GPIO_InitStructure.Pull = GPIO_PULLUP;
    //GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_LOW;
    //GPIO_InitStructure.Alternate = 0;
    //HAL_GPIO_Init(GPIOC, &GPIO_InitStructure);

    // PC5 capacitive touch panel module (CTPM) reset (RSTN)
    GPIO_InitStructure.Pin = GPIO_PIN_5;
    GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_LOW;
    GPIO_InitStructure.Alternate = 0;
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET); // set the pin value before driving it out
    HAL_GPIO_Init(GPIOC, &GPIO_InitStructure); // switch the pin to be an output
    // reset the touch panel by keeping its reset line low (active low) low for a minimum of 5ms
    HAL_Delay(10); // being conservative, min is 5ms
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_SET); // release CTPM reset
    HAL_Delay(310); // "Time of starting to report point after resetting" min is 300ms, giving an extra 10ms

    // set register 0xA4 G_MODE to interrupt polling mode (0x00). basically, CTPM keeps this input line (to PC4) low while a finger is on the screen.
    //uint8_t touch_panel_config[] = {0xA4, 0x00};
    //ensure(sectrue * (HAL_OK == HAL_I2C_Master_Transmit(&i2c_handle, TOUCH_ADDRESS, touch_panel_config, sizeof(touch_panel_config), 10)), NULL);
}

uint32_t touch_read(void)
{
    static uint8_t touch_data[TOUCH_PACKET_SIZE], previous_touch_data[TOUCH_PACKET_SIZE];

    //const GPIO_PinState ctpm_interrupt_line = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_4);

    uint8_t outgoing[] = {0x00}; // start reading from address 0x00
    if (HAL_OK != HAL_I2C_Master_Transmit(&i2c_handle, TOUCH_ADDRESS, outgoing, sizeof(outgoing), 1)) {
        return 0;
    }

    if (HAL_OK != HAL_I2C_Master_Receive(&i2c_handle, TOUCH_ADDRESS, touch_data, TOUCH_PACKET_SIZE, 1)) {
        return 0; // read failure
    }

    if (0 == memcmp(previous_touch_data, touch_data, TOUCH_PACKET_SIZE)) {
        return 0; // polled and got the same event again
    } else {
        memcpy(previous_touch_data, touch_data, TOUCH_PACKET_SIZE);
    }

    const uint32_t number_of_touch_points = touch_data[2] & 0x0F; // valid values are 0, 1, 2 (invalid 0xF before first touch) (tested with FT6206)
    const uint32_t event_flag = touch_data[3] & 0xC0;
    if (touch_data[1] == GESTURE_NO_GESTURE) {
        uint32_t xy = touch_pack_xy((X_POS_MSB << 8) | X_POS_LSB, (Y_POS_MSB << 8) | Y_POS_LSB);
        if ((number_of_touch_points == 1) && (event_flag == EVENT_PRESS_DOWN)) {
            return TOUCH_START | xy;
        } else if ((number_of_touch_points == 1) && (event_flag == EVENT_CONTACT)) {
            return TOUCH_MOVE | xy;
        } else if ((number_of_touch_points == 0) && (event_flag == EVENT_LIFT_UP)) {
            return TOUCH_END | xy;
        }
    }

    return 0;
}

uint32_t touch_click(void)
{
    uint32_t r = 0;
    // flush touch events if any
    while (touch_read()) { }
    // wait for TOUCH_START
    while ((touch_read() & TOUCH_START) == 0) { }
    // wait for TOUCH_END
    while (((r = touch_read()) & TOUCH_END) == 0) { }
    // flush touch events if any
    while (touch_read()) { }
    // return last touch coordinate
    return r;
}
