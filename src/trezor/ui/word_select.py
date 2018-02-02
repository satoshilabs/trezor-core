from micropython import const
from trezor import loop
from trezor import ui
from trezor.ui import Widget
from trezor.ui.button import Button, BTN_CLICKED

_W12 = const(12)
_W15 = const(15)
_W18 = const(18)
_W24 = const(24)


class WordSelector(Widget):

    def __init__(self, content):
        self.content = content
        self.w12 = Button(ui.grid(8, n_y=4, n_x=4, cells_x=2), str(_W12),
                          style=ui.BTN_KEY)
        self.w15 = Button(ui.grid(10, n_y=4, n_x=4, cells_x=2), str(_W15),
                          style=ui.BTN_KEY)
        self.w18 = Button(ui.grid(12, n_y=4, n_x=4, cells_x=2), str(_W18),
                          style=ui.BTN_KEY)
        self.w24 = Button(ui.grid(14, n_y=4, n_x=4, cells_x=2), str(_W24),
                          style=ui.BTN_KEY)

    def render(self):
        self.w12.render()
        self.w15.render()
        self.w18.render()
        self.w24.render()

    def touch(self, event, pos):
        if self.w12.touch(event, pos) == BTN_CLICKED:
            return _W12
        if self.w15.touch(event, pos) == BTN_CLICKED:
            return _W15
        if self.w18.touch(event, pos) == BTN_CLICKED:
            return _W18
        if self.w24.touch(event, pos) == BTN_CLICKED:
            return _W24

    async def __iter__(self):
        return await loop.wait(super().__iter__(), self.content)
