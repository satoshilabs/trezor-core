/*
 * Copyright (c) Pavol Rusnak, SatoshiLabs
 *
 * Licensed under TREZOR License
 * see LICENSE file for details
 */

#ifndef __DISPLAY_H__
#define __DISPLAY_H__

#include <stdint.h>

// ILI9341V and ST7789V drivers both support 240px x 320px display resolution
#define MAX_DISPLAY_RESX 240
#define MAX_DISPLAY_RESY 320
// X and Y display resolution used
#define DISPLAY_RESX 240
#define DISPLAY_RESY 240

#ifndef TREZOR_FONT_MONO_DISABLE
#define FONT_MONO   0
#endif
#ifndef TREZOR_FONT_NORMAL_DISABLE
#define FONT_NORMAL 1
#endif
#ifndef TREZOR_FONT_BOLD_DISABLE
#define FONT_BOLD   2
#endif

#define AVATAR_IMAGE_SIZE 144
#define LOADER_ICON_SIZE 64

#define RGB16(R, G, B) ((R & 0xF8) << 8) | ((G & 0xFC) << 3) | ((B & 0xF8) >> 3)

#define COLOR_WHITE      RGB16(255, 255, 255)
#define COLOR_GRAY128    RGB16(127, 127, 127)
#define COLOR_GRAY64     RGB16(63, 63, 63)
#define COLOR_BLACK      RGB16(0, 0, 0)
#define COLOR_RED128     RGB16(127, 0, 0)
#define COLOR_GREEN128   RGB16(0, 127, 0)
#define COLOR_BLUE128    RGB16(0, 0, 127)

// provided by port

void display_pwm_init(void);
int display_init(void);
void display_refresh(void);
void display_save(const char *filename);

// provided by common

void display_clear(void);

void display_bar(int x, int y, int w, int h, uint16_t c);
void display_bar_radius(int x, int y, int w, int h, uint16_t c, uint16_t b, uint8_t r);

void display_image(int x, int y, int w, int h, const void *data, int datalen);
void display_avatar(int x, int y, const void *data, int datalen, uint16_t fgcolor, uint16_t bgcolor);
void display_icon(int x, int y, int w, int h, const void *data, int datalen, uint16_t fgcolor, uint16_t bgcolor);

#ifndef TREZOR_PRINT_DISABLE
void display_print_color(uint16_t fgcolor, uint16_t bgcolor);
void display_print(const char *text, int textlen);
void display_printf(const char *fmt, ...) __attribute__ ((__format__ (__printf__, 1, 2)));
#endif

void display_text(int x, int y, const char *text, int textlen, uint8_t font, uint16_t fgcolor, uint16_t bgcolor);
void display_text_center(int x, int y, const char *text, int textlen, uint8_t font, uint16_t fgcolor, uint16_t bgcolor);
void display_text_right(int x, int y, const char *text, int textlen, uint8_t font, uint16_t fgcolor, uint16_t bgcolor);
int display_text_width(const char *text, int textlen, uint8_t font);

void display_qrcode(int x, int y, const char *data, int datalen, uint8_t scale);
void display_loader(uint16_t progress, int yoffset, uint16_t fgcolor, uint16_t bgcolor, const uint8_t *icon, uint32_t iconlen, uint16_t iconfgcolor);

int *display_offset(int xy[2]);
int display_orientation(int degrees);
int display_backlight(int val);

#endif
