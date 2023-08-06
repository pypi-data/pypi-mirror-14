from tkinter.font import Font
import os.path

class Config(object):
    def __init__(self):
        self.file_root = None
        self.item_font = Font(size=20)

        self.tree_item_height = 30

    def set_file_root(self, file_root):
        self.file_root = file_root
        if not os.path.exists(self.file_root):
            os.makedirs(self.file_root)
