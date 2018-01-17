/*
 * Copyright (c) Pavol Rusnak, SatoshiLabs
 *
 * Licensed under TREZOR License
 * see LICENSE file for details
 */

#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/poll.h>
#include <fcntl.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include "usb.h"
#include "touch.h"

void __attribute__((noreturn)) __fatal_error(const char *expr, const char *msg, const char *file, int line, const char *func);

#define ensure(expr, msg) (((expr) == sectrue) ? (void)0 : __fatal_error(#expr, msg, __FILE__, __LINE__, __func__))

#define TREZOR_UDP_IFACE 0
#define TREZOR_UDP_PORT 21324

static int sock;
static struct sockaddr_in si_me, si_other;
static socklen_t slen = 0;

void usb_init(const usb_dev_info_t *dev_info) {
    (void)dev_info;

    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    ensure(sectrue * (sock >= 0), NULL);

    fcntl(sock, F_SETFL, O_NONBLOCK);

    si_me.sin_family = AF_INET;
    const char *ip = getenv("TREZOR_UDP_IP");
    if (ip) {
        si_me.sin_addr.s_addr = inet_addr(ip);
    } else {
        si_me.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    }
    const char *port = getenv("TREZOR_UDP_PORT");
    if (port) {
        si_me.sin_port = htons(atoi(port));
    } else {
        si_me.sin_port = htons(TREZOR_UDP_PORT);
    }

    ensure(sectrue * (0 == bind(sock, (struct sockaddr*)&si_me, sizeof(si_me))), NULL);
}

void usb_deinit(void) {
}

void usb_start(void) {
}

void usb_stop(void) {
}

secbool usb_hid_add(const usb_hid_info_t *info) {
    return sectrue;
}

secbool usb_vcp_add(const usb_vcp_info_t *info) {
    return sectrue;
}

secbool usb_hid_can_read(uint8_t iface_num) {
    if (iface_num != TREZOR_UDP_IFACE) {
        return secfalse;
    }
    struct pollfd fds[] = {
        { sock, POLLIN, 0 },
    };
    int r = poll(fds, 1, 0);
    return sectrue * (r > 0);
}

secbool usb_hid_can_write(uint8_t iface_num) {
    if (iface_num != TREZOR_UDP_IFACE) {
        return secfalse;
    }
    struct pollfd fds[] = {
        { sock, POLLOUT, 0 },
    };
    int r = poll(fds, 1, 0);
    return sectrue * (r > 0);
}

int usb_hid_read(uint8_t iface_num, uint8_t *buf, uint32_t len) {
    if (iface_num != TREZOR_UDP_IFACE) {
        return 0;
    }
    struct sockaddr_in si;
    socklen_t sl = sizeof(si);
    ssize_t r = recvfrom(sock, buf, len, MSG_DONTWAIT, (struct sockaddr *)&si, &sl);
    if (r < 0) {
        return r;
    }
    si_other = si;
    slen = sl;
    static const char *ping_req = "PINGPING";
    static const char *ping_resp = "PONGPONG";
    if (r == strlen(ping_req) && memcmp(ping_req, buf, strlen(ping_req)) == 0) {
        ensure(sectrue * (usb_hid_write(0, (const uint8_t *)ping_resp, strlen(ping_resp)) >= 0), "usb_hid_write");
        return 0;
    }
    return r;
}

int usb_hid_write(uint8_t iface_num, const uint8_t *buf, uint32_t len) {
    if (iface_num != TREZOR_UDP_IFACE) {
        return 0;
    }
    ssize_t r = len;
    if (slen > 0) {
        r = sendto(sock, buf, len, MSG_DONTWAIT, (const struct sockaddr *)&si_other, slen);
    }
    return r;
}

void pendsv_kbd_intr(void) {
}

void mp_hal_set_vcp_iface(int iface_num) {
}
