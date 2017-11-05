from trezor import ui, loop, res
from trezor.utils import unimport


async def swipe_to_rotate():
    from trezor.ui.swipe import Swipe, degrees

    swipe = await Swipe(absolute=True)
    ui.display.orientation(degrees(swipe))


async def dim_screen():
    await loop.sleep(5 * 1000000)
    await ui.backlight_slide(ui.BACKLIGHT_DIM)
    while True:
        await loop.sleep(10000000)


@ui.layout
async def display_homescreen():
    from apps.common import storage

    image = res.load('apps/homescreen/res/trezor_lock.toig')
    ui.display.bar(0, 0, ui.SCREEN, ui.SCREEN, ui.BG)
    ui.display.icon((ui.SCREEN - 124) // 2, (ui.SCREEN - 40 - 180) // 2, image, ui.FG, ui.BG)

    if not storage.is_initialized():
        label = 'Go to trezor.io/start'
    else:
        label = storage.get_label() or 'My TREZOR'
    ui.display.text_center(ui.SCREEN // 2, ui.SCREEN - 20, label, ui.BOLD, ui.FG, ui.BG)

    await dim_screen()


@unimport
async def layout_homescreen():
    while True:
        await loop.wait(swipe_to_rotate(), display_homescreen())
