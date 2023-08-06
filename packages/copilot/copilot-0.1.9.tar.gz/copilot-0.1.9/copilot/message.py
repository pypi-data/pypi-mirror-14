from tkinter import Toplevel
from tkinter.ttk import Frame, Button, Label

from copilot.frame import CopilotBaseFrame

class MessageFrame(CopilotBaseFrame):
    def __init__(self, master, config):
        super(MessageFrame, self).__init__(master, config)

    def _make_full(self, root):
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))

class ConfirmFrame(MessageFrame):
    def __init__(self, master, config):
        super(ConfirmFrame, self).__init__(master, config)

        if config.full_screen:
            self._make_full(master)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self._result = False

        self._frame_lbl = Label(
            self.master,
            text='',
            anchor='center',
            font=self._config.item_font
        )
        self._frame_lbl.grid(row=0, column=0, columnspan=2, sticky='snew')

        self._prev_btn = Button(
            self.master,
            text='Cancel',
            command=self._prev_cmd
        )
        self._prev_btn.grid(row=1, column=0, sticky='snew')

        self._next_btn = Button(
            self.master,
            text='OK',
            command=self._next_cmd
        )
        self._next_btn.grid(row=1, column=1, sticky='snew')

    def show(master, config, msg, ok_text, cancel_text):
        new_window = Toplevel(master)
        dlg = ConfirmFrame(new_window, config)
        dlg._frame_lbl['text'] = msg
        dlg._prev_btn['text'] = cancel_text
        dlg._next_btn['text'] = ok_text

        dlg.wait_window(new_window)

        return dlg._result

    def _prev_cmd(self):
        self._result = False
        self._master.destroy()
    def _next_cmd(self):
        self._result = True
        self._master.destroy()

class OkFrame(MessageFrame):
    def __init__(self, master, config):
        super(OkFrame, self).__init__(master, config)

        if config.full_screen:
            self._make_full(master)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self._frame_lbl = Label(
            self.master,
            text='',
            anchor='center',
            font=self._config.item_font
        )
        self._frame_lbl.grid(row=0, column=0, sticky='snew')

        self._next_btn = Button(
            self.master,
            text='OK',
            command=self._next_cmd
        )
        self._next_btn.grid(row=1, column=0, sticky='snew')

    def show(master, config, msg):
        new_window = Toplevel(master)
        dlg = OkFrame(new_window, config)
        dlg._frame_lbl['text'] = msg

    def _next_cmd(self):
        self._master.destroy()
