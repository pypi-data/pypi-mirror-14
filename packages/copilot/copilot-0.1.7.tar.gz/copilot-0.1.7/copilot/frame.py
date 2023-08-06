from tkinter import Toplevel, VERTICAL
from tkinter.ttk import Frame, Button, Label, Scrollbar

class CopilotBaseFrame(Frame):
    def __init__(self, master, config):
        super(CopilotBaseFrame, self).__init__(master)
        self._master = master
        self._config = config

    def _make_full(self, root):
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))

    def _new_window_cb(self, frame_type):
        def _cb(cb_self, cb_type):
            new_window = Toplevel(cb_self._master)
            cb_type(new_window, self._config)

        return lambda: _cb(self, frame_type)

    def _new_state_window(self, frame_type, state):
        new_window = Toplevel(self._master)
        frame_type(new_window, self._config, state)

    def _new_state_window_cb(self, frame_type, state):
        def _cb(cb_self, cb_type, cb_state):
            new_window = Toplevel(cb_self._master)
            cb_type(new_window, self._config, cb_state)

        return lambda: _cb(self, frame_type, state)

class CopilotMainFrame(CopilotBaseFrame):
    def __init__(self, master, config):
        super(CopilotMainFrame, self).__init__(master, config)
        if config.full_screen:
            self._make_full(master)


class CopilotInnerFrame(CopilotBaseFrame):
    def __init__(self, master, config):
        super(CopilotInnerFrame, self).__init__(master, config)

        if config.full_screen:
            self._make_full(master)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self._create_header()

        self._sb = Scrollbar(self._master, orient=VERTICAL)
        self._sb.grid(row=1, column=3, sticky='nse')

        self._next_hidden = False

    def _cmd_back(self):
        self._master.destroy()

    def _create_header(self):
        self.back_btn = Button(
            self._master,
            text='< Back',
            command=self._cmd_back
        )
        self.back_btn.grid(row=0, column=0, sticky='w')

        self._frame_lbl = Label(
            self.master,
            text='',
            anchor='center',
            font=self._config.item_font
        )
        self._frame_lbl.grid(row=0, column=1, sticky='ew')

        self._next_btn = Button(
            self.master,
            text='Next >'
        )
        self._next_btn.grid(row=0, column=2, sticky='e')

    def _hide_next(self):
        if not self._next_hidden:
            self._next_btn.grid_remove()
            self._next_hidden = True

    def _show_next(self):
        if self._next_hidden:
            self._next_btn.grid(row=0, column=2, sticky='e')
            self._next_hidden = False
