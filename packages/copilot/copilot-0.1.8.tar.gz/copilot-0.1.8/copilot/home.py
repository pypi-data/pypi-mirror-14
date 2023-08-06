from tkinter import Toplevel
from tkinter.ttk import Frame, Button

from copilot.copy_state import CopyState
from copilot.frame import CopilotMainFrame
from copilot.file_server import FileServerFrame
from copilot.select_device import SelectDeviceFrame
from copilot.options import OptionsFrame

class HomeFrame(CopilotMainFrame):
    def __init__(self, master, config):
        super(HomeFrame, self).__init__(master, config)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.copy_btn = Button(
            self._master,
            text='Copy Files',
            command=self._cmd_copy
        )
        self.copy_btn.grid(row=0, column=0, sticky='snew')

        self.delete_btn = Button(
            self._master,
            text='Delete Files',
            command=self._cmd_delete
        )
        self.delete_btn.grid(row=1, column=0, sticky='snew')

        self.upload_btn = Button(
            self._master,
            text='Upload Files',
            command=self._new_window_cb(FileServerFrame)
        )
        self.upload_btn.grid(row=2, column=0, sticky='snew')

        self.quit_btn = Button(
            self._master,
            text='Quit',
            command=self._cmd_quit
        )
        self.quit_btn.grid(row=3, column=0, sticky='snew')

    def _cmd_copy(self):
        state = CopyState()
        state.action = 'copy'
        self._new_state_window(SelectDeviceFrame, state)

    def _cmd_delete(self):
        state = CopyState()
        state.action = 'delete'
        self._new_state_window(SelectDeviceFrame, state)

    def _cmd_quit(self):
        self._master.destroy()
