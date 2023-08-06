from tkinter import Tk
from tkinter.ttk import Style
from copilot.config import Config
from copilot.home import HomeFrame
from copilot.select_device import SelectDeviceFrame
from copilot.file_server import FileServer
import argparse
import logging
import os.path

def main():
    log = logging.getLogger()
    log.setLevel(logging.ERROR)

    parser = argparse.ArgumentParser(description='Run stuff')
    parser.add_argument('--server', action='store_true', default=False)
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--file_root', default=os.path.expanduser('~'))
    parser.add_argument('--full', action='store_true', default=False)

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    root = Tk()
    config = Config()
    config.full_screen = args.full
    config.set_file_root(os.path.expanduser(args.file_root))

    s = Style()
    s.configure('Treeview', rowheight=config.tree_item_height)
    s.configure('TButton', font='Helvetica 16')
    s.configure('Vertical.TScrollbar', arrowsize=config.sb_size)

    if args.server:
        fs = FileServer(config.web_port, config)
        fs.run(debug=True)
    else:
        root.title('copilot')
        app = HomeFrame(root, config)
        root.mainloop()

if __name__ == '__main__':
    main()
