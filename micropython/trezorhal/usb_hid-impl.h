#define USB_DESC_TYPE_HID            0x21
#define USB_DESC_TYPE_REPORT         0x22

#define HID_REQ_SET_PROTOCOL         0x0b
#define HID_REQ_GET_PROTOCOL         0x03
#define HID_REQ_SET_IDLE             0x0a
#define HID_REQ_GET_IDLE             0x02

/* usb_hid_add adds and configures new USB HID interface according to
 * configuration options passed in `info`. */
int usb_hid_add(const usb_hid_info_t *info) {

    usb_iface_t *iface = usb_get_iface(info->iface_num);

    if (iface == NULL) {
        return 1; // Invalid interface number
    }
    if (iface->type != USB_IFACE_TYPE_DISABLED) {
        return 1; // Interface is already enabled
    }

    usb_hid_descriptor_block_t *d = usb_desc_alloc_iface(sizeof(usb_hid_descriptor_block_t));

    if (d == NULL) {
        return 1; // Not enough space in the configuration descriptor
    }

    if ((info->ep_in & USB_EP_DIR_MSK) != USB_EP_DIR_IN) {
        return 1; // IN EP is invalid
    }
    if ((info->ep_out & USB_EP_DIR_MSK) != USB_EP_DIR_OUT) {
        return 1; // OUT EP is invalid
    }
    if (info->rx_buffer == NULL) {
        return 1;
    }
    if (info->report_desc == NULL) {
        return 1;
    }

    // Interface descriptor
    d->iface.bLength            = USB_LEN_IF_DESC;
    d->iface.bDescriptorType    = USB_DESC_TYPE_INTERFACE;
    d->iface.bInterfaceNumber   = info->iface_num;
    d->iface.bAlternateSetting  = 0x00;
    d->iface.bNumEndpoints      = 0x02;
    d->iface.bInterfaceClass    = 0x03; // HID Class
    d->iface.bInterfaceSubClass = info->subclass;
    d->iface.bInterfaceProtocol = info->protocol;
    d->iface.iInterface         = 0x00; // Index of string descriptor describing the interface

    // HID descriptor
    d->hid.bLength                 = sizeof(usb_hid_descriptor_t);
    d->hid.bDescriptorType         = USB_DESC_TYPE_HID;
    d->hid.bcdHID                  = 0x1101; // HID Class Spec release number
    d->hid.bCountryCode            = 0x00;   // Hardware target country
    d->hid.bNumDescriptors         = 0x01;   // Number of HID class descriptors to follow
    d->hid.bReportDescriptorType   = USB_DESC_TYPE_REPORT;
    d->hid.wReportDescriptorLength = info->report_desc_len;

    // IN endpoint (sending)
    d->ep_in.bLength          = USB_LEN_EP_DESC;
    d->ep_in.bDescriptorType  = USB_DESC_TYPE_ENDPOINT;
    d->ep_in.bEndpointAddress = info->ep_in;
    d->ep_in.bmAttributes     = USBD_EP_TYPE_INTR;
    d->ep_in.wMaxPacketSize   = info->max_packet_len;
    d->ep_in.bInterval        = info->polling_interval;

    // OUT endpoint (receiving)
    d->ep_out.bLength          = USB_LEN_EP_DESC;
    d->ep_out.bDescriptorType  = USB_DESC_TYPE_ENDPOINT;
    d->ep_out.bEndpointAddress = info->ep_out;
    d->ep_out.bmAttributes     = USBD_EP_TYPE_INTR;
    d->ep_out.wMaxPacketSize   = info->max_packet_len;
    d->ep_out.bInterval        = info->polling_interval;

    // Config descriptor
    usb_desc_add_iface(sizeof(usb_hid_descriptor_block_t));

    // Interface state
    iface->type = USB_IFACE_TYPE_HID;
    iface->hid.ep_in = info->ep_in;
    iface->hid.ep_out = info->ep_out;
    iface->hid.rx_buffer = info->rx_buffer;
    iface->hid.max_packet_len = info->max_packet_len;
    iface->hid.report_desc_len = info->report_desc_len;
    iface->hid.report_desc = info->report_desc;
    iface->hid.desc_block = d;

    return 0;
}

int usb_hid_can_read(uint8_t iface_num) {
    usb_iface_t *iface = usb_get_iface(iface_num);
    if (iface == NULL) {
        return 0; // Invalid interface number
    }
    if (iface->type != USB_IFACE_TYPE_HID) {
        return 0; // Invalid interface type
    }
    if (iface->hid.rx_buffer_len == 0) {
        return 0; // Nothing in the receiving buffer
    }
    if (usb_dev_handle.dev_state != USBD_STATE_CONFIGURED) {
        return 0; // Device is not configured
    }
    return 1;
}

int usb_hid_can_write(uint8_t iface_num) {
    usb_iface_t *iface = usb_get_iface(iface_num);
    if (iface == NULL) {
        return 0; // Invalid interface number
    }
    if (iface->type != USB_IFACE_TYPE_HID) {
        return 0; // Invalid interface type
    }
    if (iface->hid.in_idle == 0) {
        return 0; // Last transmission is not over yet
    }
    if (usb_dev_handle.dev_state != USBD_STATE_CONFIGURED) {
        return 0; // Device is not configured
    }
    return 1;
}

int usb_hid_read(uint8_t iface_num, uint8_t *buf, uint32_t len) {
    usb_iface_t *iface = usb_get_iface(iface_num);
    if (iface == NULL) {
        return -1; // Invalid interface number
    }
    if (iface->type != USB_IFACE_TYPE_HID) {
        return -2; // Invalid interface type
    }
    usb_hid_state_t *state = &iface->hid;

    // Copy maximum possible amount of data and truncate the buffer length
    if (len < state->rx_buffer_len) {
        return 0; // Not enough data in the read buffer
    }
    len = state->rx_buffer_len;
    state->rx_buffer_len = 0;
    memcpy(buf, state->rx_buffer, len);

    // Clear NAK to indicate we are ready to read more data
    usb_ep_clear_nak(&usb_dev_handle, state->ep_out);

    return len;
}

