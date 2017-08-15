from micropython import const

from trezor import io
from trezor import wire
from trezor import main

# initialize the USB stack
usb_wire = io.HID(
    iface_num=0x00,
    ep_in=0x81,
    ep_out=0x01,
    report_desc=bytes([
        0x06, 0x00, 0xff,  # USAGE_PAGE (Vendor Defined)
        0x09, 0x01,        # USAGE (1)
        0xa1, 0x01,        # COLLECTION (Application)
        0x09, 0x20,        # USAGE (Input Report Data)
        0x15, 0x00,        # LOGICAL_MINIMUM (0)
        0x26, 0xff, 0x00,  # LOGICAL_MAXIMUM (255)
        0x75, 0x08,        # REPORT_SIZE (8)
        0x95, 0x40,        # REPORT_COUNT (64)
        0x81, 0x02,        # INPUT (Data,Var,Abs)
        0x09, 0x21,        # USAGE (Output Report Data)
        0x15, 0x00,        # LOGICAL_MINIMUM (0)
        0x26, 0xff, 0x00,  # LOGICAL_MAXIMUM (255)
        0x75, 0x08,        # REPORT_SIZE (8)
        0x95, 0x40,        # REPORT_COUNT (64)
        0x91, 0x02,        # OUTPUT (Data,Var,Abs)
        0xc0,              # END_COLLECTION
    ]),
)
usb_vcp = io.VCP(
    iface_num=0x01,
    data_iface_num=0x02,
    ep_in=0x82,
    ep_out=0x02,
    ep_cmd=0x83,
)
usb_u2f = io.HID(
    iface_num=0x03,
    ep_in=0x84,
    ep_out=0x03,
    report_desc=bytes([
        0x06, 0xd0, 0xf1,  # USAGE_PAGE (FIDO Alliance)
        0x09, 0x01,        # USAGE (U2F HID Authenticator Device)
        0xa1, 0x01,        # COLLECTION (Application)
        0x09, 0x20,        # USAGE (Input Report Data)
        0x15, 0x00,        # LOGICAL_MINIMUM (0)
        0x26, 0xff, 0x00,  # LOGICAL_MAXIMUM (255)
        0x75, 0x08,        # REPORT_SIZE (8)
        0x95, 0x40,        # REPORT_COUNT (64)
        0x81, 0x02,        # INPUT (Data,Var,Abs)
        0x09, 0x21,        # USAGE (Output Report Data)
        0x15, 0x00,        # LOGICAL_MINIMUM (0)
        0x26, 0xff, 0x00,  # LOGICAL_MAXIMUM (255)
        0x75, 0x08,        # REPORT_SIZE (8)
        0x95, 0x40,        # REPORT_COUNT (64)
        0x91, 0x02,        # OUTPUT (Data,Var,Abs)
        0xc0,              # END_COLLECTION
    ]),
)
usb = io.USB(
    vendor_id=0x1209,
    product_id=0x53C1,
    release_num=0x0002,
    manufacturer="SatoshiLabs",
    product="TREZOR",
    serial_number="000000000000000000000000",
)
usb.add(usb_wire)
usb.add(usb_vcp)
usb.add(usb_u2f)
usb.open()

# load applications
from apps.common import storage
if __debug__:
    from apps import debug
from apps import homescreen
from apps import management
from apps import wallet
from apps import ethereum
from apps import fido_u2f

# boot applications
if __debug__:
    debug.boot()
homescreen.boot()
management.boot()
wallet.boot()
ethereum.boot()
fido_u2f.boot(usb_u2f)

# initialize the wire codec pipeline
wire.setup(usb_wire)

# load default homescreen
from apps.homescreen.homescreen import layout_homescreen

# run main even loop and specify which screen is default
main.run(default_workflow=layout_homescreen)
