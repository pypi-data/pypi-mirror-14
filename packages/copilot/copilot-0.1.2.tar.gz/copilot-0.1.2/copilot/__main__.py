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

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    root = Tk()
    config = Config()
    config.set_file_root(os.path.expanduser(args.file_root))

    s = Style()
    s.configure('Treeview', rowheight=config.tree_item_height)
    s.configure('TButton', font='Helvetica 20')

    if args.server:
        fs = FileServer(4000, config)
        fs.run(debug=True)
    else:
        # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        # print('w: {}, h: {}'.format(w, h))
        # root.overrideredirect(1)
        # root.geometry("%dx%d+0+0" % (w, h))

        root.title('copilot')
        app = HomeFrame(root, config)
        #app = SelectDeviceFrame(root)
        root.mainloop()

if __name__ == '__main__':
    main()
