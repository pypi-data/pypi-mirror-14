from distutils.core import setup
setup(
    name = 'copilot',
    packages = ['copilot'],
    version = '0.1.2',
    description = 'Application to manage files on external USB drives',
    author = 'Erik Davidson',
    author_email = 'erik@erikd.org',
    url = 'https://github.com/aphistic/copilot',
    download_url = 'https://github.com/aphistic/copilot/tarball/0.1.2',
    keywords = ['raspberrypi', 'raspberry', 'pi', 'filemanager'],
    classifiers = [],
    entry_points = {
        'gui_scripts': [
            'copilot = copilot.__main__:main'
        ]
    }
)
