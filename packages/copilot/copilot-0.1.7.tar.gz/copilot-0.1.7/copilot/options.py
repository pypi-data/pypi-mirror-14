from tkinter.ttk import Frame, Button, Notebook


class OptionsFrame(Frame):
    def __init__(self, master):
        super(OptionsFrame, self).__init__(master)
        self.master = master

        self.notebook = Notebook(self)
        self.notebook.pack()

        self.f1 = Frame(self.notebook)
        self.notebook.add(self.f1, text='F1')

        self.quit_button = Button(
            self.f1,
            text='Quit',
            width=25,
            command=self._close_windows)
        self.quit_button.pack()
        self.f1.pack()
        self.pack()

    def _close_windows(self):
        self.master.destroy()
