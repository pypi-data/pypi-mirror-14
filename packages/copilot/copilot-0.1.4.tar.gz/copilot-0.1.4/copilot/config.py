from tkinter.font import Font
import os.path

class Config(object):
    def __init__(self):
        self.full_screen = False
        self.file_root = None
        self.item_font = Font(size=16)

        self.tree_item_height = 30
        self.sb_size = 25

        self.web_port = 4000

    def set_file_root(self, file_root):
        self.file_root = file_root
        if not os.path.exists(self.file_root):
            os.makedirs(self.file_root)
