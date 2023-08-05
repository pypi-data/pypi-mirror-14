"""
Improvements on Pyte.
"""
from __future__ import unicode_literals
from pyte.streams import Stream
from pyte.escape import NEL

__all__ = (
    'BetterStream',
)


class BetterStream(Stream):
    """
    Extension to the Pyte `Stream` class that also handles "Esc]<num>...BEL"
    sequences. This is used by xterm to set the terminal title.
    """
    csi = {
        'n': 'cpr',  # Cursor position request.
        'c': 'send_device_attributes',  # csi > Ps c
    }
    csi.update(Stream.csi)

    escape = Stream.escape.copy()
    escape.update({
        # Call next_line instead of line_feed. We always want to go to the left
        # margin if we receive this, unlike \n, which goes one row down.
        # (Except when LNM has been set.)
        NEL: "next_line",
    })

    def __init__(self, screen):
        super(BetterStream, self).__init__()

        self.handlers['square_close'] = self._square_close
        self.handlers['escape'] = self._escape
        self._square_close_data = []
        self.listener = screen

    def _escape(self, char):
        if char == ']':
            #self.state = 'square_close'
            self.current_handler = self._square_close
        else:
            super(BetterStream, self)._escape(char)

    def _square_close(self, char):
        " Parse ``Esc]<num>...BEL``sequence. "
        if char == '\07':
            self.dispatch('square_close', ''.join(self._square_close_data))
            self._square_close_data = []
            #self.state = "stream"
            self.current_handler = self._stream
        else:
            self._square_close_data.append(char)

    def _arguments(self, char):
        if char == '>':
            # Correctly handle 'Esc[>c' (send device attributes.)
            pass
        else:
            super(BetterStream, self)._arguments(char)

    def dispatch(self, event, *args, **kwargs):
        """
        A few additions to improve performance.

        The code from Pyte has a few 'hasattr' calls in here, which is
        inefficient.
        """
        try:
            handler = getattr(self.listener, event)
            handler(*args, **self.flags)
        finally:
            if kwargs.get('reset', True):
                self.reset()

    def feed(self, chars):
        super(BetterStream, self).feed(chars)

    def _parse_corot(self):
        from pyte import ctrl

        basic = self.basic
        #dispatch = self.dispatch
        listener = self.listener
        escape = self.escape
        sharp = self.sharp
        percent = self.percent
        ESC = ctrl.ESC
        CSI = ctrl.CSI
        NUL_OR_DEL = (ctrl.NUL, ctrl.DEL)
        CTRL_SEQUENCES_ALLOWED_IN_CSI = (
            ctrl.BEL, ctrl.BS, ctrl.HT, ctrl.LF, ctrl.VT, ctrl.FF, ctrl.CR)

        def dispatch(event, *args, **kwargs):
            getattr(listener, event)(*args, **kwargs)


        while True:
            char = yield

            if char in basic:
                dispatch(basic[char])

            elif char == ESC:
                char = yield

                if char == '#':
                    dispatch(sharp[(yield)])
                elif char == '%':
                    dispatch(percent[(yield)])
                elif char in '()':
                    dispatch('set_charset', (yield), mode=char)
                else:
                    dispatch(escape[char])

            elif char == CSI:
                current = ''
                params = []
                private = False

                while True:
                    char = yield
                    if char == '?':
                        private = True
                    elif char in CTRL_SEQUENCES_ALLOWED_IN_CSI:
                        dispatch(basic[char], reset=False)
                    elif char == ctrl.SP:
                        pass
                    elif char.isdigit():
                        current += char
                    else:
                        params.append(min(int(current or 0), 9999))

                        if char == ';':
                            current = ''
                        else:
                            dispatch(CSI[char], *params)#, private=private)
                            break  # Break outside CSI.

            elif char not in NUL_OR_DEL:
                dispatch('draw', char)
