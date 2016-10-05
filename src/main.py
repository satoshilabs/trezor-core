import trezor.main
from trezor import msg
from trezor import ui
from trezor import wire

# Load all applications
# from apps import playground
# from apps import homescreen
# from apps import management
# from apps import wallet

# Initialize all applications
# playground.boot()
# homescreen.boot()
# management.boot()
# wallet.boot()

from settings.utils import autodiscover_apps, setup_default_view


autodiscover_apps()


# Change backlight to white for better visibility
ui.display.backlight(255)

# Just a demo to show how to register USB ifaces
msg.setup([(1, 0xF53C), (2, 0xF1D0)])

# Initialize the wire codec pipeline
wire.setup()

# Load default homescreen
# from apps.homescreen.layout_homescreen import layout_homescreen
#
# # Run main even loop and specify, which screen is default
# trezor.main.run(default_workflow=layout_homescreen)

setup_default_view()

