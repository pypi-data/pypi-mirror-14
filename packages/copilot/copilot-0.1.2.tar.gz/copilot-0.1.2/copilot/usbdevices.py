import os.path
from subprocess import check_output

def _read_file(path):
    with open(path) as f:
        return f.read()

def usb_drives():
    drives = []

    with open('/proc/partitions') as parts_file:
        lines = parts_file.readlines()[2:]
        for line in lines:
            words = [x.strip() for x in line.split()]
            minor_number = int(words[1])
            dev_name = words[3]
            if minor_number % 16 == 0:
                block_path = '/sys/class/block/{}'.format(dev_name)
                if os.path.islink(block_path):
                    if os.path.realpath(block_path).find('/usb') > 0:
                        drives.append(UsbDrive('/dev/{}'.format(dev_name), block_path))

    return drives

class UsbDrive(object):
    def __init__(self, dev_path, info_path):
        self._dev_path = dev_path
        self._info_path = info_path

        self._info = self._discover_info()
        self._partitions = self._discover_parts()

    def __str__(self):
        return self.name()

    def _discover_info(self):
        return {
            'vendor': _read_file(os.path.join(self._info_path, 'device/vendor')).strip(),
            'model': _read_file(os.path.join(self._info_path, 'device/model')).strip(),
            'size': int(_read_file(os.path.join(self._info_path, 'size'))) << 9
        }

        return info

    def _discover_parts(self):
        parts = []
        devs = [x.path for x in os.scandir('/dev') if x.path[:len(self._dev_path)] == self._dev_path and x.path != self._dev_path]
        mounts = {x.split(b' ')[0].decode('utf-8'): x.split(b' ')[2].decode('utf-8') for x in check_output(['mount']).split(b'\n') if len(x.split(b' ')) > 3}
        for dev in devs:
            mount = mounts.get(dev)
            if mount:
                parts.append(DrivePartition(dev, mount))

        return parts

    def name(self):
        return '{} {} ({}GB)'.format(self.vendor(), self.model(), self.size('g')).strip()

    def path(self):
        return self._dev_path

    def vendor(self):
        return self._info['vendor']

    def model(self):
        return self._info['model']

    def size(self, units='b'):
        units = units.lower()
        if units == 'b':
            new_size = self._info['size']
        elif units == 'k':
            new_size = self._info['size'] / 1024
        elif units == 'm':
            new_size = (self._info['size'] / 1024) / 1024
        elif units == 'g':
            new_size = ((self._info['size'] / 1024) / 1024) / 1024

        return round(new_size, 1)

    def partitions(self):
        return self._partitions


class DrivePartition(object):
    def __init__(self, partition_path, mount_path):
        self._part_path = partition_path
        self._mount_path = mount_path

    def path(self):
        return self._part_path

    def mount(self):
        return self._mount_path

    def __str__(self):
        return self._mount_path
