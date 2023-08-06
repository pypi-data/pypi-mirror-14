from tkinter.ttk import Scrollbar
from tkinter.ttk import Treeview, Style
import os
import shutil
import sys
try:
    from os import scandir
except ImportError:
    from scandir import scandir

from copilot.frame import CopilotInnerFrame
from copilot.message import OkFrame, ConfirmFrame
from copilot.utils import sizeof_fmt

class CopyFileFrame(CopilotInnerFrame):
    def __init__(self, master, config, state):
        super(CopyFileFrame, self).__init__(master, config)

        self._state = state

        self._item_paths = {}

        self._tree = Treeview(self._master, columns=('size'))
        self._tree.heading('size', text='Size')
        self._tree.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self._tree.configure(yscrollcommand=self._sb.set)
        self._sb['command'] = self._tree.yview

        if self._state.action == 'copy':
            self._next_btn['text'] = 'Copy'
            self._frame_lbl['text'] = 'Copy File'
            self._populate_tree(self._config.file_root)
        elif self._state.action == 'delete':
            self._next_btn['text'] = 'Delete'
            self._frame_lbl['text'] = 'Delete File'
            self._populate_tree(self._state.to_device.part().mount())

        self._next_btn['command'] = self._next_cmd

    def _next_cmd(self):
        if self._state.action == 'copy':
            self._copy_file()
        elif self._state.action == 'delete':
            self._delete_file()

    def _copy_file(self):
        cur_item = self._tree.focus()
        cur_path = self._item_paths.get(cur_item, '')
        if cur_path != '':
            new_path = os.path.join(self._state.device_to_path, os.path.basename(cur_path))
            try:
                if os.path.exists(new_path):
                    if ConfirmFrame.show(
                        self._master, self._config,
                        'The file already exists in the destination. '
                        'Would you like to overwrite it?',
                        'Yes', 'No'
                    ):
                        shutil.copyfile(cur_path, new_path)
                else:
                    shutil.copyfile(cur_path, new_path)
            except PermissionError:
                OkFrame.show(
                    self._master, self._config,
                    'Error copying file:\n\nInvalid permissions'
                )
            except Exception as e:
                OkFrame.show(
                    self._master, self._config,
                    'An error occurred while copying the file:\n\n{}'.format(e)
                )

    def _delete_file(self):
        cur_item = self._tree.focus()
        cur_path = self._item_paths.get(cur_item, '')
        if cur_path != '':
            disp_path = cur_path[len(self._state.to_device.part().mount()):]
            try:
                if ConfirmFrame.show(
                    self._master, self._config,
                    'Are you sure you\'d like to delete this file?\n{}'.format(disp_path),
                    'Yes', 'No'
                ):
                    os.remove(cur_path)
                    self._tree.delete(self._tree.focus())
            except PermissionError:
                OkFrame.show(
                    self._master, self._config,
                    'Error deleting file:\n\nInvalid permissions'
                )
            except Exception as e:
                OkFrame.show(
                    self._master, self._config,
                    'An error occurred while deleting the file:\n\n{}'.format(e)
                )

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
                try:
                    insert_path(tree, dir_path, dir_id)
                except:
                    pass

            files = [e for e in scandir(path) if e.is_file()]
            files.sort(key=lambda e: e.name)

            for idx, f in enumerate(files):
                file_name = f.name
                file_id = '{}-{}'.format(parent_id, file_name)
                file_stat = f.stat()
                file_size = sizeof_fmt(file_stat.st_size)
                file_path = os.path.join(path, file_name)
                self._item_paths[file_id] = file_path

                if idx % 2 == 0:
                    file_bg = 'file_even'
                else:
                    file_bg = 'file_odd'

                tree.insert(
                    parent_id,
                    'end',
                    file_id,
                    text=file_name,
                    tags=('file', file_bg),
                    values=(file_size)
                )

        insert_path(self._tree, tree_root, '')

        tree = self._tree
        tree.tag_configure('dir', font=self._config.item_font)
        tree.tag_configure('file', font=self._config.item_font)
        tree.tag_configure('file_odd', background='light grey')
