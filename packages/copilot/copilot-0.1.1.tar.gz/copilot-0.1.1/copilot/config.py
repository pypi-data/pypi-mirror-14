from tkinter.font import Font
import os.path

class Config(object):
    def __init__(self):
        self.file_root = '/home/aphistic/tmp'
        self.item_font = Font(size=20)

        self.tree_item_height = 30

        if not os.path.exists(self.file_root):
            os.makedirs(self.file_root)
