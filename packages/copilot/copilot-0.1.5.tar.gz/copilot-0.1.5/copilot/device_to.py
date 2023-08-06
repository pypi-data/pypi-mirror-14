from tkinter.ttk import Treeview, Style
import os
try:
    from os import scandir
except ImportError:
    from scandir import scandir

from copilot.frame import CopilotInnerFrame
from copilot.copy_file import CopyFileFrame
from copilot.utils import sizeof_fmt

class DeviceToFrame(CopilotInnerFrame):
    def __init__(self, master, config, state):
        super(DeviceToFrame, self).__init__(master, config)

        self._state = state

        if self._state.action == 'copy':
            self._frame_lbl['text'] = 'Copy To Directory'
        elif self._state.action == 'delete':
            self._frame_lbl['text'] = 'Delete From Directory'

        self._next_btn['command'] = self._next_cmd

        self._tree = Treeview(self._master, columns=('size'))
        self._tree.heading('size', text='Size')
        self._tree.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self._tree.configure(yscrollcommand=self._sb.set)
        self._sb['command'] = self._tree.yview

        self._item_paths = {}
        self._populate_tree(self._state.to_device.part().mount())

    def _next_cmd(self):
        cur_item = self._tree.focus()
        cur_path = self._item_paths.get(cur_item, '')
        if cur_path != '':
            self._state.device_to_path = cur_path
            self._new_state_window(CopyFileFrame, self._state)

    def _populate_tree(self, tree_root):
        self._item_paths = {}
        def insert_path(tree, path, parent_id):
            dirs = [e for e in scandir(path) if e.is_dir()]
            dirs.sort(key=lambda e: e.name)

            for d in dirs:
                dir_name = d.name
                dir_id = '{}-{}'.format(parent_id, dir_name)
                dir_path = os.path.join(path, dir_name)
                tree.insert(parent_id, 'end', dir_id, text=dir_name, tags=('dir'))
                self._item_paths[dir_id] = dir_path
                try:
                    insert_path(tree, dir_path, dir_id)
                except:
                    pass

        insert_path(self._tree, tree_root, '')

        tree = self._tree
        tree.tag_configure('dir', font=self._config.item_font)
        tree.tag_configure('file', font=self._config.item_font)
        tree.tag_configure('file_odd', background='light grey')