int usb_hid_write(uint8_t iface_num, const uint8_t *buf, uint32_t len) {
    usb_iface_t *iface = usb_get_iface(iface_num);
    if (iface == NULL) {
        return -1; // Invalid interface number
    }
    if (iface->type != USB_IFACE_TYPE_HID) {
        return -2; // Invalid interface type
    }
    usb_hid_state_t *state = &iface->hid;

    state->in_idle = 0;
    USBD_LL_Transmit(&usb_dev_handle, state->ep_in, UNCONST(buf), (uint16_t)len);

    return len;
}

int usb_hid_read_blocking(uint8_t iface_num, uint8_t *buf, uint32_t len, uint32_t timeout) {
    uint32_t start = HAL_GetTick();
    while (!usb_hid_can_read(iface_num)) {
        if (HAL_GetTick() - start >= timeout) {
            return 0; // Timeout
        }
        __WFI(); // Enter sleep mode, waiting for interrupt
    }
    return usb_hid_read(iface_num, buf, len);
}

int usb_hid_write_blocking(uint8_t iface_num, const uint8_t *buf, uint32_t len, uint32_t timeout) {
    uint32_t start = HAL_GetTick();
    while (!usb_hid_can_write(iface_num)) {
        if (HAL_GetTick() - start >= timeout) {
            return 0; // Timeout
        }
        __WFI(); // Enter sleep mode, waiting for interrupt
    }
    return usb_hid_write(iface_num, buf, len);
}

static int usb_hid_class_init(USBD_HandleTypeDef *dev, usb_hid_state_t *state, uint8_t cfg_idx) {
    // Open endpoints
    USBD_LL_OpenEP(dev, state->ep_in, USBD_EP_TYPE_INTR, state->max_packet_len);
    USBD_LL_OpenEP(dev, state->ep_out, USBD_EP_TYPE_INTR, state->max_packet_len);

    // Reset the state
    state->in_idle = 1;
    state->protocol = 0;
    state->idle_rate = 0;
    state->alt_setting = 0;

    // Prepare the OUT EP to receive next packet
    USBD_LL_PrepareReceive(dev, state->ep_out, state->rx_buffer, state->max_packet_len);

    return USBD_OK;
}

static int usb_hid_class_deinit(USBD_HandleTypeDef *dev, usb_hid_state_t *state, uint8_t cfg_idx) {
    // Close endpoints
    USBD_LL_CloseEP(dev, state->ep_in);
    USBD_LL_CloseEP(dev, state->ep_out);

    return USBD_OK;
}

static int usb_hid_class_setup(USBD_HandleTypeDef *dev, usb_hid_state_t *state, USBD_SetupReqTypedef *req) {
    switch (req->bmRequest & USB_REQ_TYPE_MASK) {

    // Class request
    case USB_REQ_TYPE_CLASS:
        switch (req->bRequest) {

        case HID_REQ_SET_PROTOCOL:
            state->protocol = req->wValue;
            break;

        case HID_REQ_GET_PROTOCOL:
            USBD_CtlSendData(dev, &state->protocol, sizeof(state->protocol));
            break;

        case HID_REQ_SET_IDLE:
            state->idle_rate = req->wValue >> 8;
            break;

        case HID_REQ_GET_IDLE:
            USBD_CtlSendData(dev, &state->idle_rate, sizeof(state->idle_rate));
            break;

        default:
            USBD_CtlError(dev, req);
            return USBD_FAIL;
        }
        break;

    // Interface & Endpoint request
    case USB_REQ_TYPE_STANDARD:
        switch (req->bRequest) {

        case USB_REQ_SET_INTERFACE:
            state->alt_setting = req->wValue;
            break;

        case USB_REQ_GET_INTERFACE:
            USBD_CtlSendData(dev, &state->alt_setting, sizeof(state->alt_setting));
            break;

        case USB_REQ_GET_DESCRIPTOR:
            switch (req->wValue >> 8) {

            case USB_DESC_TYPE_HID:
                USBD_CtlSendData(dev, (uint8_t *)&state->desc_block->hid, MIN(req->wLength, sizeof(state->desc_block->hid)));
                break;

            case USB_DESC_TYPE_REPORT:
                USBD_CtlSendData(dev, UNCONST(state->report_desc), MIN(req->wLength, state->report_desc_len));
                break;
            }
            break;
        }
        break;
    }
    return USBD_OK;
}

static uint8_t usb_hid_class_data_in(USBD_HandleTypeDef *dev, usb_hid_state_t *state, uint8_t ep_num) {
    if ((ep_num | USB_EP_DIR_IN) == state->ep_in) {
        state->in_idle = 1;
    }
    return USBD_OK;
}

static uint8_t usb_hid_class_data_out(USBD_HandleTypeDef *dev, usb_hid_state_t *state, uint8_t ep_num) {
    if (ep_num == state->ep_out) {
        // User should provide state->rx_buffer_len that is big
        // enough for state->max_packet_len bytes.
        state->rx_buffer_len = USBD_LL_GetRxDataSize(dev, ep_num);

        // Prepare the OUT EP to receive next packet
        USBD_LL_PrepareReceive(dev, ep_num, state->rx_buffer, state->max_packet_len);

        if (state->rx_buffer_len > 0) {
            // Block the OUT EP until we process received data
            usb_ep_set_nak(dev, ep_num);
        }
    }
    return USBD_OK;
}
